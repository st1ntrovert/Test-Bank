import allure
from playwright.sync_api import Page

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step("Открываем страницу чекаута")
    def open(self):
        self.checkout.open()
        return self

    @allure.step("Вводим корректные данные на первом этапе")
    def enter_valid_data(self, first_name, last_name, postal_code):
        self.checkout.enter_valid_data(first_name, last_name, postal_code)
        return self

    @allure.step("Вводим некорректные данные на первом этапе")
    def enter_invalid_data(self, first_name, last_name):
        self.checkout.enter_invalid_data(first_name, last_name)
        return self

    @allure.step("Отменяем чекаут")
    def cancel_checkout(self):
        self.checkout.cancel_checkout()
        return self

    @allure.step("Продолжаем чекаут (второй этап)")
    def continue_checkout(self):
        self.checkout.continue_checkout()
        return self

    @allure.step("Проверяем что появилось сообщение об ошибке")
    def check_error_message(self):
        self.checkout.check_error_message_to_be_visible()
        return self

    @allure.step("Получаем общую цену товаров в чекауте")
    def get_items_subtotal(self) -> float:
        return self.checkout.get_items_subtotal()

    @allure.step("Получаем сумму налога")
    def get_tax(self) -> float:
        return self.checkout.get_tax()

    @allure.step("Получаем финальную цену")
    def get_total_price(self) -> float:
        return self.checkout.get_total_price()

    @allure.step("Завершаем оформление заказа")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Считаем общую сумму товаров в корзине")
    def get_sum_of_cart_items(self) -> float:
        return self.checkout.get_sum_of_cart_items()

    @allure.step("Проверяем корректность суммы до налогов")
    def check_subtotal_is_correct(self):
        self.checkout.check_subtotal_is_correct()
        return self

    @allure.step("Проверяем корректность финальной цены")
    def check_total_is_correct(self):
        self.checkout.check_total_is_correct()
        return self

    @allure.step("Проверяем сообщение об успешном оформлении заказа")
    def check_checkout_is_complete(self):
        self.checkout.check_checkout_is_complete()
        return self
