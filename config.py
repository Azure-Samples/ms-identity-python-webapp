class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = 'super_secret_key'  # Setting it as an environment variable is recommended

    # Flask-Session
    SESSION_TYPE = 'filesystem'  # You can choose between Redis, SqlAlchemy, MongoDB or memcachec
    # There are other configuration options which can be used for a more customized application
    # More information about this can be found here : https://pythonhosted.org/Flask-Session/
