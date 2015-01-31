# pylint: disable=unexpected-keyword-arg, no-member, no-value-for-parameter
from django.test import TestCase as DjangoTestCase
import json
from leaderboards.grade_leaderboard import GradeLeaderboardXBlock
from mock import Mock
from xblock.core import XBlock
from .common import Generic, LeadboardBlockTest, LeaderboardWorkbenchTest


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

    def test_studio_submit(self):
        """
        Test studio_submit() since it's difficult to integrate into our
        integration testing at the moment.
        """
        block = self.new_block()
        block.count = 5

        # Invalid count:
        data = json.dumps({'count': -3, 'graded_target_id': None})
        response = block.studio_submit(request=Mock(method='POST', body=data))
        self.assertEqual(response.status_code, 400)
        response_error = json.loads(response.body)["error"]
        self.assertIn("'count' must be an integer and greater than 0.", response_error)
        self.assertEqual(block.count, 5)

        # Valid count:
        data = json.dumps({'count': 11, 'graded_target_id': None})
        response = block.studio_submit(request=Mock(method='POST', body=data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(block.count, 11)


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

    @XBlock.register_temp_plugin(Generic)
    def test_author_view(self):
        """
        When run in the studio with a valid graded_target_id,
        the block should display a summary of its configuration.
        """
        resp = self.load_scenario(
            """
            <generic>
                <generic display_name="Problem Alpha" />
                <grade_leaderboard display_name="Leaderboard Beta" count="17"
                    graded_target_id="test-scenario.generic.d1.u0"/>
            </generic>
            """,
            view_name="author_view"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("<h2>Leaderboard Beta</h2>", resp.content)
        self.assertIn(
            'will show a leaderboard of up to 17 top students based on their grades in "Problem Alpha"',
            resp.content
        )
