from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.utils.constants import Urls


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    assert page.url == Urls.CATALOG


def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")
    assert page.url == Urls.BASE
    error_text = steps.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0
    catalog_steps.logout()
    assert page.url == Urls.BASE


def test_logout_visual_user(page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)

    login_steps.open_login_page().login("visual_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0

    catalog_steps.logout()
    assert page.url == Urls.BASE
