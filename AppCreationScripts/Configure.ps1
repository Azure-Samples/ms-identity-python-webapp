[CmdletBinding()]
param(
    [Parameter(Mandatory = $False, HelpMessage = 'Tenant ID (This is a GUID which represents the "Directory ID" of the AzureAD tenant into which you want to create the apps')]
    [string] $tenantId,
    [Parameter(Mandatory = $False, HelpMessage = 'Azure environment to use while running the script. Default = Global')]
    [string] $azureEnvironmentName
)

<#
 This script creates the Azure AD applications needed for this sample and updates the configuration files
 for the visual Studio projects from the data in the Azure AD applications.
 In case you don't have Microsoft.Graph.Applications already installed, the script will automatically install it for the current user
 
 There are two ways to run this script. For more information, read the AppCreationScripts.md file in the same folder as this script.
#>

<#.Description
   This function takes a string input as a single line, matches a key value and replaces with the replacement value
#> 
Function ReplaceInLine([string] $line, [string] $key, [string] $value) {
    $index = $line.IndexOf($key)
    if ($index -ige 0) {
        $index2 = $index + $key.Length
        $line = $line.Substring(0, $index) + $value + $line.Substring($index2)
    }
    return $line
}

<#.Description
   This function takes a dictionary of keys to search and their replacements and replaces the placeholders in a text file
#> 
Function UpdateTextFile([string] $configFilePath, [System.Collections.HashTable] $dictionary) {
    # Check if text file exists. If not, copy .env.sample.
    if (!(Test-Path $configFilePath)) {
        Copy-Item "$configFilePath.sample" $configFilePath
    }
    $lines = Get-Content $configFilePath
    $index = 0
    while ($index -lt $lines.Length) {
        $line = $lines[$index]
        foreach ($key in $dictionary.Keys) {
            if ($line.Contains($key)) {
                $lines[$index] = ReplaceInLine $line $key $dictionary[$key]
            }
        }
        $index++
    }

    Set-Content -Path $configFilePath -Value $lines -Force
}

<#.Description
   Primary entry method to create and configure app registrations
