import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from werkzeug.exceptions import Unauthorized, Forbidden
from identity import __version__
from identity.web import Web, LifespanValidator
import app_config


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

web = Web(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
    redirect_uri="http://localhost:5000" + app.config["REDIRECT_PATH"],  # It must match your redirect_uri
    validators=[LifespanValidator(seconds=3600, on_error=Unauthorized("Login expired"))],
    )

@app.route("/")
def index():
    if not web.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=web.get_user(), version=__version__)

@app.route("/login")
def login():
    return render_template("login.html", version=__version__, **web.start_auth(scopes=app_config.SCOPE))

@app.errorhandler(Unauthorized)
def handler(error):
    return redirect(url_for("login"))

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def auth_response():
    result = web.complete_auth(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    return redirect(web.sign_out(url_for("index", _external=True)))

@app.route("/graphcall")
def graphcall():
    token = web.get_token(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)

if __name__ == "__main__":
    app.run()

