from pages.checkout_page import CheckoutOverviewPage

PRODUCT = "Sauce Labs Backpack"
CUSTOMER = {"first_name": "John", "last_name": "Doe", "postal_code": "12345"}


def test_checkout_info_form_accepts_customer_data(inventory_page):
    """BUG-005: the "Your Information" form must keep the entered values and let the user continue."""
    checkout = inventory_page.add_to_cart(PRODUCT).open_cart().checkout()

    checkout.fill_info(**CUSTOMER)
    assert checkout.form_values() == CUSTOMER

    checkout.continue_checkout()
    assert checkout.error_text() is None
    assert checkout.url.endswith(CheckoutOverviewPage.PATH)
