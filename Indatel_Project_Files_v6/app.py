import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & UI SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="INDATEL Pricing Intelligence", layout="wide")
st.title("⚡ INDATEL Pricing Intelligence Prototype")
st.markdown("Upload a batch quote request or search for a single site to generate budgetary MRC/NRC estimates based on sanitized historical pricing data.")

# ---------------------------------------------------------
# 2. DATA INGESTION
# ---------------------------------------------------------
@st.cache_data
def load_database():
    """Loads the Historic Pricing tab to act as our backend database."""
    file_path = "PACEU - IndaForce Project.xlsx"
    try:
        df_hist = pd.read_excel(file_path, sheet_name='Historic Pricing')
        df_hist.rename(columns={
            'IQR: Product': 'Product',
            'Zip Code (Loc Z)': 'ZIP_Code',
            'Member Provider': 'Provider'
        }, inplace=True)
        df_hist = df_hist.dropna(subset=['MRC', 'ZIP_Code'])
        # Ensure dates are datetime objects
        df_hist['Site Price: Created Date'] = pd.to_datetime(df_hist['Site Price: Created Date'], errors='coerce')
        return df_hist
    except FileNotFoundError:
        st.error(f"Error: Could not find '{file_path}'. Please ensure it is in the same directory as this script.")
        return pd.DataFrame()

db = load_database()

# ---------------------------------------------------------
# 3. QUERY & FILTER FUNCTIONS
# ---------------------------------------------------------
def query_database(target_zip, target_product, target_speed, target_term):
    """Searches the database for both exact matches and broader/probable matches."""
    if db.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    exact_matches = db[
        (db['ZIP_Code'] == target_zip) & 
        (db['Product'].str.contains(str(target_product), na=False, case=False)) &
        (db['Speed'] == target_speed) &
        (db['Term'] == target_term)
    ]
    
    zip_prefix = str(target_zip)[:3]
    fuzzy_matches = db[
        (db['ZIP_Code'].astype(str).str.startswith(zip_prefix)) &
        (db['Product'].str.contains(str(target_product), na=False, case=False))
    ]
    
    return exact_matches, fuzzy_matches

def filter_match_quality(exact_matches, fuzzy_matches):
    """Evaluates queried matches and filters them into Green, Orange, or Red categories."""
    if not db.empty:
        latest_date = db['Site Price: Created Date'].max()
        recent_cutoff = latest_date - pd.DateOffset(years=2)
    else:
        recent_cutoff = pd.Timestamp.now() - pd.DateOffset(years=2)

    if not exact_matches.empty:
        recent_exact = exact_matches[exact_matches['Site Price: Created Date'] >= recent_cutoff]
        if not recent_exact.empty:
            return "🟢 GREEN (Strong/Recent)", recent_exact
        return "🟠 ORANGE (Review - Older Pricing)", exact_matches

    if not fuzzy_matches.empty:
        return "🟠 ORANGE (Review - Probable/Fuzzy Match)", fuzzy_matches

    return "🔴 RED (No Match - Request New Pricing)", pd.DataFrame()

def generate_recommendation(target_zip, target_product, target_speed, target_term):
    """Wraps the Query and Filter functions to generate final estimates."""
    exact, fuzzy = query_database(target_zip, target_product, target_speed, target_term)
    status, dataset = filter_match_quality(exact, fuzzy)
    
    if dataset.empty:
        return {"Status": status, "Rec. MRC": "N/A", "Rec. NRC": "N/A", "Samples": 0, "Matched Data": pd.DataFrame()}

    rec_mrc = dataset['MRC'].mean()
    rec_nrc = dataset['NRC'].mean() if not dataset['NRC'].isnull().all() else 0.0
    
    display_df = dataset.copy()
    display_df['Match Quality'] = status
    
    return {
        "Status": status,
        "Rec. MRC": f"${rec_mrc:,.2f}",
        "Rec. NRC": f"${rec_nrc:,.2f}",
        "Samples": len(dataset),
        "Matched Data": display_df
    }

# ---------------------------------------------------------
# 4. DASHBOARD TABS
# ---------------------------------------------------------
def highlight_status(val):
    if isinstance(val, str):
        if '🟢 GREEN' in val:
            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
        elif '🟠 ORANGE' in val:
            return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
        elif '🔴 RED' in val:
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    return ''

tab1, tab2, tab3 = st.tabs(["📁 Batch Quote Upload", "🔍 Single Site Lookup", "📊 Database Overview"])

