from django.test import TestCase as DjangoTestCase
from leaderboards.grade_leaderboard import GradeLeaderboardXBlock
from .common import LeadboardBlockTest, LeaderboardWorkbenchTest


class GradeLeaderboardTest(LeadboardBlockTest):
    """
    Test the grade leaderboard XBlock
    """
    BLOCK_CLASS = GradeLeaderboardXBlock

    def test_validate_graded_target_id(self):
        """
        Test that validation is working.
        """
        block = self.new_block()
        validation = block.validate()
        self.expect_validation_message(validation, u"A graded activity must be chosen as a basis for the leaderboard.")

        block.graded_target_id = "section17"
        self.runtime.get_block = lambda key: None
        validation = block.validate()
        self.expect_validation_message(validation, u"The graded activity specified could not be found.")


class GradeLeaderboardWorkbenchTest(LeaderboardWorkbenchTest, DjangoTestCase):
    """
    Test the grade leaderboard XBlock in the workbench
    (i.e. with a real runtime)
    """
    def test_invalid_grade_target(self):
        """
        Test that students see a friendly error message if the graded_target_id
        is not set to a valid block.
        """
        resp = self.load_scenario('<grade_leaderboard graded_target_id="invalid"/>')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("An error occurred. Unable to display leaderboard.", resp.content)
        self.assertNotIn("<ol", resp.content)

    def test_with_mock_grades(self):
        """
        When run in the workbench with a valid graded_target_id,
        the block should display random grades.
        The randomization is deterministic so we can test against it.
        """
        resp = self.load_scenario(
            """
             <vertical_demo>
                <problem_demo>
                    <html_demo><p>What is 3+2?</p></html_demo>
                    <textinput_demo name="sum_input" input_type="int" />
                    <equality_demo name="sum_checker" left="./sum_input/@student_input" right="5" />
                </problem_demo>
                <grade_leaderboard graded_target_id="test-scenario.problem_demo.d0.u0"/>
             </vertical_demo>
             """
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("<ol", resp.content)
