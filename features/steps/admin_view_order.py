from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is logged in1')
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

@when (u'the user clicks view detail button')
def step_impl(context):
    pass

@then (u'the user can see the details')
def step_impl(context):
    pass