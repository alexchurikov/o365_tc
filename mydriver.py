# selenium related supplementary methods

from selenium import webdriver
from time import sleep
#import sys
import re
from utils import *

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException

class MyDriver:
    driver = None
    DELAY = 0

    def __init__(self, delay):
        self.DELAY = delay
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

    def find_name_in_popup(self, fieldElementID, name):
        self.fill_text_by_id(fieldElementID, name)
        self.click_id("_browse_search")  # search
        sleep(self.DELAY)

        #checking each found element for total match
        i = 1
        while True:
            debug("i=" + str(i))
            try:
                line = self.driver.find_element_by_id("vel_t1_" + str(i))
            except NoSuchElementException as ex:
                if i == 1:  # search found no objects
                    debug("Nothing found.")
                    return None
                else:
                     debug("Found something, but not exact match.")
                     return None
            try:
                debug("Line text:" + line.text)
                found_name = line.find_element_by_xpath(".//td[contains(text(),'" + name + "')]") # in popup we search for td instead of a.

                debug("Name: " + name)
                debug("Found name: " + found_name.text)
                without_spaces = re.sub('\s+',' ', found_name.text)
                debug("text_without_spaces: " + without_spaces)
                if without_spaces == name:
                    debug("Yes, it does.")
                    return found_name
            except NoSuchElementException as ex:
                print "Something went wrong. Will skip the current plan. Report this exception to developer:"
                print ex
                return None
            i += 1