#> 
Function ConfigureApplications {
    $isOpenSSl = 'N' #temporary disable open certificate creation 

    <#.Description
       This function creates the Azure AD applications for the sample in the provided Azure AD tenant and updates the
       configuration files in the client and service project  of the visual studio solution (App.Config and Web.Config)
       so that they are consistent with the Applications parameters
    #> 
    
    if (!$azureEnvironmentName) {
        $azureEnvironmentName = "Global"
    }

    # Connect to the Microsoft Graph API, non-interactive is not supported for the moment (Oct 2021)
    Write-Host "Connecting to Microsoft Graph"
    if ($tenantId -eq "") {
        Connect-MgGraph -Scopes "User.Read.All Organization.Read.All Application.ReadWrite.All" -Environment $azureEnvironmentName
    }
    else {
        Connect-MgGraph -TenantId $tenantId -Scopes "User.Read.All Organization.Read.All Application.ReadWrite.All" -Environment $azureEnvironmentName
    }
    
    $context = Get-MgContext
    $tenantId = $context.TenantId

    # Get the user running the script
    $currentUserPrincipalName = $context.Account
    $user = Get-MgUser -Filter "UserPrincipalName eq '$($context.Account)'"

    # get the tenant we signed in to
    $Tenant = Get-MgOrganization
    $tenantName = $Tenant.DisplayName
    
    $verifiedDomain = $Tenant.VerifiedDomains | Where-Object { $_.Isdefault -eq $true }
    $verifiedDomainName = $verifiedDomain.Name
    $tenantId = $Tenant.Id

    Write-Host ("Connected to Tenant {0} ({1}) as account '{2}'. Domain is '{3}'" -f $Tenant.DisplayName, $Tenant.Id, $currentUserPrincipalName, $verifiedDomainName)

    # Create the webApp AAD application
    Write-Host "Creating the AAD application (WebApp)"
    # create the application 
    $webAppAadApplication = New-MgApplication -DisplayName "WebApp" `
        -Web `
    @{ `
            RedirectUris = "http://localhost:5000/getAToken"; `
            HomePageUrl  = "https://localhost:5000/"; `
            LogoutUrl    = "https://localhost:5000/logout"; `
                                                        
    } `
        -SignInAudience AzureADandPersonalMicrosoftAccount `
        #end of command

    #add a secret to the application
    $pwdCredential = Add-MgApplicationPassword -ApplicationId $webAppAadApplication.Id -PasswordCredential $key
    $webAppAppKey = $pwdCredential.SecretText

    $currentAppId = $webAppAadApplication.AppId
    $currentAppObjectId = $webAppAadApplication.Id

    $tenantName = (Get-MgApplication -ApplicationId $currentAppObjectId).PublisherDomain
    #Update-MgApplication -ApplicationId $currentAppObjectId -IdentifierUris @("https://$tenantName/WebApp")
    
    # create the service principal of the newly created application     
    $webAppServicePrincipal = New-MgServicePrincipal -AppId $currentAppId -Tags { WindowsAzureActiveDirectoryIntegratedApp }

    # add the user running the script as an app owner if needed
    $owner = Get-MgApplicationOwner -ApplicationId $currentAppObjectId
    if ($null -eq $owner) { 
        New-MgApplicationOwnerByRef -ApplicationId $currentAppObjectId  -BodyParameter = @{"@odata.id" = "htps://graph.microsoft.com/v1.0/directoryObjects/$user.ObjectId" }
        Write-Host "'$($user.UserPrincipalName)' added as an application owner to app '$($webAppServicePrincipal.DisplayName)'"
    }
    Write-Host "Done creating the webApp application (WebApp)"

    # URL of the AAD application in the Azure portal
    # Future? $webAppPortalUrl = "https://portal.azure.com/#@"+$tenantName+"/blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/Overview/appId/"+$currentAppId+"/objectId/"+$currentAppObjectId+"/isMSAApp/"
    $webAppPortalUrl = "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/" + $currentAppId + "/isMSAApp~/false"

    # print the registered app portal URL for any further navigation
    Write-Host "Successfully registered and configured that app registration for 'WebApp' at `n $webAppPortalUrl" -ForegroundColor Green 
    
    # Update config file for 'webApp'
    # $configFile = $pwd.Path + "\..\appsettings.json"
    $configFile = $pwd.Path + "\..\.env"
    
    $dictionary = @{ "<client id>" = $webAppAadApplication.AppId; "<client secret>" = $webAppAppKey; "<tenant id>" = $tenantName };

    Write-Host "Updating the sample config '$configFile' with the following config values:" -ForegroundColor Yellow 
    $dictionary
    Write-Host "-----------------"

    UpdateTextFile -configFilePath $configFile -dictionary $dictionary

    if ($isOpenSSL -eq 'Y') {
        Write-Host -ForegroundColor Green "------------------------------------------------------------------------------------------------" 
        Write-Host "You have generated certificate using OpenSSL so follow below steps: "
        Write-Host "Install the certificate on your system from current folder."
        Write-Host -ForegroundColor Green "------------------------------------------------------------------------------------------------" 
    }
} # end of ConfigureApplications function

# Pre-requisites

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph")) {
    Install-Module "Microsoft.Graph" -Scope CurrentUser 
}

#Import-Module Microsoft.Graph

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph.Authentication")) {
    Install-Module "Microsoft.Graph.Authentication" -Scope CurrentUser 
}

Import-Module Microsoft.Graph.Authentication

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph.Identity.DirectoryManagement")) {
    Install-Module "Microsoft.Graph.Identity.DirectoryManagement" -Scope CurrentUser 
}

Import-Module Microsoft.Graph.Identity.DirectoryManagement

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph.Applications")) {
    Install-Module "Microsoft.Graph.Applications" -Scope CurrentUser 
}

Import-Module Microsoft.Graph.Applications

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph.Groups")) {
    Install-Module "Microsoft.Graph.Groups" -Scope CurrentUser 
}

Import-Module Microsoft.Graph.Groups

if ($null -eq (Get-Module -ListAvailable -Name "Microsoft.Graph.Users")) {
    Install-Module "Microsoft.Graph.Users" -Scope CurrentUser 
}

Import-Module Microsoft.Graph.Users

$ErrorActionPreference = "Stop"

# Run interactively (will ask you for the tenant ID)

try {
    ConfigureApplications -tenantId $tenantId -environment $azureEnvironmentName
}
catch {
    $_.Exception.ToString() | out-host
    $message = $_
    Write-Warning $Error[0]    
    Write-Host "Unable to register apps. Error is $message." -ForegroundColor White -BackgroundColor Red
}
Write-Host "Disconnecting from tenant"
Disconnect-MgGraph