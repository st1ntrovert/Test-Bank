from playwright.sync_api import Page

class BasketPage:
    URL = 'https://www.saucedemo.com/cart.html'

    def __init__(self, page: Page):
        self.page = page
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.cart_item = page.locator('.cart_item')