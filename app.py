import os
import requests
from flask import Flask, render_template
from identity.flask import Auth
import app_config

__version__ = "0.9.0"  # The version of this sample, for troubleshooting purpose

app = Flask(__name__)

# Test this with private browser at http://localhost:5000/foo
@app.route("/foo")
def foo():
    return "foo"






















app.config.from_object(app_config)
auth = Auth(
    app,
    authority=os.getenv("AUTHORITY"),
    client_id=os.getenv("CLIENT_ID"),
    client_credential=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    oidc_authority=os.getenv("OIDC_AUTHORITY"),
    b2c_tenant_name=os.getenv('B2C_TENANT_NAME'),
    b2c_signup_signin_user_flow=os.getenv('SIGNUPSIGNIN_USER_FLOW'),
    b2c_edit_profile_user_flow=os.getenv('EDITPROFILE_USER_FLOW'),
    b2c_reset_password_user_flow=os.getenv('RESETPASSWORD_USER_FLOW'),
)

# Test this with private browser at http://localhost:5000/foo
# using johndoe@my_test_tenant.onmicrosoft.com
@app.route("/bar")
@auth.login_required()
def bar(*, context):
    return "bar"













@app.route("/")
@auth.login_required
def index(*, context):
    return render_template(
        'index.html',
        user=context['user'],  # Variable user has a dict of the ID token claims
        edit_profile_url=auth.get_edit_profile_url(),
        api_endpoint=os.getenv("ENDPOINT"),
        title=f"Flask Web App Sample v{__version__}",
    )





















# Uncomment the SCOPE in .env
@app.route("/call_api")
@auth.login_required(scopes=os.getenv("SCOPE", "").split())
#@auth.login_required(scopes=["Calendars.ReadWrite"],
def call_downstream_api(*, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="API Response", result=api_result)

