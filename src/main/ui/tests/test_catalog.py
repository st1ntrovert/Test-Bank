from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage


def test_count_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    assert catalog.count_cards() == 6


def test_sorted_by_name(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.sort_items('az')
    assert catalog.get_product_names() == sorted(catalog.get_product_names())

    catalog.sort_items('za')
    assert catalog.get_product_names() == sorted(catalog.get_product_names(), reverse=True)


def test_sort_by_price(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    catalog.sort_items('lohi')
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices())
    catalog.sort_items('hilo')
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices(), reverse=True)


def test_add_to_cart(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    button = catalog.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1


def test_add_to_cart_sauce_labs_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    button = catalog.add_to_cart("Sauce Labs Onesie")
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1

    button = catalog.remove_from_cart("Sauce Labs Onesie")
    expect(button).to_have_text("Add to cart")
    expect(catalog.cart_badge).not_to_be_visible()


def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price


def test_product_details_fleece_jacket(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_cart(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    add_button = catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    expect(add_button).to_have_text("Remove")

    remove_button = catalog.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
    expect(remove_button).to_have_text("Add to cart")
