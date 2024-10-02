from jinja2.exceptions import TemplateNotFound
import pytest

# Note: This test file needs to be located in the same folder as the app.py
from app import app


def test_login_attempt_should_render_its_template():
    app.config.update(TESTING=True)  # Otherwise exceptions will not be thrown
    try:
        response = app.test_client().get("/")
        print(response.data)  # Typically a configuration error page rendered from template
    except TemplateNotFound:
        pytest.fail(
            "Template should be accessible, "
            "typically came from inside the Identity package.")

