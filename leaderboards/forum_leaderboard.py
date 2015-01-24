"""
Forum Leaderboard XBlock

Shows the top threads for a given discussion ID by vote.
"""
from .leaderboard import LeaderboardXBlock

from xblock.core import XBlock
from xblock.fields import Scope, String

try:
    import lms.lib.comment_client as cc
    DEV_MODE = False
except ImportError:
    # We're in the SDK, probably.
    import dummy_cc as cc
    DEV_MODE = True


class ForumLeaderboardXBlock(LeaderboardXBlock):
    STUDENT_VIEW_TEMPLATE = "forum_leaderboard.html"

    display_name = String(
        default="Forum Leaderboard", scope=Scope.settings,
        help="Display name for this block."
    )
    discussion_id = String(
        default="", scope=Scope.settings,
        help="The ID of the inline discussion to tally leading threads for.",
    )

    def get_course(self):
        """
        Gets the course, or returns a dummy value if not in an edx-platform
        environment.
        """
        if DEV_MODE:
            return 'dummy_key'
        else:
            return self.location.course_key

    def get_thread_url(self, course, discussion_id, thread_id):
        """
        Due to package structure, we can't easily import the standard
        reverse_course_url function, which is the right way to do this.
        """
        return "/courses/{0}/discussion/forum/{1}/threads/{2}".format(course, discussion_id, thread_id)

    def get_scores(self):
        """
        Compute the top threads and return them.
        """
        if not self.discussion_id:
            raise RuntimeError("No discussion ID configured.")
        course = self.get_course()
        threads = cc.Thread.search({
            'course_id': unicode(course), 'commentable_id': self.discussion_id,
            'sort_key': 'votes', 'per_page': self.count - 1
        })[0]

        scored_threads = []
        for thread in threads:
            score = thread['votes']['point']  # Might be 0
            if score:
                thread['url'] = self.get_thread_url(course, self.discussion_id, thread['id'])
                scored_threads.append((score, thread))
        return scored_threads

    def author_view(self, context=None):
        return self.create_fragment(
            "static/html/forum_leaderboard_studio.html",
            context={
                'discussion_id': self.discussion_id,
                'display_name': self.display_name,
                'count': self.count,
            },
        )

    def studio_view(self, context=None):
        return self.create_fragment(
            "static/html/forum_leaderboard_studio_edit.html",
            context={'discussion_id': self.discussion_id, 'count': self.count},
            javascript=["static/js/src/forum_leaderboard_studio.js"],
            initialize='ForumLeaderboardStudioXBlock'
        )

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        result = {'success': True, 'errors': []}
        try:
            count = int(data.get('count', LeaderboardXBlock.count.default))
            if not count > 0:
                raise ValueError
        except ValueError:
            result['success'] = False
            result['errors'].append("'count' must be an integer and greater than 0.")

        discussion_id = data.get('discussion_id', '').strip()
        if not isinstance(discussion_id, basestring):
            result['success'] = False
            result['errors'].append("'discussion_id' must be a string.")

        if result['success']:
            self.count = count
            self.discussion_id = discussion_id
        return result

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Leaderboard with many threads",
             """
             <vertical_demo>
                <forum_leaderboard discussion_id="many_threads"/>
             </vertical_demo>
             """),
            ("Leaderboard with unvoted threads",
             """
             <vertical_demo>
                 <forum_leaderboard discussion_id="unvoted_threads"/>
             </vertical_demo>
             """),
            ("Leaderboard with varied voting",
             """
             <vertical_demo>
                 <forum_leaderboard discussion_id="varied_voting" count="6"/>
             </vertical_demo>
             """),
            ("Leaderboard with empty discussion",
             """
             <vertical_demo>
                 <forum_leaderboard discussion_id="empty_discussion"/>
             </vertical_demo>
             """)
        ]
