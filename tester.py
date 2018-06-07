#ScriptName : Login.py
#---------------------
from selenium import webdriver
from time import sleep

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException


def fill_text_xpath (location, text):
    element = driver.find_element_by_xpath(location)
    element.clear()
    element.send_keys(text)

def fill_text_by_id (location, text):
    element = driver.find_element_by_id(location)
    element.clear()
    element.send_keys(text)

def click_xpath(location):
    driver.find_element_by_xpath(location).click()

def click_id(location):
    driver.find_element_by_id(location).click()

def login_to_cp(cpurl, username, password):
    driver.get(cpurl)
    fill_text_xpath("//input[@name='user']", username)
    fill_text_xpath("//input[@name='password']", password)
    click_xpath("//button[@name='login']")
    driver.maximize_window()

def switch_to_billing():
    sleep(0.9)
    driver.switch_to.frame("topFrame")
    panelName = driver.find_element_by_id("to_bm") #find a element
    #print "Title is: " + panelName.get_attribute("title")
    print "Text is: " + panelName.text

    if panelName.text == "Billing":
        panelName.click()

def wait_for_element(time, location):
    print "nothing"

def create_customer(company_name, country_code, state, zip):
    win = driver.current_window_handle

    switch_to_billing()
    found = 10
#clean this!
    for i in range(0, 10):
        sleep(1)
        print "Tick"
        try:
            driver.switch_to.window(win)
            found = 1
            print "found window"
            driver.switch_to.frame("leftFrame")
            found = 2
            print "found leftFrame"
            break
        except NoSuchFrameException:
            found = 0
            continue

    #if found == 0:
    print "Found =", found

    click_id("click_my_end_user_accounts")

    driver.switch_to.window(win)
    driver.switch_to.frame("mainFrame")
    click_id("input_____customer_add")
    click_id("input___Save")
    fill_text_by_id("input___Company", company_name)
    fill_text_by_id("input___Address1", "Test st. 123")
    fill_text_by_id("input___City", "Testcity")
    fill_text_by_id("input___CountryCountryID", country_code)
    fill_text_by_id("input___StateState", state)
    fill_text_by_id("input___Zip", zip)
    fill_text_by_id("input___AdminFName", "Test")
    fill_text_by_id("input___AdminLName", "Customer")
    fill_text_by_id("input___AdminEmail", "test@customer.tld")
    fill_text_by_id("input___AdminPhCountryCode", "1")
    fill_text_by_id("input___AdminPhAreaCode", "123")
    fill_text_by_id("input___AdminPhNumber", "4567890")
    click_id("input___Save")

####################### MAIN ######################

#=====================variables=======================
cpurl = "https://di.psteam.int.zone/cp"
username = "admin"
password = "123qweASD"

# Open browser
#mydriver = webdriver.Firefox() - fails too often = finishes with exit code 0, but doesn't do anything
driver = webdriver.Chrome(executable_path="..\chromedriver.exe")
driver.implicitly_wait(10)

# Action 1
login_to_cp(cpurl, username, password)
create_customer("Test Customer PS1", "us", "AK", "12345")

