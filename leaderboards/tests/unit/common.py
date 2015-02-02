import ddt
from django.test import Client
from mock import Mock
import unittest
from xblock.core import XBlock, String, Scope
from xblock.fragment import Fragment
from xblock.runtime import DictKeyValueStore, KvsFieldData
from xblock.test.tools import TestRuntime


@ddt.ddt
class LeadboardBlockTest(unittest.TestCase):
    """
    Base class for testing a leaderboard block.
    """
    BLOCK_CLASS = None  # Override

    def __init__(self, *args, **kwargs):
        super(LeadboardBlockTest, self).__init__(*args, **kwargs)
        # Only run tests on this if we've been subclassed
        # and the subclass has defined BLOCK_CLASS
        if self.BLOCK_CLASS is None:
            self.run = lambda self, *args, **kwargs: None

    def setUp(self):
        field_data = KvsFieldData(DictKeyValueStore())
        self.runtime = TestRuntime(services={'field-data': field_data})

    def new_block(self):
        """
        Instantiate an instance of BLOCK_CLASS
        using the test runtime.
        """
        return self.BLOCK_CLASS(runtime=self.runtime, scope_ids=Mock())  # pylint: disable=not-callable

    def expect_validation_message(self, validation, msg):
        """
        Ensure that the XBlock validation result contains at least the message
        msg
        """
        self.assertGreaterEqual(len(validation.messages), 1)
        messages = [v.text for v in validation.messages]
        self.assertIn(msg, messages)

    @ddt.data(0, -3)
    def test_bad_count_setting(self, bad_count):
        """
        Test that the block's validation checks the .count field.
        """
        block = self.new_block()
        block.count = bad_count
        validation = block.validate()
        self.expect_validation_message(validation, u"This component must be configured to display at least one entry.")

    def test_get_scores_failure(self):
        """
        Ensure that if the get_scores() method of the subclass
        doesn't work, errors are trapped and a friendly message
        is shown to students.
        """
        block = self.new_block()
        # We assume that get_scores() is going to fail because we haven't configured the block.
        fragment = block.student_view()
        self.assertIn("An error occurred. Unable to display leaderboard.", fragment.content)


class LeaderboardWorkbenchTest(object):
    """
    Mixin to test the forum leaderboard XBlock in the workbench
    (i.e. with a real runtime)
    """
    def setUp(self):
        super(LeaderboardWorkbenchTest, self).setUp()
        self.client = Client()

    def load_scenario(self, xml, view_name=None, student_id='tester1'):
        """
        Load a scenario into the workbench and fetch it using self.client
        """
        import workbench.urls  # Trigger scenario load. pylint: disable=unused-variable
        from workbench.scenarios import SCENARIOS, add_xml_scenario
        SCENARIOS.clear()
        add_xml_scenario("test", "Test Scenario", xml)
        scenario_url = '/scenario/test/'
        if view_name:
            scenario_url += view_name + '/'
        scenario_url += '?student_id=' + student_id
        return self.client.get(scenario_url)


class Generic(XBlock):
    """
    A generic XBlock helpful for tests.
    Use via the @XBlock.register_temp_plugin() decorator
    """
    has_children = True
    has_score = True
    content = String(scope=Scope.content, default=u'')
    display_name = String(scope=Scope.content, default=u'')

    def fallback_view(self, view_name, context=None):
        result = Fragment()
        child_frags = self.runtime.render_children(self, context=context)
        result.add_frags_resources(child_frags)
        result.content = self.content
        result.add_content(self.runtime.render_template("vertical.html", children=child_frags))
        return result
