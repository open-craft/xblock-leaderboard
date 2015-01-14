"""
Forum Leaderboard XBlock

Shows the top threads for a given discussion ID by vote.
"""
from django.template import Template, Context

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

import lms.lib.comment_client as cc


class ForumLeaderboardXBlock(XBlock):
    display_name = String(
        default="Forum Leaderboard", scope=Scope.settings,
        help="Display name for this block."
    )
    # Studio view not yet written. To test, set the default here,
    # or manually set in Mongo.
    discussion_id = String(
        default="", scope=Scope.settings,
        help="The ID of the inline discussion to tally leading threads for.",
    )
    count = Integer(
        default=10, scope=Scope.settings,
        help="How many threads to display."
    )

    def resource_string(self, path):
        """
        Handy helper for getting resources from our kit.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def create_fragment(self, html, context=None, css=None, javascript=None, initialize=None):
        """
        Create an XBlock, given an HTML resource string and an optional context, list of CSS
        resource strings, list of JavaScript resource strings, and initialization function name.
        """
        html = Template(self.resource_string(html))
        context = context or {}
        css = css or []
        javascript = javascript or []
        frag = Fragment(html.render(Context(context)))
        for sheet in css:
            frag.add_css(self.resource_string(sheet))
        for script in javascript:
            frag.add_javascript(self.resource_string(script))
        if initialize:
            frag.initialize_js(initialize)
        return frag

    def student_view(self, context=None):
        """
        The primary view of the ForumLeaderboardXBlock, shown to students
        when viewing courses.
        """
        # On first adding the block, the studio calls student_view instead of
        # author_view, but the studio can't access the forum, so this would
        # crash. Force call of the author view.
        if getattr(self.runtime, 'is_author_mode', False):
            return self.author_view()
        course = self.location.course_key
        threads = cc.Thread.search({
            'course_id': unicode(course), 'commentable_id': self.discussion_id,
            'sort_key': 'votes', 'per_page': self.count
        })[0]

        context = {
            'threads': threads,
            'display_name': self.display_name
        }
        return self.create_fragment(
            "static/html/forum_leaderboard.html", context=context,
            css=["static/css/forum_leaderboard.css"],
            javascript=["static/js/src/forum_leaderboard.js"],
            initialize='ForumLeaderboardXBlock')

    def author_view(self, context=None):
        return self.create_fragment(
            "static/html/forum_leaderboard_studio.html",
            context={
                'discussion_id': self.discussion_id,
                'display_name': self.display_name
            },
            css=["static/css/forum_leaderboard.css"])

    # TO-DO: Create a Dummy thread service for Workbench tests, and
    # create scenarios for it.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ForumLeaderboardXBlock",
             """<vertical_demo>
                <forum_leaderboard/>
                </vertical_demo>
             """),
        ]
