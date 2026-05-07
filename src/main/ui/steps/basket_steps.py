import allure
from playwright.sync_api import Page

from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Выходим из корзины назад в каталог")
    def go_back_to_catalog(self):
        self.basket.go_back_to_catalog()
        return self

    @allure.step("Переходим к оформлению заказа")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Удаляем товар из корзины: {item_name}")
    def remove_item(self, item_name: str):
        self.basket.remove_item(item_name)
        return self

    @allure.step("Ожидаем в корзине товар: {item_name}")
    def expect_item_in_cart(self, item_name: str):
        self.basket.expect_item_in_cart(item_name)
        return self

    @allure.step("Ожидаем что в корзине нет товара: {item_name}")
    def expect_item_not_in_cart(self, item_name: str):
        self.basket.expect_item_not_in_cart(item_name)
        return self

    @allure.step("Получаем имена товаров")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step("Получаем цены товаров")
    def get_item_prices(self) -> list[float]:
        return self.basket.get_item_prices()

    @allure.step("Получаем итоговую цену товаров")
    def get_item_total_price(self) -> float:
        return self.basket.get_items_total_price()
