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

# MARKDOWN ********************

# # Simulate Real-time Customer Events

# MARKDOWN ********************

# ## Pre-requisites
# - Add `lh_NovaMart` lakehouse to this notebook following same steps from notebook 1.
# - Retrieve the **connection string** from the Eventstream for the Setup section
#     - In your workspace, go to Lab\Ingestion and locate the `es_CustomerEvents` Eventstream 
#     - In `CustomerEvents-Source`, go to Details -> SAS Key Authentication and copy the `Connection string-primary key` (note down the `Endpoint`, `SharedAccessKeyName`, `SharedAccessKey` and `EntityPath` inside this connection string).

# MARKDOWN ********************

# ## Setup
# Configuration defaults for Event Hubs, rows per second, and checkpoint location.

# CELL ********************

# PROVIDE VALUES from the Connection string-primary key noted down
namespace =  #"<namespace-in-endpoint (value between 'sb://' and '.servicebus.windows.net/')>"
key_name =  #"<shared-access-key-name>"
key_value =  #"<shared-access-key>"
entity_path = #"<entity-path (event-hub-name)>"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

checkpoint_location = "Files/checkpoints/ecom-orders"

ROWS_PER_SECOND = 5

event_hubs_connection_string = (
    f"Endpoint=sb://{namespace}.servicebus.windows.net/;"
    f"SharedAccessKeyName={key_name};"
    f"SharedAccessKey={key_value};"
    f"EntityPath={entity_path}"
)

print("Configuration:")
print(f"- rows_per_second: {ROWS_PER_SECOND}")
print(f"- checkpoint_location: {checkpoint_location}")
print("- event_hubs_connection_string: (hidden)")

try:
    if mssparkutils.fs.exists(checkpoint_location):
        mssparkutils.fs.rm(checkpoint_location, True)
        print("Checkpoint reset.")
    else:
        mssparkutils.fs.mkdirs(checkpoint_location)
        print("Checkpoint created.")
