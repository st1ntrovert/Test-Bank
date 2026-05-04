from playwright.sync_api import expect


def test_auth(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_login_locked_out_user(page):
    page.goto("https://saucedemo.com/")

    page.get_by_placeholder("Username").fill("locked_out_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    expect(page).to_have_url("https://www.saucedemo.com/")

    expect(page.locator("[data-test=\"error\"]")).to_be_visible()


def test_logout(auth_page):
    auth_page.locator("#react-burger-menu-btn").click()
    auth_page.locator("#logout_sidebar_link").click()

    expect(auth_page).to_have_url("https://www.saucedemo.com/")
    expect(auth_page.locator("#login-button")).to_be_visible()


def test_logout_visual_user(auth_page):
    expect(auth_page).to_have_url("https://www.saucedemo.com/inventory.html")

    auth_page.locator("#react-burger-menu-btn").click()
    auth_page.locator("#logout_sidebar_link").click()

    expect(auth_page).to_have_url("https://www.saucedemo.com/")
    expect(auth_page.locator("#login-button")).to_be_visible()
