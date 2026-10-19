# Saucedemo — bug automation (Python + Playwright + pytest)

UI tests for https://www.saucedemo.com written with the **Page Object Model**.
Each test checks one bug found with `problem_user`:

- with `standard_user` all tests **PASS** (the app works correctly);
- with `problem_user` all tests **FAIL** (the bugs are reproduced).

Bug reports: [bug_reports/BUG_REPORTS.md](bug_reports/BUG_REPORTS.md)

## How to run

Requirements: Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

Run the tests:

```bash
pytest                         # standard_user (default) -> 7 passed
pytest --user problem_user     # problem_user            -> 7 failed
```

Useful options:

```bash
pytest --headed --slowmo 500                 # watch the browser
pytest --browser firefox                     # other browser
pytest tests/test_checkout.py                # one file
pytest -k sort --user problem_user           # tests by name
```

On failure a screenshot is saved to `test-results/`.

## Structure

```
.
├── pages/                    # Page Objects: all locators live here
│   ├── base_page.py          # BasePage: page, open(), data-test helper, header (cart badge/link)
│   ├── login_page.py         # LoginPage.login() -> InventoryPage
│   ├── inventory_page.py     # products list: names, prices, images, sort, add to cart, open product
│   ├── product_page.py       # product details
│   ├── cart_page.py          # cart: items, checkout()
│   └── checkout_page.py      # checkout "Your Information" form
├── tests/                    # tests use only page object methods, no locators
│   ├── test_inventory.py     # BUG-001 … BUG-004
│   └── test_checkout.py      # BUG-005
├── bug_reports/
│   ├── BUG_REPORTS.md
│   └── screenshots/
├── conftest.py               # --user option, logged-in `inventory_page` fixture
├── pytest.ini                # base_url, screenshots on failure
└── requirements.txt
```

## Design decisions

- **BasePage** keeps what every page shares: the Playwright `page`, `open()`, the
  `by_test_id()` helper and the header (cart badge and link). Every page object inherits from it.
- **`wait_until_loaded()`** — the site is a SPA: the URL changes before the content is rendered.
  Each page waits for its own content, so tests never read an empty list and pass by mistake.
- **Locators only in page objects.** They use the `data-test` attributes — they are stable
  and do not depend on CSS or text.
- **Page methods return the next page** (`login()` → `InventoryPage`, `open_cart()` → `CartPage`,
  `checkout()` → `CheckoutInfoPage`), so a test reads like a user scenario.
- **Page objects return data, tests assert.** Page objects have no `assert`; tests decide what is correct.
- **Expected values are calculated, not hard-coded** (e.g. `sorted(prices)`), so tests do not break if the catalog changes.
- **The user is a command-line option** (`--user`), so the same tests run against both users without changing code.

## Tests ↔ bugs

| Test | Bug | standard_user | problem_user |
|---|---|---|---|
| `test_each_product_has_its_own_image` | BUG-001 Same image for all products | PASS | FAIL |
| `test_sort_by_name_z_to_a` | BUG-002 Sorting does not work | PASS | FAIL |
| `test_sort_by_price[low-to-high / high-to-low]` | BUG-002 Sorting does not work | PASS | FAIL |
| `test_add_every_product_to_cart` | BUG-003 "Add to cart" broken for 3 products | PASS | FAIL |
| `test_product_link_opens_matching_details` | BUG-004 Wrong product opens | PASS | FAIL |
| `test_checkout_info_form_accepts_customer_data` | BUG-005 Last Name overwrites First Name | PASS | FAIL |
