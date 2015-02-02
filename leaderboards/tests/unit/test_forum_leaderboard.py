import ddt
from django.test import TestCase as DjangoTestCase
from leaderboards.forum_leaderboard import ForumLeaderboardXBlock
from .common import LeadboardBlockTest, LeaderboardWorkbenchTest


class ForumLeaderboardTest(LeadboardBlockTest):
    """
    Test the forum leaderboard XBlock
    """
    BLOCK_CLASS = ForumLeaderboardXBlock


@ddt.ddt
class ForumLeaderboardWorkbenchTest(LeaderboardWorkbenchTest, DjangoTestCase):
    """
    Test the forum leaderboard XBlock in the workbench
    (i.e. with a real runtime)
    """
    @ddt.data(
        '<forum_leaderboard discussion_id="empty_discussion"/>',
        '<forum_leaderboard discussion_id="unvoted_threads"/>',
    )
    def test_empty_discussion(self, scenario_xml):
        """
        Test that with an empty discussion or unvoted threads,
        we don't see a list of discussions but rather a message.
        """
        resp = self.load_scenario(scenario_xml)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("There are not yet any discussions with a score.", resp.content)
        self.assertNotIn("<ol", resp.content)

    def test_author_view(self):
        """
        Test the author view.
        """
        resp = self.load_scenario(
            """
            <forum_leaderboard discussion_id="12345" display_name="Test DN" count="7" />
            """,
            view_name="author_view"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("<h2>Test DN</h2>", resp.content)
        self.assertIn("up to 7 top threads from Discussion ID <code>12345</code>", resp.content)
