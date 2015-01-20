"""
Grade Leaderboard XBlock

Shows the top students for a given block (and any children)
"""
from .leaderboard import LeaderboardXBlock

import random

from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Scope, String, Reference
from xblock.validation import ValidationMessage


def normalize_id(key):
    """
    Helper method to normalize a key to avoid issues where some keys have version/branch and others don't.
    e.g. self.scope_ids.usage_id != self.runtime.get_block(self.scope_ids.usage_id).scope_ids.usage_id
    """
    if hasattr(key, "for_branch"):
        key = key.for_branch(None)
    if hasattr(key, "for_version"):
        key = key.for_version(None)
    return key


@XBlock.needs("i18n")
class GradeLeaderboardXBlock(LeaderboardXBlock):
    STUDENT_VIEW_TEMPLATE = "grade_leaderboard.html"

    display_name = String(
        default="Grade Leaderboard", scope=Scope.settings,
        help="Display name for this block."
    )
    graded_target_id = Reference(
        scope=Scope.settings,
        help="Which graded component to use as the basis of the leaderboard.",
    )

    def validate(self):
        """
        Validates the state of this xblock
        """
        _ = self.runtime.service(self, "i18n").ugettext
        validation = super(GradeLeaderboardXBlock, self).validate()
        if not self.graded_target_id:
            validation.add(
                ValidationMessage(
                    ValidationMessage.WARNING,
                    _(u"A graded activity must be chosen as a basis for the leaderboard.")
                )
            )
        elif not self.runtime.get_block(self.graded_target_id):
            validation.add(
                ValidationMessage(
                    ValidationMessage.ERROR,
                    _(u"The graded activity specified could not be found.")
                )
            )
        return validation

    def get_scores(self):
        """
        Compute the top students based on grade and return them.
        """
        students = []
        for i in xrange(0, self.count):
            students.append((random.randint(0,100), {"name": random.choice(["Jamie", "Alex", "Sam", "Jordan", "Taylor"])}))
        return students

    def author_view(self, context=None):
        graded_target_name = self.graded_target_id
        graded_target = self.runtime.get_block(self.graded_target_id) if self.graded_target_id else None
        if graded_target:
            graded_target_name = getattr(graded_target, "display_name", graded_target_name)
        return self.create_fragment(
            "static/html/grade_leaderboard_studio.html",
            context={
                'graded_target_id': self.graded_target_id,
                'graded_target_name': graded_target_name,
                'display_name': self.display_name,
                'count': self.count,
            },
        )

    def studio_view(self, context=None):
        """
        Display the form for changing this XBlock's settings.
        """
        own_id = normalize_id(self.scope_ids.usage_id)  # Normalization needed in edX Studio :-/

        flat_block_tree = []
        def build_tree(block, ancestors):
            """
            Build up a tree of information about the XBlocks descending from root_block
            """
            block_name = getattr(block, "display_name")
            if not block_name:
                block_type = block.runtime.id_reader.get_block_type(block.scope_ids.def_id)
                block_name = "{} ({})".format(block_type, block.scope_ids.usage_id)
            eligible = getattr(block, "has_score", False)
            if eligible:
                # If this block is graded, we mark all its ancestors as gradeable too
                if not ancestors[-1]["eligible"]:
                    for ancestor in ancestors:
                        ancestor["eligible"] = True
            block_id = normalize_id(block.scope_ids.usage_id)
            new_entry = {
                "depth": len(ancestors),
                "id": block_id,
                "name": block_name,
                "eligible": eligible,
                "is_this": block_id == own_id,
            }
            flat_block_tree.append(new_entry)
            if block.has_children and not getattr(block, "has_dynamic_children", lambda: False)():
                for child_id in block.children:
                    build_tree(block.runtime.get_block(child_id), ancestors=(ancestors + [new_entry]))

        # Determine the root block and build the tree:
        root_block = self
        while True:
            parent = root_block.get_parent()
            if not parent:
                break
            root_block = parent
        build_tree(root_block, [])

        return self.create_fragment(
            "static/html/grade_leaderboard_studio_edit.html",
            context={
                'count': self.count,
                'graded_target_id': self.graded_target_id,
                'block_tree': flat_block_tree,
            },
            javascript=["static/js/src/grade_leaderboard_studio.js"],
            initialize='GradeLeaderboardStudioXBlock'
        )

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        try:
            count = int(data.get('count', LeaderboardXBlock.count.default))
            if not count > 0:
                raise ValueError
        except ValueError:
            raise JsonHandlerError(400, "'count' must be an integer and greater than 0.")

        graded_target_id = data.get('graded_target_id')  # We cannot validate this ourselves
        if not graded_target_id:
            graded_target_id = None  # Avoid trying to set to an empty string - won't work
        self.count = count
        self.graded_target_id = graded_target_id
        return {}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Grade Leaderboard (problem and linked leaderboard)",
             """
             <vertical_demo>
                <problem_demo name="problem1">
                    <html_demo><p>What is $a+$b?</p></html_demo>
                    <textinput_demo name="sum_input" input_type="int" />
                    <equality_demo name="sum_checker" left="./sum_input/@student_input" right="$c" />
                    <script>
                        import random
                        a = random.randint(2, 5)
                        b = random.randint(1, 4)
                        c = a + b
                    </script>
                </problem_demo>
                <grade_leaderboard graded_target_id="./problem1"/>
             </vertical_demo>
             """),
            ("Grade Leaderboard (invalid block configuration)",
             """
             <vertical_demo>
                <grade_leaderboard graded_target_id="./problem2"/>
             </vertical_demo>
             """),
        ]
