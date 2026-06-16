# CareIQ System Architecture

This document details the system architecture of **CareIQ — AI-Powered Care Gap Intelligence** using a simplified left-to-right (LR) conceptual structure.

## System Architecture Concept Illustration

![CareIQ System Architecture Illustration](./careiq_system_architecture.png)

## Simplified Left-to-Right Architecture Flow (Mermaid)

```mermaid
flowchart LR
    %% 1. Databricks Lakehouse Block
    subgraph Lakehouse ["Databricks Lakehouse"]
        direction TB
        nhfs5["nfhs5 indicator table"]
        facilities["facilities table"]
        pincodes["pincodes directory"]
    end

    %% 2. Genie Disease Space Agents Blocks
    subgraph Genie ["Genie Agents"]
        direction TB
        genie_anemia["Genie Anemia Care"]
        genie_heart["Genie Heart Care"]
        genie_oncology["Genie Oncology Care"]
        genie_pulmonology["Genie Pulmonology Care"]
        genie_diarrhoea["Genie Diarrhoea Care"]
        genie_immunization["Genie Immunization Care"]
        genie_news["Genie News"]
    end

    %% Connections: Lakehouse to Genie Agents
    Lakehouse --> Genie

    %% 3. Agent Bricks Orchestrator Agent
    orchestrator["Agent Bricks Orchestrator Agent"]

    %% Orchestrator connecting with all Genie agents
    genie_anemia --- orchestrator
    genie_heart --- orchestrator
    genie_oncology --- orchestrator
    genie_pulmonology --- orchestrator
    genie_diarrhoea --- orchestrator
    genie_immunization --- orchestrator
    genie_news --- orchestrator

    %% 4. Agent Bricks Planner Agent and Tools
    planner["Agent Bricks Planner Agent"]
    
    subgraph Tools ["Planner Tools"]
        direction TB
        search_tool["Search Tool"]
        gmaps["Google Maps API"]
    end
    
    search_tool --- planner
    gmaps --- planner

    %% 5. Databricks App Block containing Streamlit App
    subgraph DatabricksApp ["Databricks App"]
        streamlit["Streamlit App"]
    end

    %% Connections from Agents to Streamlit App
    orchestrator --> streamlit
    planner --> streamlit

    %% 6. End User
    user["End User"]

    %% Connection from App to End User
    streamlit <--> user

    %% Stylings for a clean, modern aesthetic
    classDef dbStyle fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef genieStyle fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#fff;
    classDef orchStyle fill:#065f46,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef plannerStyle fill:#78350f,stroke:#f59e0b,stroke-width:2px,color:#fff;
    classDef appStyle fill:#0f172a,stroke:#64748b,stroke-width:2px,color:#fff;
    classDef userStyle fill:#991b1b,stroke:#ef4444,stroke-width:2px,color:#fff;

    class nhfs5,facilities,pincodes dbStyle;
    class genie_anemia,genie_heart,genie_oncology,genie_pulmonology,genie_diarrhoea,genie_immunization,genie_news genieStyle;
    class orchestrator orchStyle;
    class planner,search_tool,gmaps plannerStyle;
    class streamlit appStyle;
    class user userStyle;
```
