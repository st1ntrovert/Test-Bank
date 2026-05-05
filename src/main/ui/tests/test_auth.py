from playwright.sync_api import expect
from src.main.ui.pages.login_page import LoginPage


def test_auth(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_login_locked_out_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")

    expect(page).to_have_url(LoginPage.URL)

    error_text = login_page.get_error_text()
    assert "locked out" in error_text


def test_logout(auth_page):
    page = auth_page

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_visible()


def test_logout_visual_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()

    expect(page).to_have_url(LoginPage.URL)
    expect(login_page.login_button).to_be_visible()
