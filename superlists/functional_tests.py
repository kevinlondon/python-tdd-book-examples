from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edit heard about a new online todo app. She goes to check out the homepage.
        self.browser.get("http://localhost:8000")

        # She notices page title and header mentions to-do lists
        assert 'To-Do' in self.browser.title
        self.fail("tbd")

        # She is invited to enter a to-do item.
        #
        # She types "Buy peacock feathers" into a text box.
        #
        # When she hits enter, the page updates and lists "1: Buy peacock feathers."
        #
        # There is still a text box that invites her to add another item.
        # She enters "Use peacock feathers to make a fly."
        #
        # The page updates again and shows both items on her list.
        #
        # Edith wonders if the site will remember her list. She sees a unique URL
        # for the todo items she has enters and some associated text explaining it.
        #
        # She visits the unique url specified.
        #
        # Satisfied, she goes back to sleep.

if __name__ == "__main__":
    unittest.main(warnings="ignore")
