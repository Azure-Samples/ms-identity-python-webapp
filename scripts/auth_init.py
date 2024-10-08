import argparse
import asyncio
import os

from azure.identity import AzureDeveloperCliCredential
from kiota_abstractions.api_error import APIError
from msgraph import GraphServiceClient
from msgraph.generated.applications.item.add_password.add_password_post_request_body import (
    AddPasswordPostRequestBody,
)
from msgraph.generated.models.application import Application
from msgraph.generated.models.implicit_grant_settings import ImplicitGrantSettings
from msgraph.generated.models.password_credential import PasswordCredential
from msgraph.generated.models.web_application import WebApplication
from dotenv import load_dotenv, set_key

async def check_for_application(client: GraphServiceClient, app_id: str) -> bool:
    try:
        await client.applications.by_application_id(app_id).get()
    except APIError:
        return False
    return True


async def create_application(client: GraphServiceClient, local_redirect_uri) -> Application:
    request_body = Application(
        display_name="WebApp",
        sign_in_audience="AzureADandPersonalMicrosoftAccount",
        web=WebApplication(
            redirect_uris=[local_redirect_uri],
            implicit_grant_settings=ImplicitGrantSettings(enable_id_token_issuance=True),
        ),
    )
    return await client.applications.post(request_body)


async def add_client_secret(client: GraphServiceClient, app_id: str) -> str:
    request_body = AddPasswordPostRequestBody(
        password_credential=PasswordCredential(display_name="WebAppSecret"),
    )
    result = await client.applications.by_application_id(app_id).add_password.post(request_body)
    return result.secret_text


async def main():
    ENV_FILE = ".env"
    load_dotenv(ENV_FILE)

    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", required=True, help="The tenant ID")
    args = parser.parse_args()

    tenant_id = os.getenv("TENANT_ID", args.tenant)
    if tenant_id != args.tenant:
        print("Tenant ID already set in env, not updating")
        exit(0)
    if not tenant_id:
        print("Tenant ID not set in env, please provide it via --tenant argument")
        exit(1)

    print("Initializing authentication for tenant ID: ", tenant_id)
    credential = AzureDeveloperCliCredential(tenant_id=tenant_id)

    scopes = ["https://graph.microsoft.com/.default"]
    client = GraphServiceClient(credentials=credential, scopes=scopes)

    app_id = os.getenv("APP_ID")
    if not app_id:
        print(f"Checking if application {app_id} exists")
        if await check_for_application(client, app_id):
            print("Application already exists, not creating new one")
            exit(0)

    print("Creating application registration")
    redirect_uri = "http://localhost:50505/redirect"
    app = await create_application(client, redirect_uri)

    print(f"Adding client secret to {app.id}")
    client_secret = await add_client_secret(client, app.id)

    print("Updating env with APP_ID, CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_URI")
    set_key(ENV_FILE, "AUTHORITY", "https://login.microsoftonline.com/" + tenant_id)
    set_key(ENV_FILE, "APP_ID", app.id)
    set_key(ENV_FILE, "CLIENT_ID", app.app_id)
    set_key(ENV_FILE, "CLIENT_SECRET", client_secret)
    set_key(ENV_FILE, "REDIRECT_URI", redirect_uri)


if __name__ == "__main__":
    asyncio.run(main())
