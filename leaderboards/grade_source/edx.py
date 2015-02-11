# pylint: disable=import-error
"""
Fetch grades from the edX LMS as efficiently as possible.
"""
from .base import GradeSource

try:
    from courseware.grades import get_score
    from util.module_utils import yield_dynamic_descriptor_descendents
    EDX_FOUND = True
except ImportError:
    EDX_FOUND = False


class EdxLmsGradeSource(GradeSource):
    """
    edX LMS grade access implementation
    """
    SOURCE_NAME = "edx"

    def is_supported(self):
        """
        Does self.host_block.runtime support this type of grade source?
        """
        try:
            runtime = self.host_block.runtime
            return EDX_FOUND and hasattr(runtime, "get_real_user") and hasattr(runtime, "anonymous_student_id")
        except Exception:
            return False

    def get_grades(self, target_block_id, limit_hint=None):
        """
        Get the grades as a percentage for the top students who have started or
        completed target_block_id and its descendants.

        The current implementation is as follows:

           This block 'grade_source' class calls the get_score() grading
           computation built into edX which returns the grade for the current
           student only, which is then cached in the grade_leaderboard xblock
           in a user_state_summary field. The block will then use the cached
           grades from all students to compute the leaderboard.

           Pros:
             * Fairly efficient - generally uses cached grades, making one MySQL query per block
             * Grading should match edX grading very well since it uses the same method
             * Supports all block types
           Cons:
             * Requires students to view the block before their grades appear
               in the leaderboard - could result in missing/outdated data, depending
               on where the block appears in the course and how often students view
               the leaderboard.
             * Storing data in Scope.user_state_summary will lead to read write conflicts.
               e.g. if two students view the courseware simultaneously and their requests
               are handled by different gunicorn processes.

        TODO: We will need to replace this implementation with something that uses celery
        to update student grades asynchronously and stores them in a more robust cache format.
        """
        total_correct, total_possible = 0, 0
        course_id = target_block_id.course_key.for_branch(None).version_agnostic()
        target_block = self.host_block.runtime.get_block(target_block_id)
        student = self.host_block.runtime.get_real_user(self.host_block.runtime.anonymous_student_id)

        def create_module(descriptor):
            return target_block.runtime.get_block(descriptor.location)

        for module_descriptor in yield_dynamic_descriptor_descendents(target_block, create_module):

            (correct, total) = get_score(course_id, student, module_descriptor, create_module)
            if (correct is None and total is None) or (not total > 0):
                continue

            # Note we ignore the 'graded' flag since authors may wish to use a leaderboard for non-graded content
            total_correct += correct
            total_possible += total

        percent = int(round(float(total_correct) / total_possible * 100))

        with self.update_grades_cache(target_block_id) as cache:
            cache[unicode(student.id)] = (percent, {"name": student.profile.name})
            result = cache.values()

        return [entry for entry in result if entry[0] > 0]  # Return all non-zero grades
