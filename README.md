# Grafana Dashboard Backup Tool

Some python programs to call Grafana API to:

* Save every datasource to each datasource file.
	* **saveDatasources.py**
* Save every folder to each datasource file.
	* **saveFolders.py**
* Save every dashboard to each dashboard file.
	* **saveDashboards.py**
* Create datasource from a backup file.
	* **createDatasource.py**
* Create dashboard from a backup file.
	* **createDashboard.py**
* Create folder from a backup file. (supported from Grafana v.5.0.*)
	* **createFolder.py**

There a three convenient script files:

1. **backup_grafana.sh**
2. **restore_dashboards.sh**
3. **restore_datasources.sh**
3. **restore_folders.sh**

you can use them to

1. **backup all datasources, dashboards and folders.**
    * e.g.: sh backup_grafana.sh
2. **restore dashboards from your dashboard backup folder.**
    * e.g: sh restore_dashboards.sh /tmp/dashboards/2016-10-10_12:00:00
3. **restore datasources from your datasource backup folder.**
    * e.g.: sh restore_dashboards.sh /tmp/datasources/2016-10-10_12:00:00
3. **restore folders from your folder backup folder.**
    * e.g.: sh restore_folders.sh /tmp/folders/2016-10-10_12:00:00

[Grafana API document](http://docs.grafana.org/http_api/overview/)

## ENV:
* python 2.7, python 3
	* Need to **pip install requests** library
* Garafana 3.0 API

## Setting

1. Export the environment variables bellow
2. GRAFANA_URL (the default url is http://localhost:3000)
3. GRAFANA_TOKEN

You can see how to get token from here: [Grafana Web page](http://docs.grafana.org/http_api/auth/)

## How to Use
* First edit **grafanaSettings.py** as above.
* Use **saveDashboards.py** to save each dashboard to each file.
	* ex: python saveDashboards.py **folder_path**

* Use **saveDatasources.py** to save each datasources to each file under specific folder.
	*  ex: python saveDatasources.py **folder_path**

* Use **saveFolders.py** to save each folders to each file under specific folder.
	*  ex: python saveFolders.py **folder_path**

* Use **createDashboard.py** to read the dashboard  file and create or update them on Grafana.
 	*  ex: python createDashboard.py **file_path**

* Use **createDatasource.py** to read the datasource  file and create or update them on Grafana.
 	*  ex: python createDatasource.py **file_path**

* Use **createFolder.py** to read the folder file and create or update them on Grafana.
 	*  ex: python createFolder.py **file_path**

* Use **backup_grafana.sh** to backup all your dashboards, datasources and folders to **/tmp** folder.
	* It will create
		* three files: 
		    1. **/tmp/dashboards.tar.gz**
		    2. **/tmp/datasources.tar.gz**
		    3. **/tmp/folders.tar.gz**
		* three folders contain dashboard files, datasource files and folders file:         
		    1. **/tmp/dashboards/$current_time**
		    2. **/tmp/datasources/$current_time** 
		    3. **/tmp/folders/$current_time**
	* e.g.：**sh backup_grafana.sh**
	* result：
	    * **/tmp/dashboads.tar.gz**
	    * **/tmp/datasourcess.tar.gz**
	    * **/tmp/folders.tar.gz**
	    ------
	    * **/tmp/dashboards/2016-10-10_12:00:00**
	    * **/tmp/datasources/2016-10-10_12:00:00**
	    * **/tmp/folders/2016-10-10_12:00:00**
