import time
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest


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
            lambda b: b.find_element_by_id(element_id)
        )

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("id_login").click()

        # A personal login box appears
        self.switch_to_new_window("Mozilla Persona")

        # Edit logins in with her email address
        # # Use mockmyid.com for the test email
        self.browser.find_element_by_id("authentication_email").send_keys("edit@mockmyid.com")
        self.browser.find_element_by_tag_name("button").click()

        # The persona window closes
        self.switch_to_new_window("To-Do")

        # She can see that she is logged in
        self.wait_for_element_with_id("id_logout")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn("edit@mockmyid.com", navbar.text)
