#!/bin/bash
az extension add --name account

tenant_arg=$1
if [ -n "$tenant_arg" ]; then
    echo "Attempting login to Azure with tenant ID $tenant_arg..."
    az login --allow-no-subscriptions --tenant $tenant_arg --output none
else
    echo "Attempting login to Azure..."
    az login --allow-no-subscriptions --output none
fi

tenant_id=$(az account show --query tenantId --output tsv)

echo "Attempting app registration creation..."
client_id=$(az ad app create --display-name "WebApp$RANDOM$RANDOM" \
    --web-redirect-uris "http://localhost:5000/getAToken" \
    --web-home-page-url "https://localhost:5000/" \
    --sign-in-audience AzureADandPersonalMicrosoftAccount \
    --query appId --output tsv)

echo "Attempting to add a client secret to app $client_id ..."
client_secret=$(az ad app credential reset --id $client_id \
                --append --display-name "WebAppSecret" \
                --query password --output tsv)

echo "Attempting to grant permissions for app $client_id to Microsoft Graph API User.ReadBasic.All..."
az ad app permission add --id $client_id \
    --api 00000003-0000-0000-c000-000000000000 \
    --api-permissions b340eb25-3456-403f-be2f-af7a0d370277=Scope \
    --only-show-errors --output none

az ad sp create --id $client_id --output none

az ad app permission grant --id $client_id \
    --api 00000003-0000-0000-c000-000000000000 \
    --scope User.ReadBasic.All \
    --output none

# Delete .env file if it exists, otherwise create it
echo "Creating .env file..."
if [ -f .env ]; then
    > .env
fi

echo "Writing configuration to .env file..."
echo "CLIENT_ID=$client_id" >> .env
echo "CLIENT_SECRET=$client_secret" >> .env
echo "TENANT_ID=$tenant_id" >> .env

echo "Configuration complete."
