# Databricks notebook source
# determine ubuntu os version, mssql odbc driver is based on ubuntu os version
# on ubuntu you need to install the odbc driver manager (unixodb-dev) mssql odbc driver for specific version of ubuntu and pyodbc (python)
# check dbr release notes for version of ubuntu, https://learn.microsoft.com/en-us/azure/databricks/release-notes/runtime/10.4
# configure cluster with init script


# COMMAND ----------

dbutils.fs.put("dbfs:/databricks/scripts/pyodbc-install_18_04.sh", """
#!/bin/bash
echo '#### pyodbc-install_184.sh ####'
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql17
apt-get install python3-pip -y
apt-get install unixodbc-dev -y
/databricks/python3/bin/pip install --user pyodbc
""", True)

# COMMAND ----------

dbutils.fs.put("dbfs:/databricks/scripts/pyodbc-install_20_04.sh", """
#!/bin/bash
echo '#### pyodbc_install_204.sh ####'
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#Ubuntu 20.04
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql17
apt-get install python3-pip -y
apt-get install unixodbc-dev -y
/databricks/python3/bin/pip install --user pyodbc
""", True)

# COMMAND ----------

# MAGIC %sh
# MAGIC cat /dbfs/databricks/scripts/pyodbc-install_20_04.sh

# COMMAND ----------

dbutils.fs.ls('dbfs:/databricks/scripts')

# COMMAND ----------

# might need to run twice to "wake" up Azure SQL DB. 
import pandas as pd
import pyodbc

def load_data_pyodbc(query):
    #Set up the connection
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=gd88etvrt2.database.windows.net;DATABASE=MYDB;UID=SparkUser;PWD=Password1!')
    data_frame = pd.read_sql(query, conn)
    return data_frame

df = load_data_pyodbc('select * from dbo.[pima-indians-diabetes]')
print(df.shape)
display(df)

# COMMAND ----------

# MAGIC %sh
# MAGIC printenv PYTHONPATH
# MAGIC

# COMMAND ----------

import sys
sys.path.append('/databricks/python3/bin')

# COMMAND ----------

import sys
sys.path

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC echo $PYTHONPATH
