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

# # Seed Dimension Tables
# This notebook generates synthetic dimension tables for a retail analytics scenario—`dim_Customers`, `dim_Products`, and `dim_Merchants`—using PySpark, and saves them as Delta tables for downstream processing.

# MARKDOWN ********************


# MARKDOWN ********************

# ## Pre-requisite
# Add the `lh_NovaMart` lakehouse to this notebook as the default lakehouse:
# 1. Click on the `Add data items` option on the left and select `Existing data sources`.
# 2. Choose the `lh_NovaMart` lakehouse.
# 3. Clicking on the three dots beside it once it's added and click on `Set as default lakehouse`.

# MARKDOWN ********************

# ### Setup — Dimension Sizes
# **Purpose:** Define the sizes for customer, product, and merchant dimensions. Keep these in sync with any streaming/related sections.


# CELL ********************

from pyspark.sql import functions as F

NUM_CUSTOMERS = 1000
NUM_PRODUCTS  = 200
NUM_MERCHANTS = 50


# Drop existing dimension tables if they exist
spark.sql("DROP TABLE IF EXISTS dim_Customers")
spark.sql("DROP TABLE IF EXISTS dim_Products")
spark.sql("DROP TABLE IF EXISTS dim_Merchants")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# 
# ### Build `dim_Customers` DataFrame
# **Purpose:** Create a synthetic customers dimension with IDs, names, regions, and loyalty tiers using deterministic randomness for reproducibility.

# CELL ********************


customers_df = (
    spark.range(1, NUM_CUSTOMERS + 1).toDF("id")
    .withColumn("customerId",  F.format_string("C%06d", F.col("id")))
    .withColumn("customerName",F.concat(F.lit("Customer "), F.format_string("%06d", F.col("id"))))
    .withColumn("region",
        F.when(F.rand(1) < 0.25, "NA")
         .when(F.rand(2) < 0.50, "EU")
         .when(F.rand(3) < 0.75, "APAC")
         .otherwise("LATAM")
    )
    .withColumn("loyaltyTier",
        F.when(F.rand(4) < 0.60, "Standard")
         .when(F.rand(5) < 0.85, "Gold")
         .otherwise("Platinum")
    )
    .select("customerId", "customerName", "region", "loyaltyTier")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# 
# ### Persist `dim_Customers` to Delta
# **Purpose:** Overwrite and save the customers dimension as a managed Delta table named `dim_Customers`.

# CELL ********************

customers_df.write.mode("overwrite").format("delta").saveAsTable("dim_Customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Build `dim_Products` DataFrame (Category & Price)
# **Purpose:** Create a synthetic products dimension with IDs, names, categories sampled from a list, and base prices in the $10–$500 range.

# CELL ********************

categories = ["Electronics","Fashion","Home","Beauty","Toys","Grocery"]
category_expr = F.element_at(F.array(*[F.lit(c) for c in categories]),
                             (F.floor(F.rand(6) * len(categories)) + 1).cast("int"))

products_df = (
    spark.range(1, NUM_PRODUCTS + 1).toDF("id")
    .withColumn("productId",   F.format_string("PRD%04d", F.col("id")))
    .withColumn("productName", F.concat(F.lit("Product "), F.format_string("%04d", F.col("id"))))
    .withColumn("category",    category_expr)
    .withColumn("basePrice",   F.round(F.rand(7) * F.lit(490.0) + F.lit(10.0), 2))  # $10–$500
    .select("productId", "productName", "category", "basePrice")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Persist `dim_Products` to Delta
# **Purpose:** Overwrite and save the products dimension as a managed Delta table named `dim_Products`.

# CELL ********************

products_df.write.mode("overwrite").format("delta").saveAsTable("dim_Products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# 
# ### Build `dim_Merchants` DataFrame (Industry & Region)
# **Purpose:** Create a synthetic merchants dimension with IDs, names, industries, and regions sampled from predefined lists.

# CELL ********************

industries = ["Retail","Marketplace","Brand","Distributor"]
industry_expr = F.element_at(F.array(*[F.lit(i) for i in industries]),
                             (F.floor(F.rand(8) * len(industries)) + 1).cast("int"))

merchant_regions = ["NA","EU","APAC","LATAM"]
mregion_expr = F.element_at(F.array(*[F.lit(r) for r in merchant_regions]),
                            (F.floor(F.rand(9) * len(merchant_regions)) + 1).cast("int"))

merchants_df = (
    spark.range(1, NUM_MERCHANTS + 1).toDF("id")
    .withColumn("merchantId",   F.format_string("M%04d", F.col("id")))
    .withColumn("merchantName", F.concat(F.lit("Merchant "), F.format_string("%04d", F.col("id"))))
    .withColumn("industry",     industry_expr)
    .withColumn("region",       mregion_expr)
    .select("merchantId", "merchantName", "industry", "region")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Persist `dim_Merchants` to Delta
# **Purpose:** Overwrite and save the merchants dimension as a managed Delta table named `dim_Merchants`.

# CELL ********************

merchants_df.write.mode("overwrite").format("delta").saveAsTable("dim_Merchants")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Quick Sanity Checks
# **Purpose:** Purpose: Verify that the dimension tables were created successfully and contain expected sample data.

# CELL ********************

print("Dimension tables created:")
for t in ["dim_Customers","dim_Products","dim_Merchants"]:
    spark.table(t).show(5, truncate=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
