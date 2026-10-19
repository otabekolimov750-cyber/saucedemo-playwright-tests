from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = self.by_test_id("username")
        self.password_input = self.by_test_id("password")
        self.login_button = self.by_test_id("login-button")
        self.error_message = self.by_test_id("error")

    def login(self, username: str, password: str) -> InventoryPage:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_url(f"**{InventoryPage.PATH}")
        return InventoryPage(self.page).wait_until_loaded()
