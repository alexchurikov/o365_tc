#ScriptName : Login.py
#---------------------
from myselenium import *

#=====================variables=======================
# CP login
cpurl = "https://di.psteam.int.zone/cp"
#cpurl = "https://oap.psteam.int.zone/cp"
username = "admin"
password = "123qweASD"
#password = "oap-psteam"

# Customer creation
country = "us" # must the one where the Provider can sell Office 365 services
state = "AK" # will be used if required
#additional_params = ["111111111"] # depends on what is requested on the installation
    # You can check it in Billing > Settings > Attributes, see if any attributes "Applicable to" "Accounts" are "Required".
    #FR001 - to implement checking required attributes in advance and request values for them

# Order creation
#service_params = ["111111111"] # depends on what is requested on the installation
    # You can check it in Billing > Service Plans > PLAN > SERVICE TEMPLATE > Service Parameters (see if there are any required ones)
    #FR002 - to implement checking required service parameters in advance and request values for them
#paymentMethod = "Pay Later" # Using default payment method for now #FR003

DELAY = 0.9 # Default value = 0.9. Increase it, if the panel is too slow for selenium to find some elements.
#=====================Actions=======================
# Open browser
mySelenium = MySelenium(DELAY)

# Action 1
mySelenium.login_to_cp(cpurl, username, password)

#result = create_customer("Test Customer PS1", country, state, "12345", additional_params, "testps1", "123qweASD")
result = "Account #1000006 has been created."
message = str(result)
assert(message.endswith("has been created.")), "Looks like the account was not created."
customerID = message.rstrip(" has been created.")
customerID = customerID.strip("Account #")

result = mySelenium.place_order(customerID, "Office 365 Enterprise E1", "pstest1.onmicrosoft.com")
message = str(result)
assert(message.endswith("has been placed.")), "Looks like the order was not created."
orderID = message[13:-16]
print "Order ID: " + orderID