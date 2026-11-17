
# Project Architecture

## Customer Retention Intelligence Platform

This diagram illustrates the end-to-end workflow, from raw customer data processing to business intelligence and retention decision support.

```mermaid
flowchart TD
    A["Telco Customer Dataset (CSV)"]
    B["Python Data Validation"]
    C["PostgreSQL Database"]
    D["SQL Data Analysis"]
    E["Python EDA and Feature Engineering"]
    F["Customer Analytics"]
    G["KMeans Customer Segmentation"]
    H["Segmentation Results (CSV)"]
    I["Streamlit Application"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    F --> I
    H --> I

    I --> J["Business Overview"]
    I --> K["Churn Analysis"]
    I --> L["Customer Segmentation"]
    I --> M["Retention ROI Simulator"]
```
