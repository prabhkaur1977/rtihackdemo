# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8e8ddbeb-2fd3-49ea-80f2-145990e6c253",
# META       "default_lakehouse_name": "RTIDemoLakehouse",
# META       "default_lakehouse_workspace_id": "dc8edb26-fad5-4a86-9dae-3ce0cf411f97",
# META       "known_lakehouses": [
# META         {
# META           "id": "8e8ddbeb-2fd3-49ea-80f2-145990e6c253"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Removed invalid comments (SparkSQL does not support # comments)
# MAGIC -- Creating dim_orders from dbo.CustomerEvents, casting columns as required
# MAGIC CREATE TABLE dbo.fact_orders
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   orderId,
# MAGIC   customerid,
# MAGIC   productId,
# MAGIC   merchantId,
# MAGIC   CAST(amount AS DOUBLE)  AS amount,
# MAGIC   CAST(quantity AS INT)   AS quantity,
# MAGIC   paymentMethod,
# MAGIC   currency
# MAGIC FROM dbo.CustomerEvents;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE dbo.dim_events
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   eventID,
# MAGIC   orderID
# MAGIC 
# MAGIC FROM dbo.CustomerEvents;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

