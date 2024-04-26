from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is on Home page')
def step_impl(context):
    context.browser.get(context.home_page_url)

@when (u'the user click Login')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Login")
    login_link.click()

@when (u'the user input email')
def step_impl(context):
    email_input = context.browser.find_element(By.NAME, "email")
    email_input.send_keys('test2@test.com')

@when (u'the user input password')
def step_impl(context):
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('test123456789')

@when (u'the user clicks the Login button')
def step_impl(context):
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@then (u'the user can see logout')
def step_impl(context):
    try:
        WebDriverWait(context.browser, 3).until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
        assert context.browser.find_element(By.LINK_TEXT, "Home").is_displayed()
    except TimeoutException:
        raise AssertionError("Logout link not found after logging in.")