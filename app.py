import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/profile")
def profile():  # Only used in B2C scenario.
    # If we would choose to have an explicit profile() controller here,
    # it would look like this. But we chose not to. Regardless,
    # the caveats below are still meaningful to help you (the repo maintainer)
    # to better understand what is going on under the hood.

    # We could also implement a ResetPassword page. The caveats below still apply.

    # Since each B2C policy could be a new issuer,
    # here we create a new one-time MSAL app instance.
    # If we reuse a global MSAL app, the returned tokens (if any) would be
    # stored in the main MSAL app's token cache, which we don't want to happen.
    app = _build_msal_app(authority=app_config.B2C_PROFILE_AUTHORITY)

    # EditProfile in B2C is done by calling the authorize_endpoint
    return redirect(app.get_authorization_request_url(

        # We usually don't need a new access token,
        # but we still have to provide an empty scope as a placeholder
        [],

        # Because we are preparing an authorize request, we need to specify a redirect_uri.
        # The next line does exactly that. But don't let its seemingly simpleness fool you.
        # Since different policy could represent different trust boundary,
        # it might make sense to register multiple redirect_uri, one per policy.
        # But in reality, admin might not realize that,
        # so there might be only one redirect_uri registered for this app.
        # Here in this sample, we choose to reuse that same redirect_uri
        # which was already used by the default SignIn policy,
        # but then later when we received the redirected-back HTTP request,
        # we would need a way to figure out that the request was triggered by
        # a different policy, therefore any returned tokens (if any) should NOT
        # go into the token cache of the main MSAL instance with SignIn policy.
        redirect_uri=url_for("authorized", _external=True),

        # Or, alternatively, here we did it in a hacky way.
        # We create a new random state for this new EditProfile authorize request,
        # but we purposely do NOT record that state in this session. Therefore,
        # when that redirect_uri is triggered, it would be automatically ignored
        # due to mismatching state. We know this is almost an anti-pattern hack.
        state=str(uuid.uuid4()),
        ))

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template

if __name__ == "__main__":
    app.run()

