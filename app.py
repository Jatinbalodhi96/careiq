import os
import streamlit as st
import pandas as pd
import json
from databricks import sql
from openai import OpenAI

st.set_page_config(
    page_title="CareIQ — AI-Powered Care Gap Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Databricks Connection Details
# Simple env var resolution — works both locally and on Databricks Apps.
DATABRICKS_HOST      = os.environ.get("DATABRICKS_HOST", "dbc-d9de43da-bb2e.cloud.databricks.com")
DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH", "/sql/1.0/warehouses/ce1f9f3ece6a0c69")
DATABRICKS_TOKEN     = os.environ.get("DATABRICKS_TOKEN", "")  # Set via env var or Databricks Apps runtime


# Initialize Databricks OpenAI client for supervisor agent
openai_client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url=f"https://{DATABRICKS_HOST}/serving-endpoints"
)

# Initialize Session State
if "should_plot" not in st.session_state:
    st.session_state.should_plot = False
if "current_plot_code" not in st.session_state:
    st.session_state.current_plot_code = None
if "district_plot" not in st.session_state:
    st.session_state.district_plot = None
if "mapped_facilities" not in st.session_state:
    st.session_state.mapped_facilities = []
if "selected_district_name" not in st.session_state:
    st.session_state.selected_district_name = "Ghaziabad"
if "travel_plan_data" not in st.session_state:
    st.session_state.travel_plan_data = None

