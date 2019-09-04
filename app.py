import uuid
import flask
import requests
from flask import Flask, render_template, session, request
from flask_session import Session
import msal
import app_config

sess = Session()
app = Flask(__name__)
app.config.from_object('config.Config')
sess.init_app(app)

cache = msal.SerializableTokenCache()
application = msal.ConfidentialClientApplication(
    app_config.CLIENT_ID, authority=app_config.AUTHORITY,
    client_credential=app_config.CLIENT_SECRET,
    token_cache=cache)


def set_cache():
    if cache.has_state_changed:
        session[request.cookies.get("session")] = cache.serialize()


@app.route('/')
def index():
    # Initializing
    if (session.get(request.cookies.get("session"), '')) == '':
        session[request.cookies.get("session")] = ''
    cache.deserialize(session.get(request.cookies.get("session")))
    return render_template("index.html")


@app.route('/authenticate')
def authenticate():
    # Call to the authorize endpoint
    auth_state = str(uuid.uuid4())
    session[(request.cookies.get("session")+'state')] = auth_state
    authorization_url = application.get_authorization_request_url(app_config.SCOPE, state=auth_state,
                                                                  redirect_uri=app_config.REDIRECT_URI)
    resp = flask.Response(status=307)
    resp.headers['location'] = authorization_url
    return resp


@app.route("/getAToken")
def main_logic():
    code = flask.request.args['code']
    state = flask.request.args['state']
    # Raising error if state does not match
    if state != session[(request.cookies.get("session")+'state')]:
        raise ValueError("State does not match")
    result = None
    # Checking token cache for accounts
    accounts = application.get_accounts()

    # Trying to acquire token silently
    if accounts:
        result = application.acquire_token_silent(app_config.SCOPE, account=accounts[0])

    # If silent call fails, fallback to acquireToken interactive call
    if not result:
        result = application.acquire_token_by_authorization_code(code, scopes=app_config.SCOPE,
                                                                 redirect_uri=app_config.REDIRECT_URI)
    # Updating cache
    set_cache()

    # Using access token from result to call Microsoft Graph
    if 'access_token' not in result:
        return flask.redirect(flask.url_for('index'))
    endpoint = 'https://graph.microsoft.com/v1.0/me/'
    http_headers = {'Authorization': 'Bearer ' + result['access_token'],
                    'User-Agent': 'msal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    return flask.render_template('display.html', auth_result=graph_data)


@app.route("/logout")
def logout():
    # Logout
    accounts = application.get_accounts()
    application.remove_account(accounts[0])
    set_cache()
    return flask.redirect(flask.url_for('index'))


if __name__ == "__main__":
    app.run()
