from pages.base_page import BasePage
from pages.product_page import ProductPage


class InventoryPage(BasePage):
    """Products list (/inventory.html)."""

    PATH = "/inventory.html"

    # value attribute of <option> in the sort dropdown
    SORT_NAME_A_Z = "az"
    SORT_NAME_Z_A = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    def __init__(self, page):
        super().__init__(page)
        self.items = self.by_test_id("inventory-item")
        self.item_names = self.by_test_id("inventory-item-name")
        self.item_prices = self.by_test_id("inventory-item-price")
        self.item_images = self.items.locator("img")
        self.sort_dropdown = self.by_test_id("product-sort-container")

    def wait_until_loaded(self):
        # the URL changes before the products are rendered; without this
        # wait the lists below can be empty
        self.items.first.wait_for()
        return self

    def _item(self, name: str):
        return self.items.filter(has=self.item_names.get_by_text(name, exact=True))

    # --- reading data ---
    def product_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def product_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def product_image_sources(self) -> list[str]:
        return [img.get_attribute("src") for img in self.item_images.all()]

    def button_text(self, name: str) -> str:
        # product links also have role="button", so take the real <button> element
        return self._item(name).locator("button").inner_text()

    # --- actions ---
    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)
        return self

    def add_to_cart(self, name: str):
        self._item(name).get_by_role("button", name="Add to cart").click()
        return self

    def open_product(self, name: str) -> ProductPage:
        self.item_names.get_by_text(name, exact=True).click()
        self.page.wait_for_url(f"**{ProductPage.PATH}*")
        return ProductPage(self.page).wait_until_loaded()
