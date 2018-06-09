#ScriptName : Login.py
#---------------------
from selenium import webdriver
from time import sleep

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException

DELAY = 0.9


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
    sleep(DELAY)
    driver.switch_to.frame("topFrame")
    panelName = driver.find_element_by_id("to_bm") #find <a> element

    if panelName.text == "Billing":
        panelName.click()

def wait_for_element(time, location):
    print "nothing"

def create_customer(company_name, country_code, state, zip, additional_parameters, login, password):
    win = driver.current_window_handle

    switch_to_billing()
    #wait?
    driver.switch_to.window(win) # otherwise selenium doesn't see the frame
    driver.switch_to.frame("leftFrame")

    click_id("click_my_end_user_accounts")

    driver.switch_to.window(win) # otherwise selenium doesn't see the frame
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

    # Additional parameters
    additional_information_elements = driver.find_element_by_id('Additional Information').find_elements_by_tag_name("input")

    num_of_params = len(additional_parameters)
    num_of_fields = len(additional_information_elements)

    if num_of_params != num_of_fields:
        print "Customer creation error: Number of specified additional parameters(",num_of_params,") is not equal to the number of fields on the page(",num_of_fields,")"
        exit(1)
    else:
        for i in {0, num_of_params-1}:
            additional_information_elements[i].send_keys(additional_parameters[i])

    click_id("input___Next")

    fill_text_by_id("input___Login",login)
    fill_text_by_id("input___Password", password)

    click_id("input___SP_ViewAccount")

    print "Customer creation result:"
    print driver.find_element_by_id("opresult_id").find_element_by_class_name("msg-content").text

####################### MAIN ######################

#=====================variables=======================
#cpurl = "https://di.psteam.int.zone/cp"
cpurl = "https://oap.psteam.int.zone/cp"
username = "admin"
#password = "123qweASD"
password = "oap-psteam"

# Open browser
#mydriver = webdriver.Firefox() - fails too often = finishes with exit code 0, but doesn't do anything
driver = webdriver.Chrome(executable_path="..\chromedriver.exe")
driver.implicitly_wait(10)

# Action 1
login_to_cp(cpurl, username, password)
additional_params = ["111111111"]
create_customer("Test Customer PS2", "us", "AK", "12345", additional_params, "testps2", "123qweASD")

