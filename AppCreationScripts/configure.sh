#!/bin/bash
az extension add --name account

# check if tenant argument was passed in
tenant_arg=$1
# if tenantId is specified, pass it in
if [ -n "$tenant_arg" ]; then
    az login --allow-no-subscriptions --tenant $tenant_arg
else
    az login --allow-no-subscriptions
fi

tenant_id=$(az account show --query tenantId --output tsv)

# Create a web application in Azure Active Directory
client_id=$(az ad app create --display-name "WebApp$RANDOM$RANDOM" \
    --web-redirect-uris "http://localhost:5000/getAToken" \
    --web-home-page-url "https://localhost:5000/" \
    --sign-in-audience AzureADandPersonalMicrosoftAccount \
    --query appId --output tsv)

# Add a client secret
client_secret=$(az ad app credential reset --id $client_id \
                --append --display-name "WebAppSecret" \
                --query password --output tsv)

# Grant permissions to Microsoft graph API User.ReadBasic.All using az ad app permission grant
az ad app permission add --id $client_id \
    --api 00000003-0000-0000-c000-000000000000 \
    --api-permissions b340eb25-3456-403f-be2f-af7a0d370277=Scope

az ad sp create --id $client_id

az ad app permission grant --id $client_id \
    --api 00000003-0000-0000-c000-000000000000 \
    --scope User.ReadBasic.All

# Delete .env file if it exists, otherwise create it
if [ -f .env ]; then
    > .env
else
    touch .env
fi

# Write the values to the file
echo "CLIENT_ID=$client_id" >> .env
echo "CLIENT_SECRET=$client_secret" >> .env
echo "TENANT_ID=$tenant_id" >> .env