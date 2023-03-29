# Registering sample apps with the Microsoft identity platform using the Azure CLI

## Overview

This directory includes two scripts to aid in the process of registering an app with the Microsoft identity platform
and configuring this sample app with the appropriate environment variables.

* *configure.sh*: A bash script that uses the Azure CLI to register an app, generate a client secret, and grant Microsoft Graph API permissions. It then stores the `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID` in a *.env* file locally.
* *cleanup.sh*: A bash script that uses the Azure CLI to delete the app registration based off the variables inside *.env*.

## Prerequisites

To run these scripts, you need:

1. An environment to run Bash scripts
2. [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
3. An Azure account with the permission to create app registrations

If you open this project inside a Dev Container in VS Code or inside Github Codespaces, you don't need to install anything.

## Running the configuration script


Run this script to set up the app registration:

```
./scripts/configure.sh
```

⚠️ Running the script will override the local *.env* file (if one exists) with new values.

You can optionally specify a tenant ID if your account has multiple tenants and you'd like to register an app in the specified tenant.

```
./configure.sh <tenant ID>
```

## Run the cleanup script

This script takes no arguments, as it retrieves everything from the local *.env*:

```
./cleanup.sh
```