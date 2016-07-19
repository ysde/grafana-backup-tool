# Grafana Dashboard Backup Tool

Python code to call Grafana API to:

* Save datasources to a local file
* Save dashboards to a local file
* Create datasources from the local file
* Create dashboards from the local file

[Grafana API document](http://docs.grafana.org/http_api/overview/)

## ENV:
* python 2.7
	* Need to pip install requests library
* Garafana 3.0 API

## Setting

1. Export the environment variables bellow
	2. GRAFANA_URL (the default url is http://localhost:3000)
	3. GRAFANA_TOKEN 
        
Remember, you can the token from [Grafana Web page](http://docs.grafana.org/http_api/auth/)

## How to Use
* Use saveDashboards.py to save all dashboards to a file.
	* ex: python saveDashboards.py **file_path**

* Use saveDatasources.py to save all datasources to a file.
	*  ex: python saveDatasources.py **file_path**

* Use createDashboards.py to read the dashboards saved file and create them on Grafana.
 	*  ex: python createDashboards.py **file_path**
