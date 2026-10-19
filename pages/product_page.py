from pages.base_page import BasePage


class ProductPage(BasePage):
    """Single product details (/inventory-item.html?id=N)."""

    PATH = "/inventory-item.html"

    def __init__(self, page):
        super().__init__(page)
        self.name = self.by_test_id("inventory-item-name")
        self.price = self.by_test_id("inventory-item-price")
        self.back_button = self.by_test_id("back-to-products")

    def wait_until_loaded(self):
        # the URL changes before the products list is replaced, so wait for an
        # element that exists only on the details page
        self.back_button.wait_for()
        return self

    def product_name(self) -> str:
        return self.name.inner_text()

    def back_to_products(self):
        from pages.inventory_page import InventoryPage  # local import avoids a circular import

        self.back_button.click()
        return InventoryPage(self.page)
