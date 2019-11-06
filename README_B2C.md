---
page_type: sample
languages:
- python
- html
products:
- azure-active-directory
description: "This sample demonstrates a Python web application calling a web api that is secured using Azure Active Directory."
urlFragment: ms-identity-python-webapp
---
# Integrating B2C feature of Microsoft identity platform with a Python web application

## About this sample

> This sample was initially developed as a web app to demonstrate how to
> [Integrate Microsoft Identity Platform with a Python web application](https://github.com/Azure-Samples/ms-identity-python-webapp/blob/master/README.md).
> The same code base can also be used to demonstrate how to
> Integrate B2C of Microsoft identity platform with a Python web application.
> All you need is some different steps to register your app in your own B2C tenant,
> and then feed those different settings into the configuration file of this sample.

This sample covers the following:

* Update the application in Azure AD B2C
* Configure the sample to use the application
* Enable authentication in a web application using Azure Active Directory B2C
* Access a web API using Azure Active Directory B2C


### Overview

This sample demonstrates a Python web application that signs-in users with the Microsoft identity platform and calls another web api.

1. The python web application uses the Microsoft Authentication Library (MSAL) to obtain an access token from the Microsoft identity platform (formerly Azure AD v2.0):
2. The access token is used as a bearer token to authenticate the user when calling the web api.

![Overview](./ReadmeFiles/topology.png)


## Prerequisites

1. [Create an Azure Active Directory B2C tenant](https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant)
1. [Register an application in Azure Active Directory B2C](https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-applications).
1. [Create user flows in Azure Active Directory B2C](https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-user-flows)
1. Have [Python 2.7+ or Python 3+](https://www.python.org/downloads/) installed


## Update the application

In the tutorial that you completed as part of the prerequisites, you [added a web application in Azure AD B2C](https://docs.microsoft.com/azure/active-directory-b2c/tutorial-register-applications).
To enable communication with the sample in this tutorial, you need to add a redirect URI to that application in Azure AD B2C.

* Modify an existing or add a new **Reply URL**, for example `http://localhost:5000/getAToken` or `https://your_domain.com:5000/getAToken`.
  You could use any port or any path. Later we will set this sample to match what you register here.
* On the properties page, record the application ID that you'll use when you configure the web application.
* Also generate a key (client secret) for your web application. Record the key that you'll use when you configure this sample.


## Configure the sample

### Step 1:  Clone or download this repository

From your shell or command line:

```Shell
git clone https://github.com/Azure-Samples/ms-identity-python-webapp.git
```

or download and extract the repository .zip file.

> Given that the name of the sample is quite long, you might want to clone it in a folder close to the root of your hard drive, to avoid file name length limitations when running on Windows.


### Step 2:  Install sample dependency

Install the dependencies using pip:

```Shell
$ pip install -r requirements.txt
```

### Step 3:  Configure the sample to use your Azure AD tenant

In the steps below, "ClientID" is the same as "Application ID" or "AppId".

#### Configure the pythonwebapp project

> Note: if you used the setup scripts, the changes below may have been applied for you

1. Use the `app_config_b2c.py` template to replace `app_config.py`.
1. Open the (now replaced) `app_config.py` file

   * Update the value of `b2c_tenant` with the name of the Azure AD B2C tenant that you created.
     For example, replace `fabrikamb2c` with `contoso`.
   * Replace the value of `CLIENT_ID` with the application ID that you recorded.
   * Replace the value of `CLIENT_SECRET` with the key that you recorded.
   * Replace the value of `signupsignin_user_flow` with `b2c_1_signupsignin1`.
   * Replace the value of `editprofile_user_flow` with `b2c_1_profileediting1`.
   * Replace the value of `resetpassword_user_flow` with `b2c_1_passwordreset1`.
   * Replace the value of `REDIRECT_PATH` with the path part you set up in **Reply URL**.
     For example, `/getAToken`. It will be used by this sample app to form
     an absolute URL which matches your full **Reply URL**.
   * You do not have to configure the `ENDPOINT` and `SCOPE` right now


## Enable authentication

Run app.py from shell or command line. Note that the port needs to match what you've set up in your **Reply URL**:
```Shell
$ flask run --port 5000
```

You should now be able to visit `http://localhost:5000` and use the sign-in feature.
This is how you enable authentication in a web application using Azure Active Directory B2C.


## Access a web API

This sample itself does not act as a web API.
Here we assume you already have your web API up and running elsewhere in your B2C tenant,
with a specific endpoint, protected by a specific scope,
and your sample app is already granted permission to access that web API.

Now you can configure this sample to access that web API.

1. Open the (now replaced) `app_config.py` file
   * Replace the value of `ENDPOINT` with the actual endpoint of your web API.
   * Replace the value of `SCOPE` with a list of the actual scopes of your web API.
     For example, write them as `["demo.read", "demo.write"]`.

Now, re-run your web app sample, and you will find a new link showed up,
and you can access the web API using Azure Active Directory B2C.


## Community Help and Support

Use [Stack Overflow](http://stackoverflow.com/questions/tagged/msal) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`azure-active-directory` `adal` `msal` `python`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](/CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## More information

For more information, see MSAL.Python's [conceptual documentation]("https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki"):


For more information about web apps scenarios on the Microsoft identity platform see [Scenario: Web app that calls web APIs](https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-web-app-call-api-overview)

For more information about how OAuth 2.0 protocols work in this scenario and other scenarios, see [Authentication Scenarios for Azure AD](http://go.microsoft.com/fwlink/?LinkId=394414).