except Exception as e:
    print(f"Checkpoint reset skipped or failed: {e}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Imports
# Import core PySpark functions and Python standard libraries used throughout the notebook.

# CELL ********************

from pyspark.sql import functions as F, types as T
import random

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Read Dimension Tables and Broadcast Keys
# Load `customer`, `product`, and `merchant` dimension tables; collect IDs/prices to the driver; and broadcast them to executors for efficient random event generation.

# CELL ********************

customers_df = spark.table("dim_Customers").select("customerId")
products_df  = spark.table("dim_Products").select("productId", "basePrice")
merchants_df = spark.table("dim_Merchants").select("merchantId")

customer_ids = [r.customerId for r in customers_df.collect()]
product_rows = [(r.productId, r.basePrice) for r in products_df.collect()]
merchant_ids = [r.merchantId for r in merchants_df.collect()]

bc_customers = spark.sparkContext.broadcast(customer_ids)
bc_products  = spark.sparkContext.broadcast(product_rows)
bc_merchants = spark.sparkContext.broadcast(merchant_ids)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Define Order Event Generator UDF and Output Schema
# Create a Python function that synthesizes realistic order events using broadcasted dimensions, declare the output schema, and register it as a UDF.


# CELL ********************

import random
import uuid

SUCCESS_STATUS_SEQUENCE = ["ORDERED", "PAID", "DELIVERED"]
LOST_STATUS_SEQUENCE = ["ORDERED", "PAID", "LOST"]

# 0 is <1%, 5 is 50%, and the remaining weights are spread across 1..4.
SATISFACTION_VALUES = [0, 1, 2, 3, 4, 5]
SATISFACTION_WEIGHTS = [0.5, 12.0, 12.5, 12.0, 13.0, 50.0]


def generate_order_events(value):
    customers = bc_customers.value
    products = bc_products.value
    merchants = bc_merchants.value

    order_id = f"O{value:09d}"
    customer_id = random.choice(customers)
    product_id, base_price = random.choice(products)
    merchant_id = random.choice(merchants)
    quantity = random.randint(1, 5)
    amount = round(base_price * quantity, 2)
    payment_method = random.choice(["CARD", "WALLET", "BANK"])

    customer_satisfaction = random.choices(
        SATISFACTION_VALUES,
        weights=SATISFACTION_WEIGHTS,
        k=1
    )[0]

    # Keep LOST events rare: each order has a randomly selected loss chance in [2%, 5%].
    loss_chance = random.uniform(0.02, 0.05)
    status_sequence = LOST_STATUS_SEQUENCE if random.random() < loss_chance else SUCCESS_STATUS_SEQUENCE

    common_payload = {
        "orderId": order_id,
        "amount": amount,
        "quantity": quantity,
        "paymentMethod": payment_method,
        "currency": "USD",
        "customerId": customer_id,
        "productId": product_id,
        "merchantId": merchant_id,
        "customerSatisfaction": customer_satisfaction,
        "source": "simulator",
        "schemaVersion": "1.0",
    }

    return [
        {
            "eventId": str(uuid.uuid4()),
            "eventTime": None,
            "status": status,
            **common_payload,
        }
        for status in status_sequence
    ]


schema = T.StructType([
    T.StructField("eventId", T.StringType()),
    T.StructField("eventTime", T.TimestampType()),
    T.StructField("orderId", T.StringType()),
    T.StructField("status", T.StringType()),
    T.StructField("amount", T.DoubleType()),
    T.StructField("quantity", T.IntegerType()),
    T.StructField("paymentMethod", T.StringType()),
    T.StructField("currency", T.StringType()),
    T.StructField("customerId", T.StringType()),
    T.StructField("productId", T.StringType()),
    T.StructField("merchantId", T.StringType()),
    T.StructField("customerSatisfaction", T.IntegerType()),
    T.StructField("source", T.StringType()),
    T.StructField("schemaVersion", T.StringType())
])

generate_order_events_udf = F.udf(generate_order_events, T.ArrayType(schema))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Build Streaming Source and Enrich with Generated Events
# Create a rate stream for ticks, apply the UDF to synthesize events, and set the event time from the stream timestamp.

# CELL ********************

# Rebuild streaming event logic so that generate_order_events_udf is applied BEFORE posexplode.
# The key issue in prior logic was attempting to posexplode a non-existent 'events' column (it is only created after applying the UDF).
# Correct approach: First, create 'events' column from UDF, then use posexplode.

# 1. Create the 'events' column on ticks using the UDF
# 2. Use posexplode to flatten the array result into (statusStep, event)
# 3. Add eventTime based on timestamp and statusStep, then clean up intermediate columns

ticks = (
    spark.readStream.format("rate")
        .option("rowsPerSecond", ROWS_PER_SECOND)
        .load()
)

events = (
    ticks
    .withColumn("events", generate_order_events_udf(F.col("value")))
    .select("timestamp", "events")
    .select(
        "timestamp",
        F.posexplode(F.col("events")).alias("statusStep", "event")
    )
    .select(
        "timestamp",
        "statusStep",
        "event.*"
    )
    .withColumn(
        "eventTime",
        (F.col("timestamp").cast("long") + (F.col("statusStep") * F.lit(60))).cast("timestamp")
    )
    .drop("timestamp", "statusStep")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Serialize Events to JSON
# Convert each event row to a JSON payload encoded as binary under the `body` column to match Event Hubs sink expectations.

# CELL ********************

out_df = events.select(F.to_json(F.struct([F.col(c) for c in events.columns])).cast("binary").alias("body"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Write Stream
# Starts the streaming job that sends simulated order events into **Eventstream** in Microsoft Fabric and lets it run for **up to n minutes**.

# CELL ********************

try:
    encrypted = spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(event_hubs_connection_string)
    eh_conf = {"eventhubs.connectionString": encrypted}
except Exception:
    eh_conf = {"eventhubs.connectionString": event_hubs_connection_string}

query = (
    out_df.writeStream
    .format("eventhubs")
    .options(**eh_conf)
    .option("checkpointLocation", checkpoint_location)
    .outputMode("append")
    .start()
)

run_minutes = 10
 
#60  # change this to adjust how long the stream runs

timeout_ms = run_minutes * 60 * 1000

terminated = query.awaitTermination(timeout_ms)
if not terminated:
    query.stop()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
