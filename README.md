# PYOOL

## Introduction

The core idea of this package is to simplify the use of Python packages 
so that with the shortest number of lines, users can easily produce useable scripts. 

This package is designed to support the use of ODPS service. 

In addition to that, the package also include simple and useful Classes to interact 
with the two most popular databases, MySQL and PostgreSQL. 

Another Class is ChatBot is used to support the connection to Dingtalk allowing user to easily send messages to group chat using Custom ChatBot service.
  
## Installation

It is recommended that user should always update the latest version of the package so bugs 
and other issues can be resolved as well as updates. 

Simply open Command Prompt and input:

`pip install pyool`

  
## Quick Tutorial 
### OdpsConnector
In order to work with ODPS Database, let start by importing OdpsConnector and start a connection. 

```
from pyool import OdpsConnector

odps = OdpsConnector()
odps.connect(accessId = "", accessKey = "", project = "", endPoint = "", tunnelEndPoint = "")
```

In order to connect, user needs to have Access ID, Access Key and provide Project name, a specific End Point and Tunnel End Point

After having all the information, now is the time to run the query: 

`odps.run_query("SELECT 'foo' AS data")`

If the query can run, then we already successfully implement a simple script to run query on ODPS database.

If you really need to extract the data from your ODPS query, let use another function: 

`odps.dump_to_csv("SELECT 'foo' AS data", storage_path = "./your/local/file/path")` 

Storage Path is required to use this function, as the result, a CSV file will be created with all the result of your query.


The path of the downloaded file is returned as the result of dump_to_csv, so from that, you can use for further interaction, such as extracting header from the file so you can upload it onto other Database. 

To do that, here is a simple code to do that:

```
file_path = odps.dump_to_csv("SELECT 'foo' AS data", storage_path = "./your/local/file/path")
file_header = odps.extract_header(file_path) 
``` 



### PostgreSQLConnector

In order to work with PostgreSQL Database, let start with establishing connection: 


```
from pyool import PostgreSQLConnector

postgre_db = PostgreSQLConnector()
postgre_db.connect(db_name = "", host = "", port = "", user = "", password = "") 
```


Afet having the connection establshed, lets try to run some query: 

`postgre_db.run_query("SELECT CURRENT_DATE AS date_time")`


If the script run without any error, then we have successfully know how to run the query. If you want to return the data as the result, just add return_data = True:

`data = postgre_db.run_query("SELECT CURRENT_DATE AS date_time", return_data = True)`

The data returned will be in Dataframe format and ready to be used further. 


Uploading data onto the Database cant be simpler than this, here is how: 

`postgre_db.uploadCsv("./your/file/path", "your_schema.your_table", your_file_header, remove_file = True, truncate = False)`


If you have your data from ODPS, then the function dump_to_csv will return the file path which is convenient to use here. And it is recommended that you get your CSV file header with extract_header function to use in the uploadCSV here. 

Another note, remove_file will remove the CSV file so that you dont have to do it yourself everytime, and **truncate will TRUNCATE the table before uploading so be careful.**





