import os

b2c_tenant = "fabrikamb2c"
signupsignin_user_flow = "b2c_1_signupsignin1"
editprofile_user_flow = "b2c_1_profileediting1"
resetpassword_user_flow = "b2c_1_passwordreset1"
authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"

CLIENT_SECRET = "Enter_the_Client_Secret_Here" # Our Quickstart uses this placeholder
# In your production app, we recommend you to use other ways to store your secret,
# such as KeyVault, or environment variable as described in Flask's documentation here
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=signupsignin_user_flow)
B2C_PROFILE_AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=editprofile_user_flow)
B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=resetpassword_user_flow)

CLIENT_ID = "Enter_the_Application_Id_here"

REDIRECT_PATH = "/getAToken"  # It will be used to form an absolute URL
    # And that absolute URL must match your app's redirect_uri set in AAD

# This is the resource that you are going to access in your B2C tenant
ENDPOINT = ''

# These are the scopes that you defined for the web API
SCOPE = ["demo.read", "demo.write"]

SESSION_TYPE = "filesystem"  # So token cache will be stored in server-side session

