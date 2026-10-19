from playwright.sync_api import Locator, Page


class BasePage:
    """Common parent for all page objects.

    Holds the Playwright page, navigation helpers and the header elements
    that are shared by every page after login (cart icon and badge).
    """

    PATH = "/"

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = self.by_test_id("shopping-cart-link")
        self.cart_badge = self.by_test_id("shopping-cart-badge")

    def by_test_id(self, test_id: str) -> Locator:
        """Saucedemo marks elements with the data-test attribute."""
        return self.page.locator(f"[data-test='{test_id}']")

    def open(self):
        self.page.goto(self.PATH)
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        """Pages override this to wait for their own content to be rendered."""
        return self

    @property
    def url(self) -> str:
        return self.page.url

    def cart_count(self) -> int:
        """Number shown on the cart badge (0 when the badge is hidden)."""
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self):
        from pages.cart_page import CartPage  # local import avoids a circular import

        self.cart_link.click()
        return CartPage(self.page)