def generate_travel_plan(facility_name, origin_district):
    current_time_str = "Tuesday, June 16, 2026, 10:15 AM" # Morning commute context
    try:
        with open("genie_instructions/genie_space_travel_planner_instructions.txt", "r") as f:
            travel_prompt = f.read()
        
        user_content = f"""
        Generate travel safety and visit plan:
        Target Destination Facility: {facility_name}
        Patient Origin District: {origin_district}
        Current Local Time Context: {current_time_str}
        """
        
        response = openai_client.responses.create(
            model="mas-573924c0-endpoint",
            input=[
                {"role": "system", "content": travel_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        
        vis_text = " ".join(
            getattr(content, "text", "") 
            for output in response.output 
            for content in getattr(output, "content", [])
        ).strip()
        
        if vis_text.startswith("```json"):
            vis_text = vis_text[7:]
        if vis_text.endswith("```"):
            vis_text = vis_text[:-3]
        vis_text = vis_text.strip()
        
        return json.loads(vis_text)
    except Exception as e:
        print(f"Error calling Travel Planner Agent: {e}")
        return {}

@st.cache_data(ttl=3600)
def fetch_data(query):
    try:
        with sql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=DATABRICKS_HTTP_PATH,
            access_token=DATABRICKS_TOKEN,
            _tls_no_verify=True
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                return pd.DataFrame(data, columns=columns)
    except Exception as e:
        print(f"Error connecting to Databricks: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_districts():
    try:
        df = pd.read_csv("nfhs_5_district_health_indicators.csv")
        return sorted(df["district_name"].dropna().str.strip().unique())
    except Exception as e:
        print(f"Error loading local districts: {e}")
        return ["Ghaziabad", "Bathinda", "Nicobars"]

def fetch_facilities_for_district(district_name):
    district_name = district_name.strip()
    query = f"""
    SELECT 
        f.name as facility_name, 
        COALESCE(try_cast(f.latitude as double), 0.0) as latitude, 
        COALESCE(try_cast(f.longitude as double), 0.0) as longitude,
        COALESCE(try_cast(f.engagement_metrics_n_followers as double), 50.0) as trust_score
    FROM databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset.facilities f
    JOIN databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset.india_post_pincode_directory p
      ON regexp_replace(f.address_zipOrPostcode, '[^0-9]', '') = CAST(p.pincode AS STRING)
    WHERE TRIM(UPPER(p.district)) = UPPER('{district_name}')
    """
    df = fetch_data(query)
    if not df.empty:
        df = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]
    
    # Fallback to matching city name if join is empty
    if df.empty:
        query_fallback = f"""
        SELECT 
            name as facility_name, 
            COALESCE(try_cast(latitude as double), 0.0) as latitude, 
            COALESCE(try_cast(longitude as double), 0.0) as longitude,
            COALESCE(try_cast(engagement_metrics_n_followers as double), 50.0) as trust_score
        FROM databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset.facilities
        WHERE TRIM(UPPER(address_city)) = UPPER('{district_name}')
        """
        df = fetch_data(query_fallback)
        if not df.empty:
            df = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]
    return df

def fetch_health_indicators(district_name):
    district_name = district_name.strip()
    query = f"""
    SELECT 
        all_w15_49_who_are_anaemic_pct,
        w15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct,
        w15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct
    FROM databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset.nfhs_5_district_health_indicators
    WHERE TRIM(UPPER(district_name)) = UPPER('{district_name}')
    """
    return fetch_data(query)

# Premium Theme Styling
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Hide Streamlit Deploy button, header, and footer */
    [data-testid="stHeader"] {
        display: none !important;
    }
    .stDeployButton {
        display: none !important;
    }
    footer {
        visibility: hidden !important;
        height: 0px !important;
        padding: 0px !important;
    }
    
    /* Reduce top margins and default padding */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    /* Typography Balance */
    h1 {
        font-size: 1.8rem !important;
        font-weight: 850 !important;
        color: #f8fafc !important;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.025em;
    }
    h2 {
        font-size: 1.3rem !important;
        font-weight: 750 !important;
        color: #f1f5f9 !important;
        margin-top: 8px !important;
        margin-bottom: 6px !important;
    }
    h3 {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #e2e8f0 !important;
        margin-top: 6px !important;
        margin-bottom: 4px !important;
    }
    h4 {
        font-size: 0.95rem !important;
        font-weight: 650 !important;
        color: #cbd5e1 !important;
        margin-top: 2px !important;
        margin-bottom: 2px !important;
    }
    
    /* Base Content Text & Lists */
    p, li, span, label, div.stMarkdown {
        font-size: 15px !important;
        line-height: 1.65 !important;
        color: #cbd5e1;
    }
    
    /* Streamlit Selectbox text size balance */
    div[data-baseweb="select"] {
        font-size: 14.5px !important;
    }
    
    /* Premium Markdown Table Styling */
    table {
        width: 100% !important;
        font-size: 14px !important;
        border-collapse: collapse !important;
        margin: 10px 0 !important;
        background-color: rgba(30, 41, 59, 0.25) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    th {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 8px 12px !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    td {
        padding: 8px 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #cbd5e1 !important;
    }
    tr:hover {
        background-color: rgba(51, 65, 85, 0.25) !important;
    }
    
    /* Custom Card Design */
    .visual-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 10px;
    }
    
    .placeholder-chart {
        height: 300px;
        background: repeating-linear-gradient(
          45deg,
          rgba(30, 41, 59, 0.6),
          rgba(30, 41, 59, 0.6) 10px,
          rgba(51, 65, 85, 0.4) 10px,
          rgba(51, 65, 85, 0.4) 20px
        );
        border: 2px dashed rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 15px;
    }
    
    /* Agent Step Block */
    .agent-step {
        background: rgba(51, 65, 85, 0.3);
        border-left: 3px solid #38bdf8;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 12px;
        font-size: 13.5px;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("🏥 HealthGPT Care Gap Trust Planner v2")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# Main Split Columns: 60% Left for Visuals, 40% Right for Chat
col_left, col_right = st.columns([6, 4])

# --- LEFT COLUMN: DYNAMIC VISUALS OR PLACEHOLDERS (60%) ---
with col_left:
    st.markdown("### 📊 Interactive Visualizations & Geospatial Map")
    
    if st.session_state.should_plot and st.session_state.current_plot_code:
        st.markdown("<div class='visual-card'>", unsafe_allow_html=True)
        try:
            # Execute the dynamically generated plotting code
            exec(st.session_state.current_plot_code)
        except Exception as plot_err:
            st.error(f"Failed to render dynamic visualization: {plot_err}")
            st.code(st.session_state.current_plot_code, language="python")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="visual-card">
            <h4 style='margin:0 0 3px 0; color:#38bdf8 !important;'>🗺️ Geographic Care Gap Map Overlay</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Load all districts dynamically
        districts = get_all_districts()
        
        # Dropdown selection and map trigger button
        sel_col, btn_col = st.columns([7, 3])
        with sel_col:
            selected_district = st.selectbox(
                "Select District",
                options=districts,
                index=districts.index("Ghaziabad") if "Ghaziabad" in districts else 0,
                label_visibility="collapsed"
            )
        with btn_col:
            map_clicked = st.button("🗺️ Map Facilities", use_container_width=True)
            
        if map_clicked:
            with st.spinner(f"Querying facilities for {selected_district}..."):
                # Fetch facilities and health indicators from Databricks
                facilities_df = fetch_facilities_for_district(selected_district)
                indicators_df = fetch_health_indicators(selected_district)
                
                # Compute Care Gap Index
                if not indicators_df.empty:
                    anemia = float(indicators_df.iloc[0].get('all_w15_49_who_are_anaemic_pct') or 0.0)
                    bp = float(indicators_df.iloc[0].get('w15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct') or 0.0)
                    sugar = float(indicators_df.iloc[0].get('w15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct') or 0.0)
                    care_gap_index = (anemia + bp + sugar) / 3.0
                else:
                    care_gap_index = 50.0
                
                if not facilities_df.empty:
                    facilities_df['Care Gap Index'] = care_gap_index
                    st.session_state.mapped_facilities = sorted(facilities_df['facility_name'].dropna().unique().tolist())
                    st.session_state.selected_district_name = selected_district
                    st.session_state.travel_plan_data = None
                    import plotly.express as px
                    
                    # Size markers by trust score and color-code them based on the trust score (high score = green, low = red)
                    fig = px.scatter_mapbox(
                        facilities_df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="facility_name",
                        hover_data=["trust_score", "Care Gap Index"],
                        color="trust_score",
                        color_continuous_scale="RdYlGn",
                        size="trust_score",
                        zoom=10,
                        height=680,
                        title=f"Facilities in {selected_district} (District Care Gap Index: {care_gap_index:.1f}%)"
                    )
                    fig.update_layout(
                        mapbox_style="carto-darkmatter",
                        margin={"r":0,"t":40,"l":0,"b":0},
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.session_state.district_plot = fig
                else:
                    st.error(f"No facilities found for district {selected_district} in database.")
                    st.session_state.district_plot = None
                    st.session_state.mapped_facilities = []
                    st.session_state.travel_plan_data = None
                    
        # Render the map
        if st.session_state.district_plot is not None:
            st.plotly_chart(st.session_state.district_plot, use_container_width=True)
        else:
            import plotly.express as px
            # Default map centered on India (lat: 20.5937, lon: 78.9629)
            fig = px.scatter_mapbox(
                lat=[20.5937],
                lon=[78.9629],
                zoom=3.8,
                height=680
            )
            fig.update_layout(
                mapbox_style="carto-darkmatter",
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                mapbox_bounds={"west": 68.0, "east": 97.5, "south": 5.0, "north": 36.0}
            )
            st.plotly_chart(fig, use_container_width=True)
        # Render Visit & Travel Planner if facilities are mapped
        if st.session_state.mapped_facilities:
            st.markdown("""
            <div class="visual-card">
                <h4 style='margin:0 0 10px 0; color:#38bdf8 !important;'>🚗 Visit & Travel Safety Planner</h4>
            </div>
            """, unsafe_allow_html=True)
            
            p_sel, p_btn = st.columns([7, 3])
            with p_sel:
                selected_fac = st.selectbox(
                    "Select Mapped Facility to Visit",
                    options=st.session_state.mapped_facilities,
                    label_visibility="collapsed"
                )
            with p_btn:
                plan_clicked = st.button("🚀 Plan Visit", use_container_width=True)
                
            if plan_clicked:
                with st.spinner("Invoking Travel Planner Agent..."):
                    plan_data = generate_travel_plan(selected_fac, st.session_state.selected_district_name)
                    if plan_data:
                        st.session_state.travel_plan_data = plan_data
                    else:
                        st.error("Failed to generate travel plan from agent.")
            
            if st.session_state.travel_plan_data:
                pd_data = st.session_state.travel_plan_data
                
                # Show metric columns
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Distance", f"{pd_data.get('distance_km', 'N/A')} km")
                m2.metric("ETA Duration", f"{pd_data.get('eta_minutes', 'N/A')} mins")
                m3.metric("Temp Celsius", f"{pd_data.get('weather', {}).get('temp_celsius', 'N/A')}°C")
                m4.metric("Security Status", pd_data.get('geopolitical_situation', {}).get('status', 'Normal'))
                
                # Expand details
                with st.expander("🌤️ Weather & Local Advisory", expanded=True):
                    st.markdown(f"**Condition:** {pd_data.get('weather', {}).get('condition', 'Unknown')}")
                    st.markdown(f"**Advice:** {pd_data.get('weather', {}).get('travel_advice', '')}")
                
                with st.expander("🎪 Local Festivals & Events", expanded=False):
                    fests = pd_data.get('festivals', [])
                    if fests:
                        for f in fests:
                            st.markdown(f"**{f.get('name')}:** {f.get('impact')}")
                    else:
                        st.markdown("No active local festivals simulated for this period.")
                        
                with st.expander("⚠️ Traffic & Geopolitical Alert", expanded=False):
                    g = pd_data.get('geopolitical_situation', {})
                    st.markdown(f"**Geopolitical Context:** {g.get('details', '')}")
                    st.markdown(f"**Safety Alerts:** {g.get('road_safety_alerts', 'No active road safety hazards.')}")
                    st.markdown(f"**Commute Penalty:** +{g.get('traffic_delay_minutes', 0)} mins delay")
                    
                st.markdown(pd_data.get('travel_plan_markdown', ''))

# --- RIGHT COLUMN: CHAT INTERFACE (40%) ---
with col_right:
    st.markdown("### 💬 Care Gap Planner Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I am the Care Gap Planner Assistant. Ask me about any disease care gaps (e.g., heart care, oncology, anemia) in specific districts or for national averages."
            }
        ]

    # Chat box container with fixed height
    chat_container = st.container(height=680)

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # If a plot is available and not yet displayed, show the visualization button
    if st.session_state.current_plot_code and not st.session_state.should_plot:
        if st.button("📈 Visualize Data", use_container_width=True):
            st.session_state.should_plot = True
            st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask about disease care gaps..."):
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Reset visual state on new prompt
        st.session_state.current_plot_code = None
        st.session_state.should_plot = False
        
        # Call Databricks Supervisor Agent Endpoint with streaming
        with chat_container:
            with st.chat_message("assistant"):
                status_placeholder = st.empty()
                response_placeholder = st.empty()
                
                accumulated_text = ""
                thinking_steps = []
                
                # Show initial analysis state
                thinking_steps.append("<div class='agent-step'>🧠 <i>Analyzing query against orchestrator routing matrix...</i></div>")
                status_placeholder.markdown("\n".join(thinking_steps), unsafe_allow_html=True)
                
                try:
                    # Load system prompt instructions
                    try:
                        with open("genie_instructions/genie_space_orchestrator_instructions.txt", "r") as f:
                            system_prompt = f.read()
                    except Exception as sys_e:
                        system_prompt = "You are the Master Orchestrator Agent."
                    
                    # Prepare input payload, prepending system instructions and appending instructions to the last user query
                    api_messages = []
                    for m in st.session_state.messages:
                        if m == st.session_state.messages[-1] and m["role"] == "user":
                            api_messages.append({
                                "role": "user",
                                "content": m["content"] + f"\n\n[INSTRUCTION: Answer strictly following the instructions, routing rules, and the exact 'data + insights in clear pointers' output format defined below:\n{system_prompt}]"
                            })
                        else:
                            api_messages.append({"role": m["role"], "content": m["content"]} )
                    
                    api_messages = [{"role": "system", "content": system_prompt}] + api_messages
                    
                    # Call serving endpoint with stream=True
                    response_stream = openai_client.responses.create(
                        model="mas-573924c0-endpoint",
                        input=api_messages,
                        stream=True
                    )
                    
                    current_item_id = None
                    for chunk in response_stream:
                        chunk_type = getattr(chunk, "type", "Unknown")
                        
                        # 1. Handle text token delta
                        if chunk_type == "response.output_text.delta":
                            delta = getattr(chunk, "delta", "")
                            item_id = getattr(chunk, "item_id", None)
                            
                            # If starting a new message block, insert a newline separator
                            if item_id and current_item_id and item_id != current_item_id:
                                if not accumulated_text.endswith("\n"):
                                    accumulated_text += "\n\n"
                                elif not accumulated_text.endswith("\n\n"):
                                    accumulated_text += "\n"
                            
                            if item_id:
                                current_item_id = item_id
                                
                            accumulated_text += delta
                            response_placeholder.markdown(accumulated_text)
                            
                        # 2. Handle intermediate done items (Tool Calls & Genie tables)
                        elif chunk_type == "response.output_item.done":
                            item = getattr(chunk, "item", None)
                            if item:
                                item_type = getattr(item, "type", "")
                                
                                # A. Tool call (Genie Querying)
                                if item_type == "function_call":
                                    tool_name = getattr(item, "name", "Genie Space")
                                    args_str = getattr(item, "arguments", "{}")
                                    try:
                                        args = json.loads(args_str)
                                        query_text = args.get("genie_query", "Querying data")
                                    except Exception:
                                        query_text = args_str
                                    
                                    step_msg = f"<div class='agent-step'>🔍 <b>Agent Call:</b> Running query in `{tool_name}`: <i>\"{query_text}\"</i></div>"
                                    thinking_steps.append(step_msg)
                                    status_placeholder.markdown("\n".join(thinking_steps), unsafe_allow_html=True)
                                    
                                # B. Table or text payload returned from Genie Space
                                elif item_type == "message":
                                    content_list = getattr(item, "content", [])
                                    for content in content_list:
                                        text_content = getattr(content, "text", "")
                                        if text_content.startswith("||") or "|-|" in text_content:
                                            step_msg = f"<div class='agent-step'>📥 <b>Genie Output:</b> Retrieved database tables:<br><pre style='font-size:11px;'>{text_content}</pre></div>"
                                            thinking_steps.append(step_msg)
                                            status_placeholder.markdown("\n".join(thinking_steps), unsafe_allow_html=True)
                                            
                    # 3. Call Visual Orchestrator Agent to generate plotting code
                    thinking_steps.append("<div class='agent-step'>🎨 <i>Visual Orchestrator analyzing data structure...</i></div>")
                    status_placeholder.markdown("\n".join(thinking_steps), unsafe_allow_html=True)
                    
                    try:
                        with open("genie_instructions/genie_space_visual_orchestrator_instructions.txt", "r") as f:
                            vis_system_prompt = f.read()
                        
                        vis_response = openai_client.responses.create(
                            model="mas-573924c0-endpoint",
                            input=[
                                {"role": "system", "content": vis_system_prompt},
                                {"role": "user", "content": accumulated_text}
                            ]
                        )
                        
                        vis_text = " ".join(
                            getattr(content, "text", "") 
                            for output in vis_response.output 
                            for content in getattr(output, "content", [])
                        ).strip()
                        
                        # Clean the output json wrapper
                        if vis_text.startswith("```json"):
                            vis_text = vis_text[7:]
                        if vis_text.endswith("```"):
                            vis_text = vis_text[:-3]
                        vis_text = vis_text.strip()
                        
                        vis_data = json.loads(vis_text)
                        if vis_data.get("can_visualize") and vis_data.get("plot_code"):
                            st.session_state.current_plot_code = vis_data["plot_code"]
                            st.session_state.should_plot = False
                    except Exception as vis_err:
                        print(f"Visualization generation error: {vis_err}")
                        st.session_state.current_plot_code = None
                        st.session_state.should_plot = False
                        
                except Exception as e:
                    accumulated_text = f"⚠️ Error communicating with Supervisor endpoint: {str(e)}"
                    response_placeholder.markdown(accumulated_text)
                
                # Render final response and clean up intermediate steps to keep chat clean
                status_placeholder.empty()
                response_placeholder.markdown(accumulated_text)
                
        # Trigger page rerun to render the visualize button immediately below the chat input box
        st.session_state.messages.append({"role": "assistant", "content": accumulated_text})
        st.rerun()
