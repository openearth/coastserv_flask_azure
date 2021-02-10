#!/bin/bash
##write file with python to a blob storage: https://stackoverflow.com/questions/50014827/write-python-dataframe-as-csv-into-azure-blob
# Change these four parameters as needed
ACR_NAME=coastserv
ACI_PERS_RESOURCE_GROUP=coastserv
ACI_PERS_STORAGE_ACCOUNT_NAME=$ACR_NAME
ACI_PERS_LOCATION=westeurope
ACI_PERS_SHARE_NAME=acishare
APP_SERVICE_PLAN=AppSvc-coastserv-plan
APP_NAME=coastserv

RES_GROUP=$ACR_NAME # Resource Group name

# Create the resource group
echo 'creating resource group'
az group create --name=$ACR_NAME --location=westeurope --output table
echo 'creating storage account'
# Create the storage account with the parameters
az storage account create \
--resource-group $ACI_PERS_RESOURCE_GROUP \
--name $ACI_PERS_STORAGE_ACCOUNT_NAME \
--location $ACI_PERS_LOCATION \
--sku Standard_LRS

# Create the file share
echo 'creating file share'
az storage share create \
  --name $ACI_PERS_SHARE_NAME \
  --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME
echo 'creating storage key'
STORAGE_KEY=$(az storage account keys list --resource-group $ACI_PERS_RESOURCE_GROUP --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" --output tsv)
echo $STORAGE_KEY

echo 'uploading files to azure fileshare'
FILEUPLOADS=FES

az storage file upload-batch \
  --destination $ACI_PERS_SHARE_NAME \
  --source $FILEUPLOADS \
  --account-key  $STORAGE_KEY \
  --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME 

# Create container registry
echo 'create container registry'
az acr create --resource-group $RES_GROUP --name $ACR_NAME --sku Standard --location westeurope --admin-enabled true

az acr login --name $ACR_NAME
az acr update -n $ACR_NAME --admin-enabled true
docker push $ACR_NAME.azurecr.io/coastserv:v4

##to check that the image is in the registry: 
echo 'checking that repo exists:'
az acr repository list --name $ACR_NAME --output table
# Create App service plan
echo 'creating app service plan'
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $ACI_PERS_RESOURCE_GROUP --is-linux
#~ # Create the webapp
echo 'creating webapp'
az webapp create --resource-group $ACI_PERS_RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $APP_NAME --deployment-container-image-name coastserv.azurecr.io/coastserv:v4
echo 'setting port to a number expected by the web app code'
az webapp config appsettings set --resource-group $ACI_PERS_RESOURCE_GROUP --name $APP_NAME --settings WEBSITES_PORT=80
# grant permissions to the web app to access other Azure resources without needing any specific credentials.
echo 'retrieving Principal ID'
PrincipalID=$(az webapp identity assign --resource-group  $ACI_PERS_RESOURCE_GROUP --name $APP_NAME --query principalId --output tsv)
echo $PrincipalID
# retrieve subscription ID
echo 'retrieving subscription ID'
SubscriptionID=$(az account show --query id --output tsv)
echo $SubscriptionID
# Grant the web app permission to access the container registry
echo 'granting web app permisions to access Azure resources'
az role assignment create --assignee $PrincipalID --scope /subscriptions/$SubscriptionID/resourceGroups/$ACI_PERS_RESOURCE_GROUP/providers/Microsoft.ContainerRegistry/registries/coastserv --role "AcrPull"
# Connect fileshare
echo 'connecting fileshare'
#--custom-id coastserv-volume-mount
az webapp config storage-account add --resource-group $ACI_PERS_RESOURCE_GROUP --name $APP_NAME --custom-id FES --storage-type AzureFiles --share-name  $ACI_PERS_SHARE_NAME --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME --access-key $STORAGE_KEY --mount-path /app/app/coastserv/static/FES
# Deploy app
az webapp config container set --name $APP_NAME --resource-group $ACI_PERS_RESOURCE_GROUP --docker-custom-image-name coastserv.azurecr.io/coastserv:v4 --docker-registry-server-url https://coastserv.azurecr.io
az webapp config set -g $ACI_PERS_RESOURCE_GROUP -n $APP_NAME --always-on true
##username jwilms pw: qUANTUM28*0