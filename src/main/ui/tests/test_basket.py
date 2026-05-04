from playwright.sync_api import expect


def test_add_item_and_check_in_cart(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    auth_page.locator(".shopping_cart_link").click()

    item_name = auth_page.locator('[data-test="inventory-item-name"]')
    assert item_name.inner_text() == "Sauce Labs Backpack"


def test_add_several_items_and_check_in_cart(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    auth_page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()

    auth_page.locator(".shopping_cart_link").click()

    jacket_name = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    t_shirt_name = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Bolt T-Shirt")

    assert jacket_name.inner_text() == "Sauce Labs Fleece Jacket"
    assert t_shirt_name.inner_text() == "Sauce Labs Bolt T-Shirt"


def test_remove_item_from_cart(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()

    auth_page.locator(".shopping_cart_link").click()

    jacket = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    expect(jacket).to_be_visible()

    auth_page.locator('[data-test="remove-sauce-labs-fleece-jacket"]').click()
    expect(jacket).not_to_be_visible()


def test_remove_several_items_from_cart(auth_page):
    auth_page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()
    auth_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    auth_page.locator(".shopping_cart_link").click()

    t_shirt = auth_page.locator('[data-test="inventory-item-name"]', has_text="Test.allTheThings() T-Shirt (Red)")
    backpack = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Backpack")
    expect(t_shirt).to_be_visible()
    expect(backpack).to_be_visible()

    auth_page.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]').click()
    expect(t_shirt).not_to_be_visible()
    auth_page.locator('[data-test="remove-sauce-labs-backpack"]').click()
    expect(backpack).not_to_be_visible()


def test_full_end_to_end(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    auth_page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()

    auth_page.locator(".shopping_cart_link").click()

    jacket = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    t_shirt = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Bolt T-Shirt")
    expect(jacket).to_be_visible()
    expect(t_shirt).to_be_visible()

    prices_text = auth_page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace('$', '')) for p in prices_text]
    expected_total = sum(prices)

    auth_page.locator('[data-test="checkout"]').click()

    auth_page.get_by_placeholder("First Name").fill("Harry")
    auth_page.get_by_placeholder("Last Name").fill("Potter")
    auth_page.get_by_placeholder("Zip/Postal Code").fill("H0GW4RT5")

    auth_page.locator('[data-test="continue"]').click()

    expect(auth_page.locator('[data-test="subtotal-label"]')).to_have_text(f'Item total: ${round(expected_total, 2)}')
    tax_text = auth_page.locator('[data-test="tax-label"]').inner_text()
    tax = float(tax_text.split("$")[1])
    expect(auth_page.locator('[data-test="total-label"]')).to_have_text(f'Total: ${round(expected_total + tax, 2)}')

    auth_page.locator('[data-test="finish"]').click()

    expect(auth_page.locator('[data-test="complete-header"]')).to_be_visible()


def test_checkout_negative(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()

    auth_page.locator(".shopping_cart_link").click()

    jacket = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    expect(jacket).to_be_visible()

    auth_page.locator('[data-test="checkout"]').click()

    auth_page.get_by_placeholder("First Name").fill("Harry")
    auth_page.get_by_placeholder("Last Name").fill("Potter")

    auth_page.locator('[data-test="continue"]').click()

    error_message = auth_page.locator('[data-test="error"]')
    expect(error_message).to_have_text('Error: Postal Code is required')
