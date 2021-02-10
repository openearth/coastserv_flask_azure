# COASTSERV_Model
A program for nesting coastal DFM and DFMWAQ models in FES tide model output and CMEMS MERCATOR global physiochemical and biogeochemical model output. It includes utilities for downloading and processing the data. 
Designed as a backend for a webapp. **script branch, previously master, is no longer supported. Old FlaskApp branch is now master as of Dec 15 2019.**

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
* In the Ubuntu terminal, navigate to the git repo, cloned in the step before, and run
```bash
./deploy.sh
```
* In a browser, navigate to coastserv.azurewebsites.net. This might take some time to start if it is the first time you're deploying the container.
* If you make any changes to the code on your local machine, push the changes to Azure with redeploy.sh 


