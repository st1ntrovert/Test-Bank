from playwright.sync_api import Page, expect

from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils.constants import Urls


class CheckoutPage(BasePage):
    URL = Urls.CHECKOUT

    def __init__(self, page: Page):
        super().__init__(page)
        # step one
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error_message = page.locator('[data-test="error"]')

        # step two
        self.finish_button = page.locator('[data-test="finish"]')
        self.cart_list = page.locator('[data-test="cart-list"]')
        self.subtotal_price = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total_price = page.locator('[data-test="total-label"]')

        # complete
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')

    def open(self):
        self.page.goto(self.URL)

    def enter_valid_data(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def enter_invalid_data(self, first_name, last_name):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        expect(self.postal_code).to_be_empty()

    def cancel_checkout(self):
        self.cancel_button.click()

    def continue_checkout(self):
        self.continue_button.click()

    def check_error_message_to_be_visible(self):
        expect(self.error_message).to_be_visible()

    def get_items_subtotal(self) -> float:
        subtotal_text = self.subtotal_price.inner_text()
        return float(subtotal_text.split('$')[1])

    def get_tax(self) -> float:
        tax_text = self.tax.inner_text()
        return float(tax_text.split('$')[1])

    def get_total_price(self) -> float:
        total_text = self.total_price.inner_text()
        return float(total_text.split('$')[1])

    def finish_checkout(self):
        self.finish_button.click()

    def get_sum_of_cart_items(self) -> float:
        prices = self.page.locator(".cart_item .inventory_item_price").all_text_contents()
        return round(sum(float(p.strip().lstrip('$')) for p in prices), 2)

    def check_subtotal_is_correct(self):
        assert self.get_sum_of_cart_items() == self.get_items_subtotal()

    def check_total_is_correct(self):
        assert self.get_total_price() == self.get_items_subtotal() + self.get_tax()

    def check_checkout_is_complete(self):
        expect(self.complete_header).to_be_visible()
        expect(self.complete_text).to_be_visible()
