# rtihackdemo — Retail Orders (Real-Time Intelligence)

Demo assets for a **retail orders** Real-Time Intelligence (RTI) scenario in **Microsoft Fabric**.  
The flow is: **simulate retail order/customer events → ingest in Eventhouse → route with Eventstream → land/curate in Lakehouse → trigger actions with Reflex**.

## What’s in this repo

- **RTIDemoLakehouse**  
  Lakehouse used for persisted/curated datasets (reporting, analytics, downstream use).

- **Notebook 1- To seed Dimension Tables**  
  Seeds dimension/reference tables (e.g., products, merchants, customers).

- **Notebook 2-RTI Simulate Real-time Customer Events**  
  Generates sample **retail order** and customer activity events for real-time ingestion.

- **RTIDemoEventStream**  
  Eventstream definition for routing/transforms from event sources to destinations.
  
  <img width="1086" height="230" alt="image" src="https://github.com/user-attachments/assets/c27d16d9-1366-419a-a412-1a3a28f9ca51" />

  
- **RTIDemoEventHouse**  
  Eventhouse definition used to ingest and query streaming events.

- **Create Update Policy**
  Create update policy to load data from Bronze to Silver to Gold Layer.
  

  <img width="818" height="251" alt="image" src="https://github.com/user-attachments/assets/57aa01a2-9d5c-4205-b45b-28d6c6f8bf44" />

- **Realtime Dashboard**
  To monitor realtime status

  <img width="1530" height="903" alt="image" src="https://github.com/user-attachments/assets/0fffbfe9-af24-40ae-bbe1-9c39f0a5015c" />


- **Sales_Activator**
  Ship new order if customer satisfaction score is low.

-  **SendNewOrderActivator**  
  Ship new order if status of order is lost.

- **rtiopertionagent.OperationsAgent**  
  Operational assets to help monitor/run the demo.

  <img width="1782" height="880" alt="image" src="https://github.com/user-attachments/assets/80e22118-23d2-4061-ac83-83287ef931e3" />


## Prerequisites

- A **Microsoft Fabric** workspace with access to **Real-Time Intelligence** features (Eventstream, Eventhouse)
- Permission to create/import:
  - Notebooks
  - Eventstreams
  - Eventhouses
  - Lakehouses
  - Reflex activators

## Quick start (recommended order)

1. Import/clone this repository into your Fabric workspace (or download and import the items).
2. Create/select your target **Lakehouse** and **Eventhouse** (if the imported items don’t already bind to existing ones).
3. Run Notebook 1 **Seed Dimension Tables** to populate retail dimension data.
4. Configure/start **RTIDemoEventStream.Eventstream** and confirm it’s connected to destinations.
5. Run Notebook 2 **RTI Simulate Real-time Customer Events** to start sending **retail order events**.
6. Validate ingestion in **RTIDemoEventHouse.Eventhouse** (events arriving, schema as expected).
7. Verify data landing/curation in **RTIDemoLakehouse.Lakehouse**.
8. Enable **sales_activator** & **SendNewOrderActivator** to trigger actions when conditions are met.

## Notes

- Folder names ending in `.Notebook`, `.Eventhouse`, `.Eventstream`, `.Lakehouse`, `.Reflex`, `.OperationsAgent` are Fabric item export formats.
- If you rename items in Fabric after import, update any references inside notebooks/definitions accordingly.

## Contributing

PRs and suggestions are welcome.
