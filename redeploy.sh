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
version=v4
az acr login --name $ACR_NAME
az acr update -n $ACR_NAME --admin-enabled true

docker push coastserv.azurecr.io/coastserv:$version

#restart webapp

az webapp restart --name $APP_NAME --resource-group $ACI_PERS_RESOURCE_GROUP
az webapp config set -g $ACI_PERS_RESOURCE_GROUP -n $APP_NAME --always-on true