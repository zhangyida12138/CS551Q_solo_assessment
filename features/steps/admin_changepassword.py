from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is logged in 4')
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

@when (u'the user clicks customer list button2')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Customer List")
    login_link.click()

@when (u'the user enter a new password')
def step_impl(context):
    password_input = context.browser.find_element(By.NAME, "password")
    password_input.send_keys('zhangwei123')

@when (u'the user clicks update button')
def step_impl(context):
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@then (u'the user changed it6')
def step_impl(context):
    pass