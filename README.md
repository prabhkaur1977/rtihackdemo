# rtihackdemo — Retail Orders (Real-Time Intelligence)

Demo assets for a **retail orders** Real-Time Intelligence (RTI) scenario in **Microsoft Fabric**.  
The flow is: **simulate retail order/customer events → ingest in Eventhouse → route with Eventstream → land/curate in Lakehouse → trigger actions with Reflex**.

## What’s in this repo

- **RTIDemoLakehouse.Lakehouse/**  
  Lakehouse used for persisted/curated datasets (reporting, analytics, downstream use).

- **Notebook 1- To seed Dimension Tables.Notebook/**  
  Seeds dimension/reference tables (e.g., products, merchants, customers).

- **Notebook 2-RTI Simulate Real-time Customer Events.Notebook/**  
  Generates sample **retail order** and customer activity events for real-time ingestion.

- **RTIDemoEventStream.Eventstream/**  
  Eventstream definition for routing/transforms from event sources to destinations.
  
- **RTIDemoEventHouse.Eventhouse/**  
  Eventhouse definition used to ingest and query streaming events.


- **Sales_Activator/**
  Ship new order if customer satisfaction score is low.

-  **SendNewOrderActivator/**  
  Ship new order if status of order lost.

- **rtiopertionagent.OperationsAgent/**  
  Operational assets to help monitor/run the demo.

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
