# RTI Demo - Detailed Architecture Documentation

This document provides comprehensive architecture diagrams and component details for the RTI Demo solution.

---

## End-to-End Data Flow Architecture

```mermaid
flowchart TB
    subgraph "Data Generation Layer"
        NB1["📓 Notebook 1:<br/>Seed Dimension Tables"]
        NB2["📓 Notebook 2:<br/>Simulate Customer Events"]
        NB1 --> DimTables["Dimension Tables<br/>• dim_customers<br/>• dim_products<br/>• dim_merchants<br/>• dim_events"]
    end

    subgraph "Streaming Ingestion Layer"
        NB2 --> EventGen["Event Generator<br/>(Python)"]
        EventGen --> EventStream["🔄 RTI EventStream<br/>(Routing & Transform)"]
    end

    subgraph "Hot Path - Real-Time Processing"
        EventStream --> EventHouse["🏢 RTI EventHouse<br/>(KQL Database)"]
        EventHouse --> Bronze["Bronze Layer<br/>(Raw Events)"]
        Bronze -->|Update Policy| Silver["Silver Layer<br/>(Cleansed Data)"]
        Silver -->|Update Policy| Gold["Gold Layer<br/>(Aggregated)"]
    end

    subgraph "Cold Path - Analytical Storage"
        EventStream --> Lakehouse["🏢 RTI Lakehouse"]
        Lakehouse --> LH_Tables["Lakehouse Tables<br/>• CustomerEvents<br/>• fact_orders<br/>• gold_CustomerEvents"]
        DimTables -.->|Reference Data| LH_Tables
    end

    subgraph "Action Layer - Reflex Activators"
        Gold --> Activator1["⚡ Sales_Activator<br/>(Low Satisfaction Alert)"]
        Gold --> Activator2["⚡ SendNewOrder_Activator<br/>(Lost Order Recovery)"]
        Activator1 --> Action1["📧 Send Notification"]
        Activator2 --> Action2["📦 Ship New Order"]
    end

    subgraph "Analytics & Monitoring Layer"
        Gold --> RTDash["📊 Real-time Dashboard<br/>(Streaming Metrics)"]
        LH_Tables --> SemanticModel["📐 Semantic Model"]
        SemanticModel --> Analytics["📊 Analytics Dashboard<br/>• Total Sales<br/>• Avg Satisfaction<br/>• Product Qty"]
    end

    subgraph "AI Operations Layer"
        RTDash --> Agent["🤖 Operations Agent<br/>(Monitoring & Ops)"]
        EventHouse --> Agent
        Lakehouse --> Agent
    end

    style EventGen fill:#e1f5ff
    style EventStream fill:#fff4e1
    style EventHouse fill:#ffe1f5
    style Lakehouse fill:#e1ffe1
    style Bronze fill:#ffebcc
    style Silver fill:#cce5ff
    style Gold fill:#ffffcc
    style RTDash fill:#f0e1ff
    style Agent fill:#e1ffe8
```

---

## Data Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant NB as Notebook 2
    participant ES as EventStream
    participant EH as EventHouse
    participant LH as Lakehouse
    participant RA as Reflex Activators
    participant Dash as Dashboards

    Note over NB: Generate Event
    NB->>ES: Send retail order event
    
    par Hot Path
        ES->>EH: Stream to EventHouse
        EH->>EH: Bronze → Silver → Gold
        EH->>RA: Check activation rules
        alt Low Satisfaction
            RA->>RA: Trigger Sales_Activator
        end
        alt Lost Order
            RA->>RA: Trigger SendNewOrder_Activator
        end
        EH->>Dash: Update Real-time Dashboard
    and Cold Path
        ES->>LH: Stream to Lakehouse
        LH->>LH: Store in Delta tables
        LH->>Dash: Feed Semantic Model
    end
