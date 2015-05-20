import time
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest

USER_EMAIL = 'edith@mockmyid.com'


class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries =  60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return

            retries -= 1
            time.sleep(.5)

        self.fail("Could not find window.")

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(USER_EMAIL, navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(USER_EMAIL, navbar.text)

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("id_login").click()

        # A personal login box appears
        self.switch_to_new_window("Mozilla Persona")

        # Edit logins in with her email address
        # # Use mockmyid.com for the test email
        self.browser.find_element_by_id("authentication_email").send_keys(USER_EMAIL)
        self.browser.find_element_by_tag_name("button").click()

        # The persona window closes
        self.switch_to_new_window("To-Do")

        # She can see that she is logged in
        self.wait_to_be_logged_in()

        # Refreshing the page, she sees that it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # Terrified of this new feature, she reflexively clicks logout
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # The logged out status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out()
