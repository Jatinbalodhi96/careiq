# CareIQ — AI-Powered Care Gap Intelligence

## Inspiration
Healthcare statistics like high anemia rates, cardiovascular risks, and immunization deficits are often buried inside static database tables (like the NFHS-5 indicators), completely disconnected from the actual healthcare facilities that treat patients. At the same time, field health coordinators planning clinic visits lack visual tools to see where care gaps are most severe, or logistical tools to route visits safely. We wanted to build a unified system that connects demographic health data, nearby facility registry lists, and localized travel logistics into a single, chat-driven workspace.

## What it does
**CareIQ** is an AI-powered Care Gap Intelligence platform. Through a sleek dashboard, users can select a district in India to render an interactive map of health facilities color-coded by their community trust scores and sized by capacity. 
* **Conversational Care Gap Assistant**: Users can ask natural language questions about district health gaps. A Multi-Agent System routes queries to disease specialist agents (e.g., Anemia, Heart Care, Oncology), synthesizes the data, and displays it.
* **Dynamic Visualization**: A Visual Orchestrator agent dynamically writes Python plotting code to render interactive charts for the user in real-time.
* **Visit & Travel Safety Planner**: Once a clinic is selected, a dedicated Logistics Agent simulates routes, ETA, weather, local festivals, traffic delays, and safety context to generate a custom commute itinerary.

## How we built it
* **Application Framework**: Built using **Streamlit** styled with a premium dark theme and hosted on **Databricks Apps** for secure, scalable serverless deployment.
* **Data Lakehouse Layer**: Handled by **Databricks SQL Warehouse**, storing and querying the India Post Pincode directories, clinic registries, and NFHS-5 health indicators.
* **Multi-Agent AI Core**: Built on **Databricks Model Serving (`mas-573924c0-endpoint`)**. We orchestrated prompt instruction sets including a Master Orchestrator, individual Specialist Agents, a Visual Orchestrator, and a Travel Planner Agent.

## Challenges we ran into
* **Dynamic Code Execution**: Generating dynamic chart visualizations on the fly without breaking the Streamlit container. We resolved this by configuring the Visual Orchestrator to output structured, sandbox-safe Python/Plotly instructions that are executed dynamically via `exec()`.
* **Syncing Constraints**: Managing workspace uploads (since Databricks CLI sync treats `.md` and `.sql` extensions as notebooks, causing write access issues). We worked around this by formatting prompt structures as `.txt` files to enable seamless asset synchronization.
* **Orchestration Latency**: Streaming responses across routed agents. We implemented itemized chunk-streaming to keep the user interface responsive and visually interactive.

## Accomplishments that we're proud of
* Deploying a fully functional, production-ready Streamlit app directly inside the Databricks ecosystem in a matter of hours.
* Building a reliable Multi-Agent System where agents dynamically write their own front-end charting code.
* Achieving high-fidelity route planning that integrates real-world travel parameters like monsoon weather advice and localized geopolitical context.

## What we learned
* Deploying applications on **Databricks Apps** is incredibly fast and simplifies secure environment variable and token injection.
* Multi-agent design works best when specialized sub-agents have narrow scopes and strict, structured response schemas (like JSON formatting).
* Conversational interfaces become infinitely more powerful when combined with dynamic, interactive visual components.

## What's next for CareIQ
* **Live API Integrations**: Transitioning from simulated weather, transit delays, and news alerts to real-time Google Maps, OpenWeather, and news feed APIs.
* **Closed-Loop Scheduling**: Allowing coordinators to book patient appointments and direct field dispatches directly from the Care Gap Planner chat.
* **Predictive Indicators**: Integrating machine learning models to forecast future care gaps based on facility workload trends and historical weather-driven access limitations.
