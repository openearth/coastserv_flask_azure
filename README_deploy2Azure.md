# Steps to deploy Catchment-Aware LSTMs for Regional Rainfall-Runoff Modelling to Azure

All scripts required for deployment is located in the `deploy_model_to_Azure` folder.
First create the docker container with the file called, `Dockerfile`, then deploy to Azure with the shell script, `deploy.sh`.
Copy the Camels data to a folder named basin_timeseries_v1p2_metForcing_obsFlow and put this in the deploy folder.
The basin_timeseries_v1p2_metForcing_obsFlow should contain mean forcing, attributes etc.

## Prerequisites
- [Docker](https://docs.docker.com/docker-for-windows/install/)
- [An Azure account](https://azure.microsoft.com/en-us/free/search/?&ef_id=CjwKCAjww5r8BRB6EiwArcckC0kzAYGgQyXwjiOD9prVhsSG7vlBgM4FZU3To3evtGv8ah7hqDrXABoCf8AQAvD_BwE:G:s&OCID=AID2100079_SEM_CjwKCAjww5r8BRB6EiwArcckC0kzAYGgQyXwjiOD9prVhsSG7vlBgM4FZU3To3evtGv8ah7hqDrXABoCf8AQAvD_BwE:G:s&dclid=COKSsPzvs-wCFRSkewod9HoGDg)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt)

## Steps to create Docker container
- In Windows Powershell run
```
docker build -t lstmregional.azurecr.io/ealstm:v1 .
```
- Ensure that the image has been created by running 

```
docker images
```
## Steps to deploy container to the cloud
In the Linux subsystem on Windows, run `deploy.sh`
```
./deploy.sh
```
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/