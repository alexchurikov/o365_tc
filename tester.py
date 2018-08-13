#ScriptName : Login.py
#---------------------
from selenium import webdriver
from time import sleep
import sys

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

def switch_panel(needed_panel_name): # "Billing" or "Operations"
    sleep(DELAY)
    driver.switch_to.frame("topFrame")
    panelName = driver.find_element_by_id("to_bm") #find <a> element

    if panelName.text == needed_panel_name:
        panelName.click()

def create_customer(company_name, country_code, state, zip, additional_parameters, login, password):
    print "Creating customer with name: ", company_name

    win = driver.current_window_handle

    switch_panel("Billing")

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
        message = "Customer creation error: Number of specified additional parameters(",num_of_params,") is not equal to the number of fields on the page(",num_of_fields,")"
        raise message
    else:
        for i in {0, num_of_params-1}:
            additional_information_elements[i].send_keys(additional_parameters[i])

    click_id("input___Next")

    fill_text_by_id("input___Login",login)
    fill_text_by_id("input___Password", password)

    click_id("input___SP_ViewAccount")

    result = driver.find_element_by_id("opresult_id").find_element_by_class_name("msg-content").text
    print "Customer creation result:"
    print result

    return result

def find_name_in_popup(field_element_id, value):
    fill_text_by_id(field_element_id, value)
    click_id("_browse_search")  # search

    #checking each found element for total match
    i = 1
    while True:
        try:
            line = driver.find_element_by_id("vel_t1_" + str(i))
        except NoSuchElementException as ex:
            print ex

            if i == 1:  # search found no objects
                #print "Nothing found"
                return None


        print "Something found, but ..."

        if i == 3:
            break
        i += 1





def place_order(customerID, planName, subdomain):
    print "Placing order for customer #" + customerID + ", purchasing plan '" + planName + "'"

    win = driver.current_window_handle

    switch_panel("Billing")

    driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
    driver.switch_to.frame("leftFrame")

    click_id("click_orders")

    driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
    driver.switch_to.frame("mainFrame")
    click_id("input___add")

    # filling fields
    fill_text_by_id("input___AccountAccountID",customerID)
    click_id("input___refPlan")

    # switch to popup here, as in Dasha
    driver.switch_to.window(driver.window_handles[1])
    assert (driver.title == "Service Plans"), "Could not find Service Plans popup."

    find_name_in_popup("filter_name", planName)

    #driver.switch_to().window(win)  # switch back to parent window
    #driver.switch_to.frame("mainFrame")
####################### MAIN ######################

#=====================variables=======================
cpurl = "https://di.psteam.int.zone/cp"
#cpurl = "https://oap.psteam.int.zone/cp"
username = "admin"
password = "123qweASD"
#password = "oap-psteam"

country = "us" # must the one where the Provider can sell Office 365 services
state = "AK" # if required
#additional_params = ["111111111"] # depends on what is requested on the installation

#=====================Actions=======================
# Open browser
#mydriver = webdriver.Firefox() - fails too often = finishes with exit code 0, but doesn't do anything
driver = webdriver.Chrome(executable_path="..\chromedriver.exe")
driver.implicitly_wait(3)

# Action 1
login_to_cp(cpurl, username, password)

#result = create_customer("Test Customer PS1", country, state, "12345", additional_params, "testps1", "123qweASD")
result = "Account #1000006 has been created."
message = str(result)
assert(message.endswith("has been created.")), "Looks like the account was not created."

customerID = message.rstrip(" has been created.")
customerID = customerID.strip("Account #")
result = place_order(customerID, "Office 365 Enterprise E1", "pstest1.onmicrosoft.com")
assert(result == "Order submitted"), "place_order() Could not find the plan for order creation."
#place_order(customerID, "IIS Hosting", "pstest1.onmicrosoft.com")
