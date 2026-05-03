from playwright.sync_api import expect


def test_count_items(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    products = page.locator(".inventory_item")
    assert products.count() == 6


def test_sorted_by_name(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("az")

    names = page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names), "Товары не отсортированы по имени A-Z"


def test_sort_by_name_reversed(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("za")

    names = page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"

def test_sort_by_price(page):
    page.goto("https://saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("lohi")

    prices_text = page.locator(".inventory_item_price").all_text_contents()

    prices = [float(p.replace("$", "")) for p in prices_text]

    assert prices == sorted(prices), "Цены не отсортированы от меньшей к большей"

    sort_select.select_option("hilo")

    prices_text = page.locator(".inventory_item_price").all_text_contents()

    prices = [float(p.replace("$", "")) for p in prices_text]


    assert prices == sorted(prices, reverse=True), "Цены не отсортированы от большей к меньшей"


def test_add_to_cart(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()

    expect(page.locator(".shopping_cart_badge")).to_contain_text("1")

    page.locator("[data-test=\"shopping-cart-link\"]").click()

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")
