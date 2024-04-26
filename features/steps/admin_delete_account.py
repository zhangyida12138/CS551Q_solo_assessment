from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is logged in 3')
def step_impl(context):
    context.browser.get(context.home_page_url)
    login_link = context.browser.find_element(By.LINK_TEXT, "Login")
    login_link.click()
    email_input = context.browser.find_element(By.NAME, "email")
    email_input.send_keys('admin@test.com')
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('zhangwei123')
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@when (u'the user clicks customer list button')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Customer List")
    login_link.click()

@when (u'the user clicks delete button3')
def step_impl(context):
    pass
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='delete']")
    login_button.click()

@then (u'the user deleted it 1')
def step_impl(context):
    pass