from ddt import ddt, unpack, data
from selenium.common.exceptions import NoSuchElementException
from xblockutils.base_test import SeleniumBaseTest
from scenarios import leaderboard_scenarios

@ddt
class LeaderboardTestCase(SeleniumBaseTest):
    module_name = __name__
    default_css_selector = 'div.forum_leaderboard_block'

    @unpack
    @data(*leaderboard_scenarios)
    def test_options(self, page, ul, links):
        self.go_to_page(page)
        line_items = [
            item for item in
            self.browser.find_elements_by_css_selector('ul.forum-leaderboard li')
        ]
        item_text = [item.text for item in line_items]
        self.assertEqual(
            item_text,
            ul,
        )
        # Selenium returns hrefs with fully qualified URLs but does not have an easy
        # way of grabbing the base URL.
        # We start with the full URL, something like http://localhost:8000/whatever

        # ['http:', '/', '/', 'localhost:8000', 'whatever']
        base_url = self.browser.current_url.split('/', 3)

        base_url.pop()
        # http://localhost:8000
        base_url = '/'.join(base_url)

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
