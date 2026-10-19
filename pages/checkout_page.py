from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Checkout step one: "Your Information" form."""

    PATH = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = self.by_test_id("firstName")
        self.last_name_input = self.by_test_id("lastName")
        self.postal_code_input = self.by_test_id("postalCode")
        self.continue_button = self.by_test_id("continue")
        self.error_message = self.by_test_id("error")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    def form_values(self) -> dict[str, str]:
        return {
            "first_name": self.first_name_input.input_value(),
            "last_name": self.last_name_input.input_value(),
            "postal_code": self.postal_code_input.input_value(),
        }

    def continue_checkout(self):
        self.continue_button.click()
        return self

    def error_text(self) -> str | None:
        if self.error_message.count() == 0:
            return None
        return self.error_message.inner_text()


class CheckoutOverviewPage(BasePage):
    """Checkout step two: order overview."""

    PATH = "/checkout-step-two.html"
