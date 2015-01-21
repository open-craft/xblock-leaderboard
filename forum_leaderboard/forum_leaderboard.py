"""
Forum Leaderboard XBlock

Shows the top threads for a given discussion ID by vote.
"""
from django.template import Template, Context

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

try:
    import lms.lib.comment_client as cc
    DEV_MODE = False
except ImportError:
    # We're in the SDK, probably.
    import dummy_cc as cc
    DEV_MODE = True


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

        course = self.get_course()
        threads = cc.Thread.search({
            'course_id': unicode(course), 'commentable_id': self.discussion_id,
            'sort_key': 'votes', 'per_page': self.count
        })[0]

        # Score might be 0.
        threads = [thread for thread in threads if thread['votes']['point']]
        for thread in threads:
            thread['url'] = self.get_thread_url(
                course, self.discussion_id, thread['id'])

        context = {
            'threads': threads,
            'display_name': self.display_name
        }
        return self.create_fragment(
            "static/html/forum_leaderboard.html", context=context,
            css=["static/css/forum_leaderboard.css"],
        )

    def author_view(self, context=None):
        return self.create_fragment(
            "static/html/forum_leaderboard_studio.html",
            context={
                'discussion_id': self.discussion_id,
                'display_name': self.display_name,
                'count': self.count,
            },
            css=["static/css/forum_leaderboard.css"]
        )

    def studio_view(self, context=None):
        return self.create_fragment(
            "static/html/forum_leaderboard_studio_edit.html",
            context={'discussion_id': self.discussion_id, 'count': self.count},
            css=["static/css/forum_leaderboard.css"],
            javascript=["static/js/src/forum_leaderboard_studio.js"],
            initialize='ForumLeaderboardStudioXBlock'
        )

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        result = {'success': True, 'errors': []}
        try:
            count = int(data.get('count', ForumLeaderboardXBlock.count.default))
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
