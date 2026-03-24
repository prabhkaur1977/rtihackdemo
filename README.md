# rtihackdemo — Retail Orders (Real-Time Intelligence)

Demo assets for a **retail orders** Real-Time Intelligence (RTI) scenario in **Microsoft Fabric**.  
The flow is: **simulate retail order/customer events → ingest in Eventhouse → route with Eventstream → land/curate in Lakehouse → trigger actions with Reflex**.

## What’s in this repo

- **1. Seed Dimension Tables.Notebook/**  
  Seeds dimension/reference tables (e.g., products, stores, customers).

- **RTI Simulate Real-time Customer Events.Notebook/**  
  Generates sample **retail order** and customer activity events for real-time ingestion.

- **RTIDemoEventHouse.Eventhouse/**  
  Eventhouse definition used to ingest and query streaming events.

- **RTIDemoEventStream.Eventstream/**  
  Eventstream definition for routing/transforms from event sources to destinations.

- **RTIDemoLakehouse.Lakehouse/**  
  Lakehouse used for persisted/curated datasets (reporting, analytics, downstream use).

- **sales_activator.Reflex/** and **SendNewOrderActivator.Reflex/**  
  Reflex activators that can trigger actions based on **retail order conditions** (e.g., new order, high-value order, inventory/store rules).

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
3. Run **1. Seed Dimension Tables.Notebook** to populate retail reference/dimension data.
4. Configure/start **RTIDemoEventStream.Eventstream** and confirm it’s connected to destinations.
5. Run **RTI Simulate Real-time Customer Events.Notebook** to start sending **retail order events**.
6. Validate ingestion in **RTIDemoEventHouse.Eventhouse** (events arriving, schema as expected).
7. Verify data landing/curation in **RTIDemoLakehouse.Lakehouse**.
8. Enable **sales_activator.Reflex** / **SendNewOrderActivator.Reflex** to trigger actions when conditions are met.

## Notes

- Folder names ending in `.Notebook`, `.Eventhouse`, `.Eventstream`, `.Lakehouse`, `.Reflex`, `.OperationsAgent` are Fabric item export formats.
- If you rename items in Fabric after import, update any references inside notebooks/definitions accordingly.

## Contributing

PRs and suggestions are welcome.
