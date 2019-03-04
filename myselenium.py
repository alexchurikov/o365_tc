# High-level methods, OA/BA objects related

from selenium import webdriver
from time import sleep
#import sys
import re
from utils import *
from mydriver import *

class MySelenium:
    myDriver = None
    DELAY = 0

    def __init__(self, delay):
        self.DELAY = delay
        self.myDriver = MyDriver(delay)

    def login_to_cp(self, cpurl, username, password):
        self.myDriver.driver.get(cpurl)
        self.myDriver.fill_text_by_xpath("//input[@name='user']", username)
        self.myDriver.fill_text_by_xpath("//input[@name='password']", password)
        self.myDriver.click_xpath("//button[@name='login']")
        self.myDriver.driver.maximize_window()

    def switch_panel(self, neededPanelName): # "Billing" or "Operations"
        sleep(self.DELAY)

        self.myDriver.driver.switch_to.frame("topFrame")
        panelName = self.myDriver.driver.find_element_by_id("to_bm") #find <a> element

        if panelName.text == neededPanelName:
            panelName.click()

    def create_customer(self, company_name, country_code, state, zip, additional_parameters, login, password):
        print "Creating customer with name: ", company_name

        win = self.myDriver.driver.current_window_handle

        self.switch_panel("Billing")

        self.myDriver.driver.switch_to.window(win) # otherwise selenium doesn't see the frame
        self.myDriver.driver.switch_to.frame("leftFrame")

        self.myDriver.click_id("click_my_end_user_accounts")

        self.myDriver.driver.switch_to.window(win) # otherwise selenium doesn't see the frame
        self.myDriver.driver.switch_to.frame("mainFrame")
        self.myDriver.click_id("input_____customer_add")
        self.myDriver.click_id("input___Save")
        self.myDriver.fill_text_by_id("input___Company", company_name)
        self.myDriver.fill_text_by_id("input___Address1", "Test st. 123")
        self.myDriver.fill_text_by_id("input___City", "Testcity")
        self.myDriver.fill_text_by_id("input___CountryCountryID", country_code)
        self.myDriver.fill_text_by_id("input___StateState", state)
        self.myDriver.fill_text_by_id("input___Zip", zip)
        self.myDriver.fill_text_by_id("input___AdminFName", "Test")
        self.myDriver.fill_text_by_id("input___AdminLName", "Customer")
        self.myDriver.fill_text_by_id("input___AdminEmail", "test@customer.tld")
        self.myDriver.fill_text_by_id("input___AdminPhCountryCode", "1")
        self.myDriver.fill_text_by_id("input___AdminPhAreaCode", "123")
        self.myDriver.fill_text_by_id("input___AdminPhNumber", "4567890")
        self.myDriver.click_id("input___Save")

        # Additional parameters
        numOfParams = len(additional_parameters)
        # if some parameters are passed, verify that their number (numOfParams) matches the number of requeted parameters (numOfFields)
        if numOfParams > 0:
            additionalInformationElements = self.myDriver.driver.find_element_by_id('Additional Information').find_elements_by_tag_name("input")
            numOfFields = len(additionalInformationElements)

            if numOfParams != numOfFields:
                message = "Customer creation error: Number of specified additional parameters(",numOfParams,") is not equal to the number of fields on the page(",num_of_fields,"). "
                message = message + "SOLUTION: if there are no required parameters, remove all parameters in variables like this: additionalParams = []"
                message = message + "Otherwise: additionalParams array should contain full list of parameters requested by the page."
                raise message

            for i in {0, numOfParams-1}:
                additionalInformationElements[i].send_keys(additional_parameters[i])

        self.myDriver.click_id("input___Next")

        self.myDriver.fill_text_by_id("input___Login",login)
        self.myDriver.fill_text_by_id("input___Password", password)

        self.myDriver.click_id("input___SP_ViewAccount")

        result = self.myDriver.driver.find_element_by_id("opresult_id").find_element_by_class_name("msg-content").text
        print "Customer creation result:"
        print result

        return result

    def place_order(self, customerID, planName, subdomain):
        print "Placing order for customer #" + customerID + ", purchasing plan '" + planName + "'"

        win = self.myDriver.driver.current_window_handle
        self.myDriver.driver.switch_to.window(win) # otherwise selenium doesn't see the frame

        self.switch_panel("Billing")

        self.myDriver.driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
        self.myDriver.driver.switch_to.frame("leftFrame")

        self.myDriver.click_id("click_orders")

        self.myDriver.driver.switch_to.window(win)  # otherwise selenium doesn't see the frame
        self.myDriver.driver.switch_to.frame("mainFrame")
        self.myDriver.click_id("input___add")

        # filling fields
        # filling customer ID
        self.myDriver.fill_text_by_id("input___AccountAccountID",customerID)

        # choosing plan
        self.myDriver.click_id("input___refPlan")
        self.myDriver.driver.switch_to.window(self.myDriver.driver.window_handles[1])
        assert (self.myDriver.driver.title == "Service Plans"), "Could not find Service Plans popup."

        plan = self.myDriver.find_name_in_popup("filter_name", planName)
        if plan==None:
            print "Order creation failed, plan '" + planName + "' was not found, exiting."
            return
        plan.click()
        self.myDriver.driver.switch_to.window(win)
        self.myDriver.driver.switch_to.frame("mainFrame")

        # choosing period
        self.myDriver.click_id("input___ct_refPlanPeriod")
        self.myDriver.driver.switch_to.window(self.myDriver.driver.window_handles[1])
        assert (self.myDriver.driver.title == "Subscription Periods"), "Could not find Subscription Periods popup."
        period = self.myDriver.driver.find_element_by_id("vel_t1_1") # choosing the first line
        period.click()

        self.myDriver.driver.switch_to.window(win)
        self.myDriver.driver.switch_to.frame("mainFrame")
        self.myDriver.click_id("input___SaveAdd")

        # next screen (parameters)
        self.myDriver.fill_text_by_id("input____aps_defaults_o365", subdomain) # filling .onmicrosoft.com sub-domain
        # assuming there are no other required parameters
        self.myDriver.click_id("input___Next")

        # select payment method
        # Using default one for now
        self.myDriver.click_id("input___SP_ViewPromoOrder")

        result = self.myDriver.driver.find_element_by_id("opresult_id").find_element_by_class_name("msg-content").text
        print "Order creation result:"
        print result

        return result

    def find_subscription_ID(self, orderID):
        return 0

    def process_order(self, orderID):
        self.switch_panel("Billing")

        # find order

        # check status

        # if New, open it.

        # if Payment Method not Attached, pay order - create credit memo

        orderStatus = "Completed"
        if orderStatus == "Processed":
            return find_subscription_ID(orderID)
        else:
            return -1

    def find_oa_tasks(self, subscriptionID):
        self.myDriver.switch_panel("Operations")

    def check_subscription_tasks(self, subscriptionID): # returns array of failed task IDs (can be empty array)
        while 1:
            find_oa_tasks(subscriptionID)