import os


if (os.getenv('B2C_TENANT_NAME')
    and os.getenv('SIGNUPSIGNIN_USER_FLOW') and os.getenv('EDITPROFILE_USER_FLOW')):
    # This branch is for B2C. You can delete this branch if you are not using B2C.
    b2c_tenant = os.getenv('B2C_TENANT_NAME')
    authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"
    AUTHORITY = authority_template.format(
        tenant=b2c_tenant,
        user_flow=os.getenv('SIGNUPSIGNIN_USER_FLOW'))
    B2C_PROFILE_AUTHORITY = authority_template.format(
        tenant=b2c_tenant,
        user_flow=os.getenv('EDITPROFILE_USER_FLOW'))
    B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(
        # If you are using the new "Recommended user flow"
        # (https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions),
        # you can remove the B2C_RESET_PASSWORD_AUTHORITY settings from this file.
        tenant=b2c_tenant,
        user_flow=os.getenv('RESETPASSWORD_USER_FLOW'))
else:  # This branch is for AAD or CIAM
    # You can configure your authority via environment variable
    # Defaults to a multi-tenant app in world-wide cloud
    AUTHORITY = os.getenv("AUTHORITY") or "https://login.microsoftonline.com/common"

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"
# Using the file system will not work in most production systems,
# it's better to use a database-backed session store instead.
