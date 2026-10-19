import pytest

from pages.inventory_page import InventoryPage


def test_each_product_has_its_own_image(inventory_page):
    """BUG-001: every product must show its own picture."""
    sources = inventory_page.product_image_sources()

    assert sources, "No product images found"
    assert len(set(sources)) == len(sources), f"Products share the same image: {sources}"


def test_sort_by_name_z_to_a(inventory_page):
    """BUG-002: sorting Name (Z to A) must reorder the products."""
    names = inventory_page.sort_by(InventoryPage.SORT_NAME_Z_A).product_names()

    assert names == sorted(names, reverse=True)


@pytest.mark.parametrize(
    "sort_option, descending",
    [
        (InventoryPage.SORT_PRICE_LOW_HIGH, False),
        (InventoryPage.SORT_PRICE_HIGH_LOW, True),
    ],
    ids=["low-to-high", "high-to-low"],
)
def test_sort_by_price(inventory_page, sort_option, descending):
    """BUG-002: sorting by price must reorder the products."""
    prices = inventory_page.sort_by(sort_option).product_prices()

    assert prices == sorted(prices, reverse=descending)


def test_add_every_product_to_cart(inventory_page):
    """BUG-003: "Add to cart" must work for every product."""
    products = inventory_page.product_names()

    for name in products:
        inventory_page.add_to_cart(name)

    not_added = [name for name in products if inventory_page.button_text(name) != "Remove"]
    assert not_added == [], f"'Add to cart' did nothing for: {not_added}"
    assert inventory_page.cart_count() == len(products)
    assert sorted(inventory_page.open_cart().product_names()) == sorted(products)


def test_product_link_opens_matching_details(inventory_page):
    """BUG-004: clicking a product name must open the details of that product."""
    mismatches = {}

    for name in inventory_page.product_names():
        opened = inventory_page.open_product(name).product_name()
        if opened != name:
            mismatches[name] = opened
        inventory_page.open()

    assert mismatches == {}, f"Clicked -> opened: {mismatches}"
