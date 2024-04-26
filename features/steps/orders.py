from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is logged in and brought something')
def step_impl(context):
    context.browser.get(context.home_page_url)
    login_link = context.browser.find_element(By.LINK_TEXT, "Login")
    login_link.click()
    email_input = context.browser.find_element(By.NAME, "email")
    email_input.send_keys('test2@test.com')
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('test123456789')
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@when (u'the user click Orders button')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Orders")
    login_link.click()

@then (u'the user can see the orders')
def step_impl(context):
    pass