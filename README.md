# COASTSERV_Model
A program for nesting coastal DFM and DFMWAQ models in FES tide model output and CMEMS MERCATOR global physiochemical and biogeochemical model output. 
This app is deployd on Azure at coasterv.azurewebsites.net. This readme describes how to create the docker container and deploy the app to Azure.


**other requirements:**
* an Azure account
* a CMEMS account
* a D-FLOW FM *.pli file
* FES data
* Docker Desktop 

# Create the coastserv docker container and deploy on Azure as a webapp
* Clone this repo with 
```bash
git clone https://github.com/openearth/coastserv_flask_azure.git
```
* If on a Windows machine enable docker desktop to be used on the Ubuntu subsystem by going to Setting and checking the option: 'Expose daemon on tpc:...'
* In the Ubuntu terminal, navigate to the git repo, cloned in the step before. Build the docker container with
```bash
docker build --tag coastserv.azurecr.io/coastserv:v6 .
```
* Test the container on your local machine first with:
```bash
docker run -p 80:80 -v D:\PROJECTS\2021\COASTSERV_azure\FES\:/app/app/coastserv/static/FES coastserv.azurecr.io/coastserv:v6
```
Where you replace 'D:\PROJECTS\2021\COASTSERV_azure\FES\' with the path to your FES data.
* In a browser, navigate to 'localhost:80' and run a test by using the test.pli file. 
* If all looks well, push the FES data to Azure and deploy your app with:
```bash
./deploy.sh
```
* In a browser, navigate to coastserv.azurewebsites.net. This might take some time to start if it is the first time you're deploying the container.
* If you make any changes to the code on your local machine, push the changes to Azure with redeploy.sh 


