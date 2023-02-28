import os

b2c_tenant = os.getenv('TENANT_NAME')
signupsignin_user_flow = os.getenv('SIGNUPSIGNIN_USER_FLOW')
editprofile_user_flow = os.getenv('EDITPROFILE_USER_FLOW')

resetpassword_user_flow = os.getenv('RESETPASSWORD_USER_FLOW')  # Note: Legacy setting.
# If you are using the new
# "Recommended user flow" (https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions),
# you can remove the resetpassword_user_flow and the B2C_RESET_PASSWORD_AUTHORITY settings from this file.

authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = authority_template.format(tenant=b2c_tenant, user_flow=signupsignin_user_flow)
B2C_PROFILE_AUTHORITY = authority_template.format(tenant=b2c_tenant, user_flow=editprofile_user_flow)

B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(tenant=b2c_tenant, user_flow=resetpassword_user_flow)
# If you are using the new
# "Recommended user flow" (https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions),
# you can remove the resetpassword_user_flow and the B2C_RESET_PASSWORD_AUTHORITY settings from this file.

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# This is the API resource endpoint (*not* the endpoint of this app!)
ENDPOINT = ''

# These are the scopes you've exposed in the web API app registration in the Azure portal
SCOPE = []

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
