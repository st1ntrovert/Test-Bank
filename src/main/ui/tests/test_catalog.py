from playwright.sync_api import expect


def test_count_catalog(auth_page):
    products = auth_page.locator(".inventory_item")
    assert products.count() == 6


def test_sorted_by_name(auth_page):
    sort_select = auth_page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("az")

    names = auth_page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names), "Товары не отсортированы по имени A-Z"


def test_sort_by_name_z_to_a(auth_page):
    sort_select = auth_page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("za")

    names = auth_page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"


def test_sort_by_price(auth_page):
    page = auth_page
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


def test_add_to_cart(auth_page):
    auth_page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()

    expect(auth_page.locator(".shopping_cart_badge")).to_contain_text("1")

    auth_page.locator("[data-test=\"shopping-cart-link\"]").click()

    expect(auth_page).to_have_url("https://www.saucedemo.com/cart.html")

    expect(auth_page.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")


def test_add_to_cart_sauce_labs_onesie(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    add_button = product_card.locator("button")

    add_button.click()
    expect(add_button).to_have_text("Remove")

    expect(auth_page.locator(".shopping_cart_badge")).to_contain_text("1")

    add_button.click()
    expect(add_button).to_have_text("Add to cart")
    expect(auth_page.locator(".shopping_cart_badge")).to_be_hidden()


def test_product_details_onesie(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")

    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()

    product_card.locator('[data-test="inventory-item-name"]').click()

    detail_name = auth_page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = auth_page.locator('[data-test="inventory-item-price"]').inner_text()

    assert product_name == detail_name, "Имя товара не совпадает"
    assert product_price == detail_price, "Цена товара не совпадает"


def test_product_details_fleece_jacket(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Fleece Jacket")

    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()

    product_card.locator('[data-test="inventory-item-name"]').click()

    detail_name = auth_page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = auth_page.locator('[data-test="inventory-item-price"]').inner_text()

    assert product_name == detail_name, "Имя товара не совпадает"
    assert product_price == detail_price, "Цена товара не совпадает"


def test_remove_item_from_cart(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Test.allTheThings() T-Shirt (Red)")
    product_button = product_card.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    product_button.click()

    remove_button = product_card.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]')
    assert remove_button.is_visible(), "Кнопка Remove не появилась"

    remove_button.click()

    assert product_button.is_visible(), "Кнопка Add to cart не вернулась после удаления товара"


def test_remove_onesie_from_cart(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    product_button = auth_page.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    product_button.click()

    remove_button = product_card.locator('[data-test="remove-sauce-labs-onesie"]')
    assert remove_button.is_visible()

    remove_button.click()

    assert product_button.is_visible()
