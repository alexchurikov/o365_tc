#ScriptName : Login.py
#---------------------
from myselenium import *

#=====================variables=======================
# CP login
# version 7.3:
cpurl = "https://di.psteam.int.zone/cp"
# version 8.0:
#cpurl = "https://odindemo.com/cp"
#cpurl = "https://oap.psteam.int.zone/cp"
username = "admin"
password = "123qweASD"
#password = "J3TbU7F5U6k3"
#password = "oap-psteam"

# Customer creation
country = "us" # must the one where the Provider can sell Office 365 services
state = "AK" # will be used if required
customerName = "Test Customer PS1"
postalIndex = "12345"
userLogin = "testps9"
userPassword = "123qweASD"
additionalParams = []
#additionalParams = ["111111111", "222"] # depends on what is requested on the installation
    # You can check it in Billing > Settings > Attributes, see if any attributes "Applicable to" "Accounts" are "Required".
    #FR001 - to implement checking required attributes in advance and request values for them

# Order creation
planName = "Office 365 Enterprise E1"
domainName = "pstest9.onmicrosoft.com"
#service_params = ["111111111"] # depends on what is requested on the installation
    # You can check it in Billing > Service Plans > PLAN > SERVICE TEMPLATE > Service Parameters (see if there are any required ones)
    #FR002 - to implement checking required service parameters in advance and request values for them
#paymentMethod = "Pay Later" # Using default payment method for now #FR003

DELAY = 0.9 # Default value = 0.9. Increase it, if the panel is too slow for selenium to find some elements.
#=====================Actions=======================
# Open browser
mySelenium = MySelenium(DELAY)

# Log in to CP
mySelenium.login_to_cp(cpurl, username, password)

# creating customer
result = mySelenium.create_customer(customerName, country, state, postalIndex, additionalParams, userLogin, userPassword)
#result = "Account #1000006 has been created."
message = str(result)
assert(message.endswith("has been created.")), "Looks like the account was not created."
customerID = message.rstrip(" has been created.")
customerID = customerID.strip("Account #")

# placing order
result = mySelenium.place_order(customerID, planName, domainName)
#result = "Sales order #SO000011 has been placed."
message = str(result)
assert(message.endswith("has been placed.")), "Looks like the order was not created."
orderID = message[13:-16]
debug("Order ID: " + orderID)

# process order and check tasks in OA

#subscriptionID = mySelenium.process_order(orderID)
#assert(subscriptionID > 0), "Looks like order processing failed."
#result = mySelenium.check_subscription_tasks(subscriptionID)
#assert(result == 0), "Looks like some tasks failed in OA."
