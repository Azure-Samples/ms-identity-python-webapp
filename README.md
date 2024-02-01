---
page_type: sample
languages:
- python
products:
- azure-active-directory
description: "This sample demonstrates a Python web application calling a Microsoft Graph that is secured using Azure Active Directory."
urlFragment: ms-identity-python-webapp
---
# Integrating Microsoft Identity Platform with a Python web application

This is a Python web application that uses the Flask framework and the Microsoft identity platform to sign in users and make authenticated calls to the Microsoft Graph API.

# Configuration

## If you are configuring your Microsoft Entra ID app or Microsoft Entra External ID app

To get started with this sample, you have two options:

* Use the Azure portal to create the Azure AD applications and related objects. Follow the steps in
  [Quickstart: Add sign-in with Microsoft to a Python web app](https://docs.microsoft.com/azure/active-directory/develop/web-app-quickstart?pivots=devlang-python).
* Use PowerShell scripts that automatically create the Azure AD applications and related objects (passwords, permissions, dependencies) for you, and then modify the configuration files. Follow the steps in the [App Creation Scripts README](./AppCreationScripts/AppCreationScripts.md).

## If you are configuring your B2C app

This sample can also work as a B2C app. If you are using a B2C tenant, follow
[Configure authentication in a sample Python web app by using Azure AD B2C](https://learn.microsoft.com/azure/active-directory-b2c/configure-authentication-sample-python-web-app).


# Deployment

Once you finish testing this web app locally, you can deploy it to your production.
You may choose any web app hosting services you want.
Here we will describe how to deploy it to
[Azure App Service](https://azure.microsoft.com/en-us/products/app-service).

* Follow the ["Quickstart: Deploy a Python (Django or Flask) web app to Azure App Service"](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python),
  but replace its sample app (which does not do user sign-in) with this web app.

* [Configure your app's settings](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal#configure-app-settings) to define [these environment variables](https://github.com/Azure-Samples/ms-identity-python-webapp/blob/main/.env.sample).

* If your `app_config.py` contains `SESSION_TYPE = "filesystem"`,
  you shall turn on "session affinity" (a.k.a. "ARR affinity") in your
  [App Service Web App's Configuration](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal#configure-general-settings)


## Contributing

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](/CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
