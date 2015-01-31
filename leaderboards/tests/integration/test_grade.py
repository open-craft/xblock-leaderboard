from workbench.test.selenium_test import SeleniumTest
from xblock.core import XBlock
from ..unit.common import Generic


class UnscoredGeneric(Generic):
    """
    Generic XBlock with has_score = False
    """
    has_score = False


class GradeLeaderboardTestCase(SeleniumTest):
    """
    Integration tests for the grade leaderboard
    """
    module_name = __name__
    default_css_selector = 'div.forum_leaderboard_block'

    @XBlock.register_temp_plugin(Generic)
    @XBlock.register_temp_plugin(UnscoredGeneric, "generic-no-score")
    def test_studio_view(self):
        """
        Test the studio edit view for grade leaderboards.
        """
        # We need <generic> XBlock in order to do this test, as we need a
        # hierarchy and the normal SDK demo blocks don't support studio_view.
        # However, <generic> is not usually registered, so if we put it in the
        # xml folder it will cause issues. Instead, we create the scenario now:
        import workbench.urls  # Trigger scenario load. pylint: disable=unused-variable
        from workbench.scenarios import SCENARIOS, add_xml_scenario
        SCENARIOS.clear()
        add_xml_scenario(
            "test", "Test Scenario",
            """
            <generic>
                <generic display_name="Problem1" />
                <generic display_name="Problem2" />
                <generic-no-score display_name="has_score False container">
                    <generic display_name="Problem3"/>
                </generic-no-score>
                <generic-no-score display_name="has_score False leaf"/>
                <grade_leaderboard count="93"/>
             </generic>
            """
        )
        scenario_url = self.live_server_url + '/scenario/test/studio_view/'
        self.browser.get(scenario_url)

        count_field = self.browser.find_element_by_css_selector('input[id=count]')
        self.assertEqual(count_field.get_attribute('value'), "93")

        select = self.browser.find_element_by_css_selector('select#graded_target_id')
        option_elements = select.find_elements_by_css_selector('option')
        options = {}
        for opt in option_elements:
            desc = opt.text.strip()
            value = opt.get_attribute("value")
            enabled = not opt.get_attribute("disabled")
            options[desc] = (value, enabled)

        for display_name in ("Problem1", "Problem2", "Problem3", "has_score False container"):
            self.assertIn(display_name, options)
            self.assertTrue(options[display_name][1])  # Should be enabled
        for display_name in ("has_score False leaf", "Grade Leaderboard (This leaderboard)"):
            self.assertIn(display_name, options)
            # The current block and any blocks that don't contain a has_score problem
            # should not be selectable:
            self.assertFalse(options[display_name][1])

        # Would love to test the save button here but because of the way
        # we are using $ajax({global: false}) to better integrate with studio,
        # we run into issues with CSRF protection in workbench and the hacks
        # needed to work around it get too complex and ugly.
        # For now we will just test the save method in unit testing.
