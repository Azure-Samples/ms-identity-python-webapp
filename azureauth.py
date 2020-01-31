import app_config
import msal

class AzureAuth:
   
    def __init__(self):
       self.cache = msal.SerializableTokenCache()
       self.confidentialClient = msal.ConfidentialClientApplication(app_config.CLIENT_ID)
    
    def build_msal_app(self):
        self.confidentialClient = msal.ConfidentialClientApplication(
            app_config.CLIENT_ID, 
            authority=app_config.AUTHORITY,
            client_credential=app_config.CLIENT_SECRET, 
            token_cache=self.cache)

    def get_auth_url(self, state=None, redirect_uri=None):
        return self.confidentialClient.get_authorization_request_url(
            app_config.SCOPE or [],
            state=state or str(uuid.uuid4()),
            redirect_uri=redirect_uri)

    def acquire_token_by_authorization_code(self, authCodeFromServer, redirectUri):
        return self.confidentialClient.acquire_token_by_authorization_code(
            authCodeFromServer,
            scopes=app_config.SCOPE, # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=redirectUri)

    def get_token_from_cache(self, flaskSession):
        self.load_cache(flaskSession)
        if self.confidentialClient.get_accounts():
            result = self \
                .confidentialClient \
                .acquire_token_silent(
                    app_config.SCOPE, 
                    account=self.confidentialClient.get_accounts()[0]
                )
            return result 
    
    def load_cache(self, flaskSession):
        if flaskSession.get("token_cache"):
            self.cache.deserialize(flaskSession["token_cache"])

    def save_cache(self):
        if self.cache.has_state_changed:
            return self.cache.serialize()
    
    def refreshToken():
        pass
