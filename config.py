class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = 'super_secret_key'

    # Flask-Session
    SESSION_TYPE = 'filesystem'
