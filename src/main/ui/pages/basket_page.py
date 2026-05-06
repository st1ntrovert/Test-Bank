from playwright.sync_api import Page, expect


class BasketPage:
    URL = 'https://saucedemo.com/cart.html'

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator('.shopping_cart_link')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.cart_items = page.locator('.cart_item')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.error_message = page.locator('[data-test="error"]')

    def open_cart(self):
        self.cart_link.click()

    def go_back_to_catalog(self):
        self.continue_shopping_button.click()

    def checkout(self):
        self.checkout_button.click()

    def remove_item(self, item_name: str):
        card = self.cart_items.filter(has_text=item_name)
        button = card.locator('button')
        button.click()

    def expect_item_in_cart(self, item_name: str):
        card = self.cart_items.filter(has_text=item_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, item_name: str):
        card = self.cart_items.filter(has_text=item_name)
        expect(card).not_to_be_visible()

    def get_item_names(self) -> list[str]:
        return self.cart_items.locator('.inventory_item_name').all_text_contents()

    def get_item_prices(self) -> list[float]:
        prices_text = self.cart_items.locator('.inventory_item_price').all_text_contents()
        return [float(p.replace('$', "")) for p in prices_text]

    def get_items_total_price(self) -> float:
        return sum(self.get_item_prices())
