"""
Common functionality for Leaderboard XBlocks
"""
from django.template import Template, Context

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment
from xblock.validation import ValidationMessage


@XBlock.needs("i18n")
class LeaderboardXBlock(XBlock):
    """
    Base class for leaderboard XBlocks
    """
    STUDENT_VIEW_TEMPLATE = "override_this.html"
    CSS_FILE = "static/css/leaderboard.css"

    # Fields:
    count = Integer(
        default=10, scope=Scope.settings,
        help="How many entries to display on the leaderboard."
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
        css = css or [self.CSS_FILE]
        javascript = javascript or []
        frag = Fragment(html.render(Context(context)))
        for sheet in css:
            frag.add_css(self.resource_string(sheet))
        for script in javascript:
            frag.add_javascript(self.resource_string(script))
        if initialize:
            frag.initialize_js(initialize)
        return frag

    def get_scores(self):
        """
        Override this method to return a list of up to self.count tuples of
        (score, entry) where score is an integer used to determine ranking
        (higher is better) and entry is a dictionary passed to the template.

        e.g. [(98, {name: "Jordan"}), (96, {name: "Jamie"}), (96, {name: "Tracy"})]

        Results do not have to be sorted nor limited to self.count.
        """
        raise NotImplementedError()

    def student_view(self, context=None):
        """
        The primary view of the leaderboard, shown to students when viewing courses.
        """
        # On first adding the block, the studio calls student_view instead of
        # author_view, which causes problems. Force call of the author view.
        if getattr(self.runtime, 'is_author_mode', False):
            return self.author_view()

        # Convert from scores to numbered ranks which can include ties:
        data = self.get_scores()
        data.sort(cmp=lambda x,y: y[0] - x[0])  # sort by score
        data = data[:self.count]
        leaders = []  # list of (rank, entry) where rank starts at 1
        for score, entry in data:
            entry["score"] = score
            if not leaders:  # First entry:
                leaders.append((1, entry))
            elif score == leaders[-1][1]["score"]:
                # Tied with previous entry:
                last_rank = leaders[-1][0]
                leaders.append((last_rank, entry))
            else:
                leaders.append((len(leaders)+1, entry))

        context = {
            'leaders': leaders,
            'display_name': self.display_name
        }
        return self.create_fragment(
            "static/html/{}".format(self.STUDENT_VIEW_TEMPLATE),
            context=context,
        )

    def validate(self):
        """
        Validates the state of this xblock
        """
        _ = self.runtime.service(self, "i18n").ugettext
        validation = super(LeaderboardXBlock, self).validate()
        if self.count <= 0:
            validation.add(
                ValidationMessage(
                    ValidationMessage.ERROR,
                    _(u"This component must be configured to display at least one entry.")
                )
            )
        return validation
