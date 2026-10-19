# Bug reports — saucedemo.com (`problem_user`)

**Common environment for all reports**

| Field | Value |
|---|---|
| Application | Swag Labs — https://www.saucedemo.com |
| User | `problem_user` / `secret_sauce` |
| Browser | Chromium 156 (Playwright 1.64) |
| OS | Windows 11 |
| Date | 2026-10-19 |
| Control check | All bugs **do not** reproduce with `standard_user` |

Severity scale: Blocker > Critical > Major > Minor. Priority: High / Medium / Low.

| ID | Title | Severity | Priority | Automated test |
|---|---|---|---|---|
| BUG-001 | All products show the same placeholder image | Major | Medium | `test_each_product_has_its_own_image` |
| BUG-002 | Sorting of products does not work | Major | Medium | `test_sort_by_name_z_to_a`, `test_sort_by_price` |
| BUG-003 | "Add to cart" does nothing for 3 of 6 products | Critical | High | `test_add_every_product_to_cart` |
| BUG-004 | Product name opens the details of a different product | Critical | High | `test_product_link_opens_matching_details` |
| BUG-005 | Checkout: typing Last Name overwrites First Name, checkout is blocked | Blocker | High | `test_checkout_info_form_accepts_customer_data` |

---

## BUG-005 · Checkout: text typed in "Last Name" goes into "First Name", checkout cannot be completed

- **Severity:** Blocker — the user cannot place any order
- **Priority:** High
- **Component:** Checkout → "Your Information" (`/checkout-step-one.html`)

**Preconditions:** logged in as `problem_user`, at least one product in the cart.

**Steps to reproduce**
1. Click the cart icon → click **Checkout**.
2. Type `John` in **First Name**.
3. Type `Doe` in **Last Name**.
4. Type `12345` in **Zip/Postal Code**.
5. Click **Continue**.

**Expected result**
- First Name = `John`, Last Name = `Doe`, Zip = `12345`.
- The user goes to "Checkout: Overview" (`/checkout-step-two.html`).

**Actual result**
- After step 3 **First Name** becomes `Doe`, **Last Name** stays empty (each character typed into Last Name replaces the First Name value).
- After step 5 the error `Error: Last Name is required` is shown and the user stays on step one. The order cannot be completed.

**Attachment:** [screenshots/BUG-005-checkout.png](screenshots/BUG-005-checkout.png)

---

## BUG-003 · "Add to cart" does nothing for some products on the products page

- **Severity:** Critical — the products cannot be bought from the catalog
- **Priority:** High
- **Component:** Products page (`/inventory.html`)

**Preconditions:** logged in as `problem_user`, cart is empty.

**Steps to reproduce**
1. On the Products page click **Add to cart** for each of the 6 products.

**Expected result**
- Every button changes to **Remove**.
- The cart badge shows `6`, the cart contains all 6 products.

**Actual result**
- For **Sauce Labs Bolt T-Shirt**, **Sauce Labs Fleece Jacket** and **Test.allTheThings() T-Shirt (Red)** the button stays "Add to cart" and nothing is added.
- The cart badge shows `3`.

**Attachment:** [screenshots/BUG-003-add-to-cart.png](screenshots/BUG-003-add-to-cart.png)

---

## BUG-004 · Clicking a product name opens the details page of another product

- **Severity:** Critical — the user sees (and may buy) a different product than the one they chose
- **Priority:** High
- **Component:** Products page → Product details (`/inventory-item.html?id=N`)

**Preconditions:** logged in as `problem_user`.

**Steps to reproduce**
1. On the Products page click the name **Sauce Labs Backpack**.

**Expected result:** details page of **Sauce Labs Backpack** opens (`?id=4`).

**Actual result:** details page of **Sauce Labs Fleece Jacket** opens (`?id=5`).

The same happens for every product (the link points to `id + 1`):

| Clicked | Opened |
|---|---|
| Sauce Labs Backpack | Sauce Labs Fleece Jacket |
| Sauce Labs Bike Light | Sauce Labs Bolt T-Shirt |
| Sauce Labs Bolt T-Shirt | Sauce Labs Onesie |
| Sauce Labs Fleece Jacket | "ITEM NOT FOUND" |
| Sauce Labs Onesie | Test.allTheThings() T-Shirt (Red) |
| Test.allTheThings() T-Shirt (Red) | Sauce Labs Backpack |

**Attachment:** [screenshots/BUG-004-wrong-product.png](screenshots/BUG-004-wrong-product.png)

---

## BUG-002 · Sorting products does not change the order

- **Severity:** Major — the feature does not work, a workaround exists (scroll manually)
- **Priority:** Medium
- **Component:** Products page → sort dropdown

**Preconditions:** logged in as `problem_user`.

**Steps to reproduce**
1. On the Products page open the sort dropdown.
2. Select **Name (Z to A)**.
3. Repeat with **Price (low to high)** and **Price (high to low)**.

**Expected result**
- Z to A: `Test.allTheThings() T-Shirt (Red)` first, `Sauce Labs Backpack` last.
- Low to high: `$7.99, $9.99, $15.99, $15.99, $29.99, $49.99`.
- High to low: the reverse.
- The dropdown shows the selected option.

**Actual result**
- The order of products does not change for any option (prices stay `$29.99, $9.99, $15.99, $49.99, $7.99, $15.99`).
- The dropdown jumps back to **Name (A to Z)**.

**Attachment:** [screenshots/BUG-002-sort.png](screenshots/BUG-002-sort.png)

---

## BUG-001 · All products on the products page show the same image

- **Severity:** Major — the user cannot recognise products by picture
- **Priority:** Medium
- **Component:** Products page (`/inventory.html`)

**Preconditions:** none.

**Steps to reproduce**
1. Log in as `problem_user`.
2. Look at the product images on the Products page.

**Expected result:** each product shows its own photo (backpack, bike light, t-shirt, …).

**Actual result:** all 6 products show the same dog picture. Every `<img>` has the same `src`: `/assets/sl-404-*.jpg` (a "404" placeholder), so the real images are not loaded.

**Attachment:** [screenshots/BUG-001-images.png](screenshots/BUG-001-images.png)
