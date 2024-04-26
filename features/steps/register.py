from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is on Home page1')
def step_impl(context):
    context.browser.get(context.home_page_url)

@when (u'the user click Register')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Register")
    login_link.click()

@when (u'the user inputs email')
def step_impl(context):
    email_input = context.browser.find_element(By.NAME, "email")
    email_input.send_keys('test3@test.com')

@when (u'the user sets password')
def step_impl(context):
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('test123456789')

@when (u'the user input password agian')
def step_impl(context):
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('test123456789')

@when (u'the user clicks the Register button')
def step_impl(context):
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@then (u'the user can logout')
def step_impl(context):
    pass