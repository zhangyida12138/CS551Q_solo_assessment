from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given (u'the user is on Home page2')
def step_impl(context):
    context.browser.get(context.home_page_url)

@when (u'the user choose a product and click View Product')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "View Product")
    login_link.click()

@when (u'the user click add to cart button')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "add to cart")
    login_link.click()

@when (u'the user clicks the Process to Checkout button')
def step_impl(context):
    login_link = context.browser.find_element(By.LINK_TEXT, "Checkout")
    login_link.click()

@then (u'the user can see the alter')
def step_impl(context):
    pass