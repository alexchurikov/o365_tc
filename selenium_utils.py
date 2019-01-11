from selenium import webdriver
from time import sleep
#import sys
import re
from utils import *

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException

DELAY = 0.9

class MySelenium:
    driver = None

    def __init__(self):
        #mydriver = webdriver.Firefox() - fails too often = finishes with exit code 0, but doesn't do anything
        self.driver = webdriver.Chrome(executable_path="..\chromedriver.exe")
        self.driver.implicitly_wait(3)

    def fill_text_by_xpath(self, location, text):
        element = self.driver.find_element_by_xpath(location)
        element.clear()
        element.send_keys(text)

    def fill_text_by_id(self, location, text):
        element = self.driver.find_element_by_id(location)
        element.clear()
        element.send_keys(text)

    def click_xpath(self, location):
        self.driver.find_element_by_xpath(location).click()

    def click_id(self, location):
        self.driver.find_element_by_id(location).click()

    def login_to_cp(self, cpurl, username, password):
        self.driver.get(cpurl)
        self.fill_text_by_xpath("//input[@name='user']", username)
        self.fill_text_by_xpath("//input[@name='password']", password)
        self.click_xpath("//button[@name='login']")
        self.driver.maximize_window()

    def switch_panel(self, needed_panel_name): # "Billing" or "Operations"
        sleep(DELAY)
        self.driver.switch_to.frame("topFrame")
        panelName = self.driver.find_element_by_id("to_bm") #find <a> element

        if panelName.text == needed_panel_name:
            panelName.click()

    def create_customer(self, company_name, country_code, state, zip, additional_parameters, login, password):
        print "Creating customer with name: ", company_name

        win = self.driver.current_window_handle

        self.switch_panel("Billing")

        self.driver.switch_to.window(win) # otherwise selenium doesn't see the frame
        self.driver.switch_to.frame("leftFrame")

        self.click_id("click_my_end_user_accounts")

        self.driver.switch_to.window(win) # otherwise selenium doesn't see the frame
        self.driver.switch_to.frame("mainFrame")
        self.click_id("input_____customer_add")
        self.click_id("input___Save")
        self.fill_text_by_id("input___Company", company_name)
        self.fill_text_by_id("input___Address1", "Test st. 123")
        self.fill_text_by_id("input___City", "Testcity")
        self.fill_text_by_id("input___CountryCountryID", country_code)
        self.fill_text_by_id("input___StateState", state)
        self.fill_text_by_id("input___Zip", zip)
        self.fill_text_by_id("input___AdminFName", "Test")
        self.fill_text_by_id("input___AdminLName", "Customer")
        self.fill_text_by_id("input___AdminEmail", "test@customer.tld")
        self.fill_text_by_id("input___AdminPhCountryCode", "1")
        self.fill_text_by_id("input___AdminPhAreaCode", "123")
        self.fill_text_by_id("input___AdminPhNumber", "4567890")
        self.click_id("input___Save")

        # Additional parameters
        additional_information_elements = self.driver.find_element_by_id('Additional Information').find_elements_by_tag_name("input")

        num_of_params = len(additional_parameters)
        num_of_fields = len(additional_information_elements)

        if num_of_params != num_of_fields:
            message = "Customer creation error: Number of specified additional parameters(",num_of_params,") is not equal to the number of fields on the page(",num_of_fields,")"
            raise message
        else:
            for i in {0, num_of_params-1}:
                additional_information_elements[i].send_keys(additional_parameters[i])

        self.click_id("input___Next")

        self.fill_text_by_id("input___Login",login)
        self.fill_text_by_id("input___Password", password)

        self.click_id("input___SP_ViewAccount")

        result = self.driver.find_element_by_id("opresult_id").find_element_by_class_name("msg-content").text
        print "Customer creation result:"
        print result

        return result

    def find_name_in_popup(self, field_element_id, name):
        self.fill_text_by_id(field_element_id, name)
        self.click_id("_browse_search")  # search
        sleep(DELAY)

        #checking each found element for total match
        i = 1
        while True:
            debug("i=" + str(i))
            try:
                line = self.driver.find_element_by_id("vel_t1_" + str(i))
            except NoSuchElementException as ex:
                if i == 1:  # search found no objects
                    print "Nothing found."
                    return None
                else:
                     print "Found something, but not exact match."
                     return None
            try:
                #print line.text
                found_name = line.find_element_by_xpath(".//a[contains(text(),'" + name + "')]")

                print "Name: " + name
                print "Found name: " + found_name.text
                without_spaces = re.sub('\s+',' ', found_name.text)
                print "text_without_spaces: " + without_spaces
                if without_spaces == name:
                    print "Yes, it does."
                    return found_name
            except NoSuchElementException as ex:
                print "Something went wrong. Will skip the current plan. Report this exception to developer:"
                print ex
                return None
            i += 1


    def place_order(self, customerID, planName, subdomain):
        print "Placing order for customer #" + customerID + ", purchasing plan '" + planName + "'"

        win = self.driver.current_window_handle

        self.switch_panel("Billing")

        self.driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
        self.driver.switch_to.frame("leftFrame")

        self.click_id("click_orders")

        self.driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
        self.driver.switch_to.frame("mainFrame")
        self.click_id("input___add")

        # filling fields
        # filling customer ID
        self.fill_text_by_id("input___AccountAccountID",customerID)
        self.click_id("input___refPlan")

        # choosing plan
        self.driver.switch_to.window(self.driver.window_handles[1])
        assert (self.driver.title == "Service Plans"), "Could not find Service Plans popup."

        plan = self.find_name_in_popup("filter_name", planName)
        if plan==None:
            print "Order creation failed, plan '" + planName + "' was not found, exiting."
            return
        #plan.click()
        #driver.switch_to.window(win)

        # choosing

        #driver.switch_to().window(win)  # switch back to parent window
        #driver.switch_to.frame("mainFrame")