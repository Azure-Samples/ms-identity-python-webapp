# Read in the variables from .env
source .env

# Delete the app registration
echo "Attempting to delete app with ID $CLIENT_ID"
az ad app delete --id $CLIENT_ID

# Find and delete the service principal for that app registration
sp_id=$(az ad sp list --filter "appId eq '"$CLIENT_ID"'" --query "[0].id" --output tsv)

if [ -z "$sp_id" ]; then
    echo "Service principal with ID $sp_id does not exist."
    exit 1
else
    echo "Attempting to delete service principal with ID $sp_id"
    az ad sp delete --id $sp_id
fi

echo "All associated resources are cleaned up."