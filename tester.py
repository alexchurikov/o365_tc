#ScriptName : Login.py
#---------------------
from myselenium import *

#=====================variables=======================
cpurl = "https://di.psteam.int.zone/cp"
#cpurl = "https://oap.psteam.int.zone/cp"
username = "admin"
password = "123qweASD"
#password = "oap-psteam"

country = "us" # must the one where the Provider can sell Office 365 services
state = "AK" # will be used if required
#additional_params = ["111111111"] # depends on what is requested on the installation

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
assert(result == "Order submitted"), "place_order() Could not find the plan for order creation."

