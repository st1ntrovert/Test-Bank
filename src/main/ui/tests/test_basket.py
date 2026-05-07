from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps


def test_add_item_and_check_in_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce").add_to_cart("Sauce Labs Backpack")
    basket_steps.open_cart().expect_item_in_cart("Sauce Labs Backpack")


def test_add_several_items_and_check_in_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce")
    catalog_steps.add_to_cart("Sauce Labs Fleece Jacket").add_to_cart("Sauce Labs Bolt T-Shirt")

    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Fleece Jacket").expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce").add_to_cart("Sauce Labs Fleece Jacket")
    basket_steps.open_cart().expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_steps.remove_item("Sauce Labs Fleece Jacket").expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_several_items_from_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce")
    catalog_steps.add_to_cart("Test.allTheThings() T-Shirt (Red)").add_to_cart("Sauce Labs Backpack")

    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Backpack").expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")
    basket_steps.remove_item("Test.allTheThings() T-Shirt (Red)").remove_item("Sauce Labs Backpack")
    basket_steps.expect_item_not_in_cart("Sauce Labs Backpack")
    basket_steps.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_full_end_to_end(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)
    checkout_steps = CheckoutSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce")
    catalog_steps.add_to_cart("Sauce Labs Fleece Jacket").add_to_cart("Sauce Labs Bolt T-Shirt")

    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Fleece Jacket").expect_item_in_cart("Sauce Labs Bolt T-Shirt")
    basket_steps.checkout()

    checkout_steps.enter_valid_data("Vlad", "The Vampire", "123")
    checkout_steps.continue_checkout().check_subtotal_is_correct().check_total_is_correct().finish_checkout()
    checkout_steps.check_checkout_is_complete()


def test_checkout_negative(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)
    checkout_steps = CheckoutSteps(page)

    catalog_steps.open().login("standard_user", "secret_sauce").add_to_cart("Sauce Labs Fleece Jacket")

    basket_steps.open_cart().expect_item_in_cart("Sauce Labs Fleece Jacket").checkout()

    checkout_steps.enter_invalid_data("Vlad", "The Vampire").continue_checkout()
    checkout_steps.check_error_message()