```

---

## Component Details

### 1️⃣ Data Generation Layer
- **Notebook 1: Seed Dimension Tables**
  - Creates reference/dimension tables
  - Tables: `dim_customers`, `dim_products`, `dim_merchants`, `dim_events`
  - One-time setup for master data

- **Notebook 2: Simulate Customer Events**
  - Generates realistic retail order events
  - Simulates customer behavior patterns
  - Configurable event rate and volume

### 2️⃣ Streaming Ingestion Layer
- **RTI EventStream**
  - Captures events in real-time
  - Routes to multiple destinations (hot & cold paths)
  - Performs light transformations
  - Schema validation

### 3️⃣ Hot Path - EventHouse (Real-Time)
- **RTI EventHouse (KQL Database)**
  - Ultra-low latency ingestion
  - KQL query capabilities
  - Update policies for data transformation
  
- **Medallion Architecture:**
  - **Bronze Layer**: Raw event ingestion (high velocity)
  - **Silver Layer**: Cleansed, validated data
  - **Gold Layer**: Business-level aggregations

### 4️⃣ Cold Path - Lakehouse (Analytics)
- **RTI Lakehouse**
  - Parquet/Delta format for analytics
  - Integration with dimension tables
  - Tables: `CustomerEvents`, `fact_orders`, `gold_CustomerEvents`
  - Optimized for complex queries and ML

### 5️⃣ Action Layer - Reflex Activators
- **Sales_Activator**
  - Trigger: Customer satisfaction score < threshold
  - Action: Send alert/notification to sales team
  
- **SendNewOrder_Activator**
  - Trigger: Order status = "lost"
  - Action: Automatically ship replacement order

### 6️⃣ Analytics & Monitoring
- **Real-time Dashboard**
  - Live streaming metrics
  - Event throughput monitoring
  - System health indicators
  
- **Semantic Model & Analytics Dashboard**
  - Total sales amount
  - Average customer satisfaction score
  - Product quantity metrics
  - Trend analysis

### 7️⃣ AI Operations
- **Operations Agent**
  - AI-powered monitoring
  - Automated troubleshooting
  - Proactive recommendations

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Event Generation** | PySpark, Python | Simulate retail events |
| **Ingestion** | Fabric EventStream | Real-time event routing |
| **Hot Storage** | Fabric EventHouse (KQL) | Low-latency queries |
| **Cold Storage** | Fabric Lakehouse (Delta) | Analytical workloads |
| **Transformation** | KQL Update Policies | Bronze → Silver → Gold |
| **Actions** | Fabric Reflex | Event-driven automation |
| **Visualization** | Power BI, Real-time Dash | Analytics & monitoring |
| **AI/ML** | Operations Agent | Intelligent operations |

---

## Key Features

✅ **Real-time Processing**: Sub-second latency from event to insight  
✅ **Lambda Architecture**: Hot path (EventHouse) + Cold path (Lakehouse)  
✅ **Medallion Design**: Bronze → Silver → Gold data quality layers  
✅ **Event-Driven Actions**: Automated responses via Reflex  
✅ **Scalability**: Handles high-velocity streaming data  
✅ **AI-Powered Ops**: Intelligent monitoring and troubleshooting  
✅ **End-to-End Observability**: Dashboards at every layer

---

## Design Patterns

### Lambda Architecture
The solution implements Lambda Architecture with:
- **Hot Path (Speed Layer)**: EventHouse for real-time analytics
- **Cold Path (Batch Layer)**: Lakehouse for comprehensive analysis
- **Serving Layer**: Dashboards and semantic models

### Medallion Architecture
Data quality improves through layers:
- **Bronze**: Raw, unprocessed data from event sources
- **Silver**: Validated, cleansed, and deduplicated data
- **Gold**: Business-level aggregated and enriched data

### Event-Driven Architecture
- Events trigger automated actions via Reflex
- Decoupled components communicate through EventStream
- Asynchronous processing for scalability

---

**Architecture Version**: 1.0  
**Last Updated**: March 27, 2026
