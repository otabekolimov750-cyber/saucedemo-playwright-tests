from pages.base_page import BasePage
from pages.checkout_page import CheckoutInfoPage


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.item_names = self.by_test_id("inventory-item-name")
        self.checkout_button = self.by_test_id("checkout")

    def product_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def checkout(self) -> CheckoutInfoPage:
        self.checkout_button.click()
        return CheckoutInfoPage(self.page)
