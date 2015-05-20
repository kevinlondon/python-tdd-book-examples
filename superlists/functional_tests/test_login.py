import time
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
        self.wait_to_be_logged_in(USER_EMAIL)

        # Refreshing the page, she sees that it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(USER_EMAIL)

        # Terrified of this new feature, she reflexively clicks logout
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(USER_EMAIL)

        # The logged out status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(USER_EMAIL)
