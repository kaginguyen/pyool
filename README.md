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
odps.connect(accessID = "", accessKey = "", project = "", endPoint = "", tunnelEndPoint = "")
```

In order to connect, user needs to have Access ID, Access Key and provide Project name, a specific End Point and Tunnel End Point

After having all the information, now is the time to run the query: 

`odps.run_query("SELECT 'foo' AS data")`

If the query can run, then we already successfully implement a simple script to run query on ODPS database.

If you really need to extract the data from your ODPS query, let use another function: 

`odps.dump_to_csv("SELECT 'foo' AS data", storage_path = "./your/local/file/path")` 

Storage Path is required to use this function, as the result, a CSV file will be created with all the result of your query.

The returning path of the file is returned as the result of dump_to_csv, so from that, you can use for further interaction, such as extracting header from the file so you can upload it onto other Database. 

To do that, here is a simple code to do that:

```
file_path = odps.dump_to_csv("SELECT 'foo' AS data", storage_path = "./your/local/file/path")
file_header = odps.extract_header(file_path) 
``` 

