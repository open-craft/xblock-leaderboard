from ddt import ddt, unpack, data
from selenium.common.exceptions import NoSuchElementException
from urlparse import urlparse
from xblockutils.base_test import SeleniumBaseTest
from .forum_scenarios import forum_scenarios

@ddt
class LeaderboardTestCase(SeleniumBaseTest):
    module_name = __name__
    default_css_selector = 'div.forum_leaderboard_block'

    @unpack
    @data(*forum_scenarios)
    def test_options(self, page, links, ol=None, message=None):
        self.go_to_page(page)
        if ol:
            line_items = [
                item for item in
                self.browser.find_elements_by_css_selector('.forum-leaderboard li')
            ]
            item_text = [item.text for item in line_items]
            self.assertEqual(item_text, ol)

            parsed_url = urlparse(self.browser.current_url)
            base_url = "{}://{}".format(parsed_url.scheme, parsed_url.netloc)

            page_links = []
            for item in line_items:
                try:
                    page_links.append(item.find_element_by_css_selector('a').get_attribute('href'))
                except NoSuchElementException:
                    page_links.append(None)

            links = [(base_url + link) if link else None for link in links]
            self.assertEqual(
                page_links,
                links,
            )
        if message:
            msg_text = self.browser.find_elements_by_css_selector('.forum_leaderboard_block p')[0].text
            self.assertEqual(msg_text, message)
