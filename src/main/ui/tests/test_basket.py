from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage


def test_add_item_and_check_in_cart(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")
    catalog_page.add_to_cart("Sauce Labs Backpack")
    catalog_page.open_cart()

    basket_page.expect_item_in_cart("Sauce Labs Backpack")


def test_add_several_items_and_check_in_cart(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")
    catalog_page.add_to_cart("Sauce Labs Fleece Jacket")
    catalog_page.add_to_cart("Sauce Labs Bolt T-Shirt")

    catalog_page.open_cart()

    basket_page.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_page.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")
    catalog_page.add_to_cart("Sauce Labs Fleece Jacket")
    catalog_page.open_cart()
    basket_page.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_page.remove_item("Sauce Labs Fleece Jacket")
    basket_page.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_several_items_from_cart(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")

    catalog_page.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    catalog_page.add_to_cart("Sauce Labs Backpack")

    catalog_page.open_cart()

    basket_page.expect_item_in_cart("Sauce Labs Backpack")
    basket_page.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket_page.remove_item("Test.allTheThings() T-Shirt (Red)")
    basket_page.remove_item("Sauce Labs Backpack")

    basket_page.expect_item_not_in_cart("Sauce Labs Backpack")
    basket_page.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_full_end_to_end(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)
    checkout_page = CheckoutPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")

    catalog_page.add_to_cart("Sauce Labs Fleece Jacket")
    catalog_page.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog_page.open_cart()
    basket_page.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_page.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    basket_page.checkout()

    checkout_page.enter_valid_data("Vlad", "The Vampire", "123")
    checkout_page.continue_checkout()
    checkout_page.check_subtotal_is_correct()
    checkout_page.check_total_is_correct()
    checkout_page.finish_checkout()
    checkout_page.check_checkout_is_complete()


def test_checkout_negative(page):
    catalog_page = CatalogPage(page)
    basket_page = BasketPage(page)
    checkout_page = CheckoutPage(page)

    catalog_page.open()
    catalog_page.login("standard_user", "secret_sauce")

    catalog_page.add_to_cart("Sauce Labs Fleece Jacket")

    catalog_page.open_cart()
    basket_page.expect_item_in_cart("Sauce Labs Fleece Jacket")

    basket_page.checkout()

    checkout_page.enter_invalid_data("Vlad", "The Vampire")
    checkout_page.continue_checkout()
    checkout_page.check_error_message_to_be_visible()
