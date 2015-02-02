"""
Code to retrieve student grades for various runtimes.
"""
from contextlib import contextmanager


class GradeSource(object):
    """
    Base class for grade source classes
    """
    SOURCE_NAME = None  # Override this and set to a short string

    def __init__(self, host_block):
        """
        Initialize this grade source to retrieve grades from various xblocks
        for display in host_block.
        """
        self.host_block = host_block

    def is_supported(self):
        """
        Does self.host_block.runtime support this type of grade source?
        """
        raise NotImplementedError

    def get_grades(self, target_block_id, limit_hint=None):
        """
        Get the total grade for all students that have started/attempted
        'target_block_id' and all descendant blocks.
        Returns [(percentage, student info), ...]

        If limit_hint is set, this grade source may limit its return to only
        include the top [limit_hint] students. If it always returns all students,
        that is fine too.
        """
        raise NotImplementedError

    @contextmanager
    def update_grades_cache(self, target_block_id):
        """
        Context manager for updating the grades_cache field with the grade of target_block_id

        This is a [potentially misguided] attempt to reduce the chance that two students
        will view this block at the same time, resulting in one of them overwriting the
        other's updates to self.grades_cache. Whether or not this makes a difference is TBD.
        """
        source_key = u"{}:{}".format(self.SOURCE_NAME, unicode(target_block_id))
        try:
            grades_cache = self.host_block._field_data.get(self.host_block, "grades_cache")
        except KeyError:
            grades_cache = {}
        value = grades_cache.get(source_key, {})
        yield value
        grades_cache[source_key] = value
        self.host_block._field_data.set(self.host_block, "grades_cache", grades_cache)

from .edx import EdxLmsGradeSource
from .mock import MockGradeSource
