from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is on Home page3')
def step_impl(context):
    context.browser.get(context.home_page_url)

@when (u'the user enter a product name')
def step_impl(context):
    search_input = context.browser.find_element(By.LINK_TEXT, "Search here")
    search_input.send_keys('test123456789')

@when (u'the user click the search button')
def step_impl(context):
    login_button = context.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    login_button.click()

@then (u'the user can see the products')
def step_impl(context):
    pass