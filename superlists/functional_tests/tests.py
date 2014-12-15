from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert row_text in [row.text for row in rows]

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edit heard about a new online todo app. She goes to check out the homepage.
        self.browser.get(self.live_server_url)

        # She notices page title and header mentions to-do lists
        assert 'To-Do' in self.browser.title

        # She is invited to enter a to-do item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

        # She types "Buy peacock feathers" into a text box.
        buy_peacock_text = "Buy peacock feathers"
        inputbox.send_keys(buy_peacock_text)

        # When she hits enter, she is taken to a new URL and
        # the page updates and lists "1: Buy peacock feathers."
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: {0}".format(buy_peacock_text))

        # There is still a text box that invites her to add another item.
        # She enters "Use peacock feathers to make a fly."
        inputbox = self.browser.find_element_by_id('id_new_item')
        make_fly_text = "Use peacock feathers to make a fly."
        inputbox.send_keys(make_fly_text)
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on her list.
        self.check_for_row_in_list_table("1: {0}".format(buy_peacock_text))
        self.check_for_row_in_list_table("2: {0}".format(make_fly_text))

        # Now a new user, Francis, comes along to the site.
        # (We use a new browser session to make sure that none of the info)
        # (from Edith's session is leaking through cookies, etc.)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page and there is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        assert buy_peacock_text not in page_text
        assert make_fly_text not in page_text

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        assert francis_list_url != edith_list_url

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        assert buy_peacock_text not in page_text
        assert "Buy milk" in page_text

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Edith goes to the home page.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She noticed the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely cnetered there.
        inputbox.send_keys("testing\n")
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
