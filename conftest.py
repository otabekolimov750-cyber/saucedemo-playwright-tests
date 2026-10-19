import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

USERS = ["standard_user", "problem_user"]
PASSWORD = "secret_sauce"  # public demo password shown on the saucedemo login page


def pytest_addoption(parser):
    parser.addoption(
        "--user",
        default="standard_user",
        choices=USERS,
        help="Saucedemo user to log in with (default: standard_user)",
    )


def pytest_report_header(config):
    return f"saucedemo user: {config.getoption('--user')}"


@pytest.fixture(scope="session")
def user(request) -> str:
    return request.config.getoption("--user")


@pytest.fixture
def inventory_page(page, user) -> InventoryPage:
    """Logged-in user on the products page."""
    return LoginPage(page).open().login(user, PASSWORD)