with tab1:
    st.subheader("Batch Quote Request (RFQ/RFP)")
    uploaded_file = st.file_uploader("Upload an Excel file (Matching INDATEL RFQ/RFP Format)", type=["xlsx"])
    
    if uploaded_file:
        rfq_df = pd.read_excel(uploaded_file)
        st.write("### Incoming Request:")
        st.dataframe(rfq_df)
        
        col1, col2 = st.columns([1, 5])
        
        run_analysis = False
        
        with col2:
            if st.button("⏹️ Stop / Reset Analysis", key="stop_batch"):
                st.warning("Execution stopped. Data cleared.")
                st.stop()
                
        with col1:
            if st.button("▶️ Run Pricing Analysis"):
                run_analysis = True
                
        # Moved the results rendering outside of the narrow col1 block
        if run_analysis:
            results = []
            with st.spinner("Analyzing against PostgreSQL Historical Data..."):
                for index, row in rfq_df.iterrows():
                    t_zip = row.get('ZIP Code')
                    t_prod = row.get('Product')
                    t_speed = row.get('Speed (Mbps)')
                    t_term = row.get('Term (Months)')
                    
                    if pd.isna(t_zip): continue
                    
                    rec = generate_recommendation(t_zip, t_prod, t_speed, t_term)
                    
                    if rec:
                        results.append({
                            "Site ID": row.get('Site ID', f"Site-{index}"),
                            "Target Product": f"{t_speed}M {t_prod} ({t_term}mo)",
                            "Status": rec["Status"],
                            "Rec. MRC": rec["Rec. MRC"],
                            "Rec. NRC": rec["Rec. NRC"],
                            "Samples Found": rec["Samples"]
                        })
            
            st.success("Analysis Complete!")
            st.write("### Budgetary Recommendations & Match Quality:")
            
            res_df = pd.DataFrame(results)
            styled_df = res_df.style.map(highlight_status, subset=['Status']) if hasattr(res_df.style, 'map') else res_df.style.applymap(highlight_status, subset=['Status'])
            
            # The dataframe will now take up the full container width instead of 1/6th of the page
            st.dataframe(styled_df, use_container_width=True)

with tab2:
    st.subheader("Single Site Proximity Finder")
    col1, col2, col3, col4 = st.columns(4)
    s_zip = col1.number_input("ZIP Code", value=33024, step=1)
    s_prod = col2.selectbox("Product", ["Ethernet - Switched", "DIA", "EIA", "Wave"])
    s_speed = col3.number_input("Speed (Mbps)", value=20, step=10)
    s_term = col4.selectbox("Term (Months)", [12, 24, 36, 48, 60])
    
    btn_col1, btn_col2 = st.columns([1, 5])
    
    run_search = False
    
    with btn_col2:
        if st.button("⏹️ Stop / Clear Search", key="stop_single"):
            st.warning("Search cleared.")
            st.stop()
            
    with btn_col1:
        if st.button("🔍 Search Historical Pricing"):
            run_search = True
            
    if run_search:
        res = generate_recommendation(s_zip, s_prod, s_speed, s_term)
        if res:
            st.write(f"### Match Quality: {res['Status']}")
            if res["Samples"] > 0:
                colA, colB = st.columns(2)
                colA.metric(label="Recommended Budgetary MRC", value=res["Rec. MRC"])
                colB.metric(label="Recommended Budgetary NRC", value=res["Rec. NRC"])
                st.info(f"Calculations based on **{res['Samples']}** historical records.")
                
                st.write("### Priority Matches Found")
                display_df = res["Matched Data"][['Site Price: Created Date', 'Product', 'MRC', 'NRC', 'Term', 'Speed', 'ZIP_Code', 'Provider', 'Match Quality']]
                styled_matches = display_df.style.map(highlight_status, subset=['Match Quality']) if hasattr(display_df.style, 'map') else display_df.style.applymap(highlight_status, subset=['Match Quality'])
                
                st.dataframe(styled_matches, use_container_width=True)
            else:
                st.error("New pricing needs to be requested from providers.")

with tab3:
    st.subheader("Sanitized Historical Database")
    st.write(f"Total Records Available: **{len(db)}**")
    st.dataframe(db[['Site Price: Created Date', 'Product', 'MRC', 'NRC', 'Term', 'Speed', 'Loc Z', 'ZIP_Code', 'Provider']].head(100), use_container_width=True)
