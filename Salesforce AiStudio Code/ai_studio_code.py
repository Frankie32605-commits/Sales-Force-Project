import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import re
from difflib import SequenceMatcher
import io
import json
import os

# ---------------------------------------------------------
# 1. PAGE SETUP & DESIGN SYSTEM WITH ULTRA-DARK CHARACTERS & ICONS
# ---------------------------------------------------------
st.set_page_config(
    page_title="ISP Rate Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  :root {
    --bg: #0f1420;
    --panel: #171e2e;
    --line: #26304a;
    --text: #e6eaf2;
    --muted: #8b96b0;
    --accent: #4f8cff;
    --good: #2ecc8f;
    --warn: #f5a524;
    --bad: #ff5d6c;
  }

  /* Global Layout */
  .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
  }

  .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 98% !important;
  }

  /* Sidebar Layout */
  section[data-testid="stSidebar"] {
    background-color: var(--panel) !important;
    border-right: 1px solid var(--line) !important;
  }

  /* Sidebar Labels */
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3,
  section[data-testid="stSidebar"] h4,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] .stCaption {
    color: var(--text) !important;
  }

  /* ========================================================================= */
  /* ULTRA-DARK CHARACTERS, NUMBERS, AND ICONS FOR ALL TYPE BOXES             */
  /* ========================================================================= */

  /* 1. All Input Containers: Crisp White with Strong Border */
  div[data-baseweb="input"],
  div[data-baseweb="base-input"],
  div[data-baseweb="select"] > div,
  div[data-testid="stNumberInputContainer"],
  div[data-testid="stTextInput"] div[data-baseweb="input"],
  div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 2px solid #64748b !important;
    border-radius: 8px !important;
  }

  /* 2. All Typed Text & Numbers: Pitch Black (#000000), Heavy Weight (800) */
  input,
  input[type="text"],
  input[type="number"],
  div[data-baseweb="input"] input,
  div[data-baseweb="base-input"] input,
  div[data-testid="stNumberInputField"],
  div[data-baseweb="select"] span,
  div[data-baseweb="select"] div,
  div[data-baseweb="select"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    opacity: 1 !important;
  }

  /* 3. Number Input Stepper (+ / -) Buttons: Solid & Visible */
  button[data-testid="stNumberInputStepDown"],
  button[data-testid="stNumberInputStepUp"],
  div[data-testid="stNumberInputContainer"] button {
    background-color: #e2e8f0 !important;
    border-left: 1px solid #cbd5e1 !important;
    opacity: 1 !important;
    cursor: pointer !important;
  }
  button[data-testid="stNumberInputStepDown"]:hover,
  button[data-testid="stNumberInputStepUp"]:hover {
    background-color: #cbd5e1 !important;
  }

  /* 4. Number Input Icons (+ / -): Solid Black with Thick Lines */
  button[data-testid="stNumberInputStepDown"] svg,
  button[data-testid="stNumberInputStepUp"] svg,
  div[data-testid="stNumberInputContainer"] svg {
    fill: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 2.5px !important;
    color: #000000 !important;
    opacity: 1 !important;
    width: 14px !important;
    height: 14px !important;
  }
  button[data-testid="stNumberInputStepDown"] svg path,
  button[data-testid="stNumberInputStepUp"] svg path {
    fill: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 2px !important;
  }

  /* 5. Dropdown Chevron Arrow (v): Solid Black & Bold */
  div[data-baseweb="select"] svg {
    fill: #000000 !important;
    color: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 2px !important;
    opacity: 1 !important;
    width: 18px !important;
    height: 18px !important;
  }
  div[data-baseweb="select"] svg path {
    fill: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 1.5px !important;
  }

  /* 6. Dropdown Menu Items (When Opened) */
  ul[data-baseweb="menu"],
  div[data-baseweb="popover"],
  div[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 2px solid #64748b !important;
  }
  ul[data-baseweb="menu"] li,
  ul[data-baseweb="menu"] li * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
  }
  ul[data-baseweb="menu"] li:hover {
    background-color: #e2e8f0 !important;
  }

  /* 7. Multi-select Tags and Cross (x) Icons */
  span[data-baseweb="tag"] {
    background-color: #e2e8f0 !important;
  }
  span[data-baseweb="tag"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
  }
  span[data-baseweb="tag"] svg {
    fill: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 2px !important;
  }

  /* ========================================================================= */
  /* 8. FILE UPLOADER - dropzone hit area must stay intact                     */
  /* ========================================================================= */

  /* The dropzone itself: white surface, dashed border, drop events enabled */
  div[data-testid="stFileUploader"] section,
  div[data-testid="stFileUploaderDropzone"] {
    background-color: #ffffff !important;
    border: 2px dashed #64748b !important;
    border-radius: 8px !important;
    position: relative !important;
    pointer-events: auto !important;
  }

  /* The real file input: visible hit area, never hidden behind an overlay */
  div[data-testid="stFileUploader"] input[type="file"],
  div[data-testid="stFileUploaderDropzone"] input[type="file"] {
    pointer-events: auto !important;
    opacity: 0 !important;      /* invisible but still clickable */
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    cursor: pointer !important;
  }

  /* Text and icons only - colors without touching layout or hit areas */
  div[data-testid="stFileUploader"] span,
  div[data-testid="stFileUploader"] small,
  div[data-testid="stFileUploader"] p,
  div[data-testid="stFileUploaderDropzone"] span,
  div[data-testid="stFileUploaderDropzone"] small,
  div[data-testid="stFileUploaderDropzone"] p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
  }

  /* Descriptions under the dropzone keep their muted look, still readable */
  div[data-testid="stFileUploader"] small {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
    font-weight: 700 !important;
  }

  /* The browse button must stay clickable and on top of the dropzone */
  div[data-testid="stFileUploader"] button,
  div[data-testid="stFileUploaderDropzone"] button {
    pointer-events: auto !important;
    position: relative !important;
    z-index: 2 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
    background-color: #e2e8f0 !important;
    border: 1px solid #64748b !important;
  }

  div[data-testid="stFileUploader"] svg,
  div[data-testid="stFileUploaderDropzone"] svg {
    fill: #000000 !important;
    stroke: #000000 !important;
    stroke-width: 1.5px !important;
    opacity: 1 !important;
  }

  /* Uploaded-file chip */
  div[data-testid="stFileUploaderFile"] {
    background-color: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    pointer-events: auto !important;
  }
  div[data-testid="stFileUploaderFile"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
  }

  /* 9. Placeholders: High-Contrast Dark Slate */
  ::placeholder,
  input::placeholder,
  textarea::placeholder {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
  }

  /* ========================================================================= */
  /* CARDS, HEADERS & TABLES                                                   */
  /* ========================================================================= */

  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 16px 24px;
  }
  .header-bar h2 {
    margin: 0;
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
  }
  .header-bar p {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: var(--muted);
  }

  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 18px;
  }
  .card h3 {
    margin: 0 0 12px;
    font-size: 14px;
    color: var(--muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .04em;
  }

  .kpis {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 18px;
  }
  .kpi {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 16px;
  }
  .kpi .v {
    font-size: 26px;
    font-weight: 700;
    margin-top: 6px;
    color: var(--text);
  }
  .kpi .l {
    color: var(--muted);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: .04em;
  }

  .tag {
    padding: 3px 8px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
  }
  .up { background: #3a1d24; color: var(--bad); }
  .down { background: #143326; color: var(--good); }
  .flat { background: #352b14; color: var(--warn); }

  .rec {
    border-left: 4px solid var(--good);
    padding: 10px 14px;
    margin-bottom: 10px;
    background: #131a29;
    border-radius: 6px;
  }
  .rec b {
    font-size: 22px;
    color: var(--text);
  }

  .stTabs [data-baseweb="tab-list"] {
    background-color: var(--panel) !important;
    border-bottom: 1px solid var(--line) !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 4px 12px 0 12px !important;
    gap: 6px !important;
  }
  .stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 10px 18px !important;
  }
  .stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background-color: transparent !important;
  }

  .stButton > button[kind="primary"] {
    background-color: var(--accent) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
  }
  .stButton > button:not([kind="primary"]) {
    background-color: transparent !important;
    color: var(--text) !important;
    border: 1px solid var(--line) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
  }
  .stButton > button:hover {
    border-color: var(--accent) !important;
  }

  [data-testid="stDataFrame"] {
    background-color: var(--panel) !important;
    border-radius: 8px !important;
    border: 1px solid var(--line) !important;
  }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. FULLSCREEN COMPONENT (.btn.ghost)
# ---------------------------------------------------------
def render_fullscreen_toggle():
    components.html("""
    <div style="display: flex; justify-content: flex-end; align-items: center; width: 100%;">
      <button id="fs-btn" onclick="toggleFullScreen()" style="
        background: transparent;
        border: 1px solid #26304a;
        color: #e6eaf2;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        font-family: system-ui, -apple-system, sans-serif;
        cursor: pointer;
        transition: .2s;
      " onmouseover="this.style.borderColor='#4f8cff'" onmouseout="this.style.borderColor='#26304a'">
        <span id="fs-text">Toggle Full Screen</span>
      </button>
    </div>
    <script>
    function toggleFullScreen() {
      try {
        var doc = window.parent.document;
        var docEl = doc.documentElement;
        var btnText = document.getElementById("fs-text");
        if (!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
          if (docEl.requestFullscreen) docEl.requestFullscreen();
          else if (docEl.msRequestFullscreen) docEl.msRequestFullscreen();
          else if (docEl.webkitRequestFullscreen) docEl.webkitRequestFullscreen();
          btnText.innerText = "Exit Full Screen";
        } else {
          if (doc.exitFullscreen) doc.exitFullscreen();
          btnText.innerText = "Toggle Full Screen";
        }
      } catch (e) { console.error(e); }
    }
    window.parent.document.addEventListener('fullscreenchange', function() {
      var doc = window.parent.document;
      var btnText = document.getElementById("fs-text");
      if (btnText) btnText.innerText = doc.fullscreenElement ? "Exit Full Screen" : "Toggle Full Screen";
    });
    </script>
    """, height=44)

# ---------------------------------------------------------
# 3. STATISTICAL RECOMMENDATION MODEL & CANVAS CHART
# ---------------------------------------------------------
def analyze_provider(provider_name: str, df: pd.DataFrame, lookback_months: int = 12, target_pct: float = 0.40, apply_trend: bool = True):
    if df.empty or 'LMP' not in df.columns:
        return None
    prov_df = df[df['LMP'] == provider_name].dropna(subset=['Created_Date', 'MRC'])
    prov_df = prov_df[prov_df['MRC'] > 0].sort_values('Created_Date')
    if prov_df.empty:
        return None

    latest_date = prov_df['Created_Date'].max()
    cutoff_date = latest_date - pd.DateOffset(months=lookback_months)
    window_df = prov_df[prov_df['Created_Date'] >= cutoff_date]
    if window_df.empty:
        window_df = prov_df

    prices = window_df['MRC'].values
    n = len(prices)
    if n == 0:
        return None

    pct_val = float(np.percentile(prices, target_pct * 100))

    if n > 1:
        xs = np.arange(n)
        mx = xs.mean()
        my = prices.mean()
        denom = np.sum((xs - mx) ** 2)
        slope = float(np.sum((xs - mx) * (prices - my)) / denom) if denom != 0 else 0.0
    else:
        slope = 0.0

    trend12 = slope * 12
    rec = (pct_val + slope * 3) if apply_trend else pct_val
    rec = max(rec, 0.0)

    my = float(prices.mean())
    sd = float(prices.std()) if n > 1 else 0.0
    conf = "High" if (n >= 12 and (sd / my) < 0.08) else ("Medium" if n >= 6 else "Low")

    chart_dates = window_df['Created_Date'].dt.strftime('%Y-%m-%d').tolist()
    chart_prices = [float(p) for p in prices]

    return {
        "provider": provider_name,
        "n": n,
        "avg": my,
        "low": float(prices.min()),
        "high": float(prices.max()),
        "slope": slope,
        "trend12": trend12,
        "rec": rec,
        "conf": conf,
        "dates": chart_dates,
        "prices": chart_prices
    }

def render_canvas_chart(chart_info):
    if not chart_info or not chart_info.get("prices"):
        st.write("Insufficient data points for charting.")
        return

    dates_json = json.dumps(chart_info["dates"])
    prices_json = json.dumps(chart_info["prices"])
    rec_val = chart_info["rec"]

    components.html(f"""
    <canvas id="chart" width="800" height="260" style="width:100%; height:260px; background:#171e2e; border-radius:8px;"></canvas>
    <script>
    (function(){{
      const c = document.getElementById('chart');
      if (!c) return;
      const x = c.getContext('2d');
      const W = c.width, H = c.height, P = 36;
      const dates = {dates_json};
      const ps = {prices_json};
      const rec = {rec_val};

      x.clearRect(0, 0, W, H);
      const mn = Math.min(...ps, rec) * 0.95;
      const mx = Math.max(...ps, rec) * 1.05;
      const X = i => P + i * (W - 2 * P) / Math.max(ps.length - 1, 1);
      const Y = v => H - P - (v - mn) / Math.max(mx - mn, 0.01) * (H - 2 * P);

      x.strokeStyle = '#26304a';
      x.fillStyle = '#8b96b0';
      x.font = '11px sans-serif';
      for (let i = 0; i <= 4; i++) {{
        const v = mn + (mx - mn) * i / 4;
        x.beginPath();
        x.moveTo(P, Y(v));
        x.lineTo(W - P, Y(v));
        x.stroke();
        x.fillText('$' + v.toFixed(0), 2, Y(v) + 4);
      }}

      x.strokeStyle = '#4f8cff';
      x.lineWidth = 2;
      x.beginPath();
      ps.forEach((p, i) => i ? x.lineTo(X(i), Y(p)) : x.moveTo(X(i), Y(p)));
      x.stroke();

      x.setLineDash([6, 4]);
      x.strokeStyle = '#2ecc8f';
      x.beginPath();
      x.moveTo(P, Y(rec));
      x.lineTo(W - P, Y(rec));
      x.stroke();
      x.setLineDash([]);

      x.fillStyle = '#2ecc8f';
      x.font = 'bold 11px sans-serif';
      x.fillText('Recommended $' + rec.toFixed(2), W - P - 130, Y(rec) - 6);

      x.fillStyle = '#8b96b0';
      x.font = '11px sans-serif';
      if (dates.length > 0) {{
        x.fillText(dates[0], P, H - 10);
        x.fillText(dates[dates.length - 1], W - P - 65, H - 10);
      }}
    }})();
    </script>
    """, height=275)

# ---------------------------------------------------------
# 4. ADDRESS & PRODUCT NORMALIZATION
# ---------------------------------------------------------
STREET_ABBREVIATIONS = {
    r"\broad\b": "rd", r"\bstreet\b": "st", r"\bavenue\b": "ave", r"\bboulevard\b": "blvd",
    r"\bparkway\b": "pkwy", r"\bdrive\b": "dr", r"\blane\b": "ln", r"\bcourt\b": "ct",
    r"\bcircle\b": "cir", r"\bhighway\b": "hwy", r"\bsuite\b": "ste", r"\bnorth\b": "n",
    r"\bsouth\b": "s", r"\beast\b": "e", r"\bwest\b": "w"
}

def clean_address(addr: str) -> str:
    if not isinstance(addr, str) or pd.isna(addr):
        return ""
    addr = re.sub(r"^\*.*?\*\s*-\s*", "", addr, flags=re.IGNORECASE)
    addr = addr.lower().strip()
    addr = re.sub(r"[,\.\#\-\/]", " ", addr)
    addr = re.sub(r"\s+", " ", addr).strip()
    for pattern, replacement in STREET_ABBREVIATIONS.items():
        addr = re.sub(pattern, replacement, addr)
    return addr

def extract_street_number(addr: str) -> str:
    match = re.match(r"^(\d+)", addr.strip())
    return match.group(1) if match else ""

def normalize_product(prod: str) -> str:
    if not isinstance(prod, str) or pd.isna(prod):
        return "UNKNOWN"
    p = prod.upper()
    if any(k in p for k in ["DIA", "DEDICATED INTERNET", "INTERNET"]):
        return "DIA"
    elif any(k in p for k in ["ETHERNET", "EVPL", "SWITCHED", "E-LINE"]):
        return "EVPL"
    elif "WAVE" in p:
        return "WAVELENGTH"
    return p

# ---------------------------------------------------------
# 5. DATA INGESTION & AUTO-DISCOVERY PIPELINE
# ---------------------------------------------------------
DEFAULT_DB_COLS = [
    'Created_Date', 'Product', 'ZIP_Code', 'Raw_Address', 'LMP',
    'Customer', 'Status_Raw', 'Speed', 'Term', 'MRC', 'NRC', 'PPM', 'Valid_Price'
]

COLUMN_ALIASES = {
    'Created_Date': ['site price: created date', 'date', 'created_date', 'timestamp', 'effective_date'],
    'Product': ['iqr: product', 'product', 'plan', 'tier', 'package'],
    'ZIP_Code': ['zip code (loc z)', 'zip', 'zip_code', 'postal', 'region'],
    'Raw_Address': ['loc z', 'address', 'location', 'site_address', 'street'],
    'LMP': ['member provider', 'provider', 'carrier', 'isp', 'vendor'],
    'Customer': ['inbound quote request: customer', 'customer', 'client', 'account'],
    'Status_Raw': ['status', 'quote_status', 'state'],
    'Speed': ['speed', 'speed (mbps)', 'bandwidth', 'speed_mbps'],
    'Term': ['term', 'term (months)', 'contract_term'],
    'MRC': ['mrc', 'price', 'rate', 'monthly_price', 'amount'],
    'NRC': ['nrc', 'install', 'setup', 'non_recurring']
}

def normalize_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c: str(c).strip().lower() for c in df.columns}
    rename_dict = {}
    for standard_col, aliases in COLUMN_ALIASES.items():
        for orig_col, lower_col in cols.items():
            clean_name = re.sub(r"[\s_]+", " ", lower_col)
            if clean_name in aliases or lower_col in aliases:
                rename_dict[orig_col] = standard_col
                break
    return df.rename(columns=rename_dict)

def prepare_database_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=DEFAULT_DB_COLS)

    df = normalize_dataframe_columns(df)
    for col in DEFAULT_DB_COLS:
        if col not in df.columns:
            df[col] = np.nan

    df['Created_Date'] = pd.to_datetime(df['Created_Date'], errors='coerce')
    df['ZIP_Code'] = df['ZIP_Code'].astype(str).str.extract(r'(\d{5})')[0]
    df['Clean_Address'] = df['Raw_Address'].apply(clean_address)
    df['Street_Number'] = df['Clean_Address'].apply(extract_street_number)
    df['Normalized_Product'] = df['Product'].apply(normalize_product)

    df['MRC'] = pd.to_numeric(df['MRC'], errors='coerce')
    df['NRC'] = pd.to_numeric(df['NRC'], errors='coerce')
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Term'] = pd.to_numeric(df['Term'], errors='coerce')
    df['PPM'] = np.where((df['Speed'] > 0) & (df['MRC'] > 0), df['MRC'] / df['Speed'], np.nan)
    df['Valid_Price'] = (df['MRC'].notnull()) & (df['MRC'] > 0)
    return df

def find_master_file_on_disk():
    search_paths = [
        "PACEU - IndaForce Project.xlsx",
        os.path.join(os.path.dirname(__file__), "PACEU - IndaForce Project.xlsx") if "__file__" in globals() else "",
        r"D:\Indatel_Project_Files_v6\PACEU - IndaForce Project.xlsx",
        r"D:\Salesforce AiStudio Code\PACEU - IndaForce Project.xlsx",
        r"D:\PACEU - IndaForce Project.xlsx"
    ]
    for p in search_paths:
        if p and os.path.exists(p):
            return p
    return None

if 'db' not in st.session_state:
    local_path = find_master_file_on_disk()
    if local_path:
        try:
            xl = pd.ExcelFile(local_path)
            hist_sheet = next((s for s in xl.sheet_names if "historic" in s.lower() or "pricing" in s.lower()), None)
            if hist_sheet:
                st.session_state['db'] = prepare_database_df(pd.read_excel(xl, sheet_name=hist_sheet))
            else:
                st.session_state['db'] = pd.DataFrame(columns=DEFAULT_DB_COLS)
        except Exception:
            st.session_state['db'] = pd.DataFrame(columns=DEFAULT_DB_COLS)
    else:
        st.session_state['db'] = pd.DataFrame(columns=DEFAULT_DB_COLS)

# --- Deferred database swap: a sidebar upload stores the frame in
#     'pending_db' and we apply it at the top of the next render, so a
#     drop in progress is never interrupted by a mid-stream rerun. ---
if 'pending_db' in st.session_state:
    st.session_state['db'] = st.session_state.pop('pending_db')
    st.rerun()

db = st.session_state['db']
max_db_date = db['Created_Date'].max() if (not db.empty and pd.notnull(db['Created_Date'].max())) else pd.Timestamp.now()

# ---------------------------------------------------------
# 6. MATCH EVALUATION ENGINE (GREEN / ORANGE / RED)
# ---------------------------------------------------------
def evaluate_site(addr, zip_code, prod, speed, term, db_source, max_date, freshness_months=12, sim_threshold=0.72):
    if db_source.empty:
        return {
            "Status": "RED",
            "Action": "Database empty. Broadcast RFQ to market carriers.",
            "Match_Type": "No data",
            "MRC": np.nan, "NRC": np.nan, "LMP": "Unknown", "Date": None, "Age_Mo": None
        }

    clean_target = clean_address(str(addr))
    target_st_num = extract_street_number(clean_target)
    norm_prod = normalize_product(str(prod))
    target_zip = str(zip_code).zfill(5)[:5]

    candidates = db_source[(db_source['ZIP_Code'] == target_zip) & (db_source['Normalized_Product'] == norm_prod)]
    product_mismatch = False

    if candidates.empty:
        candidates = db_source[db_source['ZIP_Code'] == target_zip]
        product_mismatch = True
        if candidates.empty:
            return {
                "Status": "RED",
                "Action": "Net-new site. Zero history in ZIP. Broadcast RFQ to market carriers.",
                "Match_Type": "Net-new sample site",
                "MRC": np.nan, "NRC": np.nan, "LMP": "Unknown", "Date": None, "Age_Mo": None
            }

    best_match = None
    best_similarity = 0.0
    match_kind = "None"

    for _, row in candidates.iterrows():
        hist_addr = row['Clean_Address']
        hist_st_num = row['Street_Number']

        if clean_target == hist_addr or (target_st_num and target_st_num == hist_st_num and target_st_num in hist_addr and clean_target in hist_addr):
            best_match = row
            best_similarity = 1.0
            match_kind = "Exact"
            break

        if target_st_num and hist_st_num and target_st_num == hist_st_num:
            sim = SequenceMatcher(None, clean_target, hist_addr).ratio()
            if sim >= sim_threshold and sim > best_similarity:
                best_similarity = sim
                best_match = row
                match_kind = "Variation"

    if best_match is None or best_similarity < sim_threshold:
        return {
            "Status": "RED",
            "Action": "Net-new site. Unquoted location. Broadcast RFQ to LMPs.",
            "Match_Type": "Net-new sample site",
            "MRC": np.nan, "NRC": np.nan, "LMP": "Unknown", "Date": None, "Age_Mo": None
        }

    hist_date = best_match['Created_Date']
    age_days = (max_date - hist_date).days if pd.notnull(hist_date) else 9999
    age_months = round(age_days / 30.4, 1) if pd.notnull(hist_date) else None
    is_fresh = (age_months is not None) and (age_months <= freshness_months)

    lmp = best_match['LMP'] if pd.notnull(best_match['LMP']) and str(best_match['LMP']).strip() != "" else "LMP Identified (Unspecified)"
    hist_mrc = best_match['MRC'] if best_match['Valid_Price'] else np.nan
    hist_nrc = best_match['NRC'] if pd.notnull(best_match['NRC']) and best_match['NRC'] >= 0 else 0.0
    hist_speed = best_match['Speed']
    speed_matches = (hist_speed == speed) if pd.notnull(hist_speed) else False

    if product_mismatch:
        return {
            "Status": "ORANGE",
            "Action": f"Location previously quoted for {best_match['Product']}. Contact {lmp} for {prod} rates.",
            "Match_Type": "Address match / Product mismatch",
            "MRC": hist_mrc, "NRC": hist_nrc, "LMP": lmp, "Date": hist_date, "Age_Mo": age_months
        }

    if match_kind == "Exact":
        if speed_matches:
            if is_fresh and pd.notnull(hist_mrc):
                return {
                    "Status": "GREEN",
                    "Action": f"Strong recent match ({age_months} mo ago). Validated {lmp} rate reusable.",
                    "Match_Type": "Exact historical match",
                    "MRC": hist_mrc, "NRC": hist_nrc, "LMP": lmp, "Date": hist_date, "Age_Mo": age_months
                }
            else:
                return {
                    "Status": "ORANGE",
                    "Action": f"Exact address match, but quote is {age_months} mo old. Fast-track refresh with {lmp}.",
                    "Match_Type": "Exact address / Stale pricing",
                    "MRC": hist_mrc, "NRC": hist_nrc, "LMP": lmp, "Date": hist_date, "Age_Mo": age_months
                }
        else:
            return {
                "Status": "ORANGE",
                "Action": f"LMP on-net ({lmp}), but historical speed was {hist_speed}M vs {speed}M requested.",
                "Match_Type": "Exact address / Different speed",
                "MRC": hist_mrc, "NRC": hist_nrc, "LMP": lmp, "Date": hist_date, "Age_Mo": age_months
            }

    if match_kind == "Variation":
        return {
            "Status": "ORANGE",
            "Action": f"Address variation found. Check building suite and request fast confirmation from {lmp}.",
            "Match_Type": "Address variation of historical site",
            "MRC": hist_mrc, "NRC": hist_nrc, "LMP": lmp, "Date": hist_date, "Age_Mo": age_months
        }

    return {
        "Status": "RED",
        "Action": "Net-new site. Requote required.",
        "Match_Type": "Net-new",
        "MRC": np.nan, "NRC": np.nan, "LMP": "Unknown", "Date": None, "Age_Mo": None
    }

# ---------------------------------------------------------
# 7. SIDEBAR CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ISP Rate Analyzer")
    st.caption("Pricing Intelligence Platform")
    st.markdown("---")

    st.markdown("#### Model Parameters")
    lookback_window = st.number_input("Lookback window (months)", min_value=3, max_value=60, value=12, step=1)
    target_pct = st.number_input("Target percentile of history", min_value=0, max_value=100, value=40, step=5) / 100.0
    apply_trend_proj = st.checkbox("Apply trend projection (3 mo)", value=True)

    st.markdown("---")
    st.markdown("#### Address Matching")
    variation_sensitivity = st.slider("Variation Sensitivity", min_value=0.60, max_value=0.90, value=0.72, step=0.02)

    st.markdown("---")
    st.markdown("#### Historical Database Status")
    if not db.empty and db['MRC'].notnull().any():
        st.success(f"Connected: **{len(db):,}** historical quotes")
        st.caption(f"Latest record: {max_db_date.strftime('%Y-%m-%d')}")
    else:
        st.warning("Database not loaded. Upload the master Excel file below:")
        up_master = st.file_uploader("Upload PACEU Master File (.xlsx)", type=["xlsx"], key="sb_uploader")
        if up_master:
            try:
                xl_sb = pd.ExcelFile(up_master)
                hist_sheet = next((s for s in xl_sb.sheet_names if "historic" in s.lower() or "pricing" in s.lower()), None)
                if hist_sheet:
                    st.session_state['pending_db'] = prepare_database_df(pd.read_excel(xl_sb, sheet_name=hist_sheet))
                    st.success("Historical database successfully extracted!")
                else:
                    st.error("No sheet named 'Historic Pricing' found in that workbook.")
            except Exception as e:
                st.error(f"Upload failed: {e}")

# ---------------------------------------------------------
# 8. MAIN HEADER BAR
# ---------------------------------------------------------
hc1, hc2 = st.columns([4, 1])
with hc1:
    st.markdown("""
    <div class="header-bar">
      <div>
        <h2>ISP Rate Analyzer</h2>
        <p>Analyze historical pricing dumps, evaluate incoming RFPs, and benchmark recommended provider rates.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
with hc2:
    render_fullscreen_toggle()

# ---------------------------------------------------------
# 9. TABS (SECTIONS 1-4)
# ---------------------------------------------------------
tab_import, tab_data, tab_rates, tab_settings = st.tabs([
    "1. Import Data",
    "2. Organized Data",
    "3. Recommended Rates",
    "Settings"
])

# ---------------------------------------------------------
# SECTION 1: IMPORT DATA DUMPS & BATCH RFP
# ---------------------------------------------------------
with tab_import:
    st.markdown("### Import Data Dumps & RFPs")

    col_up, col_samp = st.columns([4, 1])
    with col_up:
        uploaded_file = st.file_uploader(
            "Drop CSV or Excel files here or click to browse",
            type=["xlsx", "csv", "json"],
            key="importer_box"
        )
    with col_samp:
        st.write("")
        st.write("")
        load_sample = st.button("Load Sample Data", use_container_width=True)

    imported_df = None

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                xl_file = pd.ExcelFile(uploaded_file)
                hist_sheet = next((s for s in xl_file.sheet_names if "historic" in s.lower() or "pricing" in s.lower()), None)
                if hist_sheet and (st.session_state['db'].empty or len(st.session_state['db']) == 0):
                    st.session_state['pending_db'] = prepare_database_df(pd.read_excel(xl_file, sheet_name=hist_sheet))
                    st.success(f"Extracted historical quotes from '{hist_sheet}' into master database.")

                rfp_sheets = [s for s in xl_file.sheet_names if "historic" not in s.lower() and "pricing" not in s.lower()]
                if not rfp_sheets:
                    rfp_sheets = xl_file.sheet_names

                sel_sheet = st.selectbox("Select Request Sheet to Triage", rfp_sheets, index=0)
                imported_df = pd.read_excel(xl_file, sheet_name=sel_sheet)
            elif uploaded_file.name.endswith(".csv"):
                imported_df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                imported_df = pd.read_json(uploaded_file)
        except Exception as e:
            st.error(f"Error parsing file: {e}")

    elif load_sample:
        local_p = find_master_file_on_disk()
        if local_p:
            try:
                xl_sample = pd.ExcelFile(local_p)
                hist_sheet = next((s for s in xl_sample.sheet_names if "historic" in s.lower() or "pricing" in s.lower()), None)
                if hist_sheet:
                    st.session_state['pending_db'] = prepare_database_df(pd.read_excel(xl_sample, sheet_name=hist_sheet))
                rfp_sheets = [s for s in xl_sample.sheet_names if "historic" not in s.lower() and "pricing" not in s.lower()]
                imported_df = pd.read_excel(xl_sample, sheet_name=rfp_sheets[0] if rfp_sheets else 0)
                st.success(f"Loaded sample RFP from disk ({len(imported_df)} sites).")
            except Exception as e:
                st.error(f"Failed to load sample: {e}")
        else:
            st.error("PACEU - IndaForce Project.xlsx not found on local disk. Please upload it above.")

    if imported_df is not None:
        imported_df = normalize_dataframe_columns(imported_df)
        st.markdown("##### Uploaded Request Preview:")
        st.dataframe(imported_df.head(4), use_container_width=True)

        if st.button("Run Rate Analysis & Triage", type="primary"):
            current_db = st.session_state['db']

            if current_db.empty:
                st.error("Historical database is empty! Please upload 'PACEU - IndaForce Project.xlsx' containing the 'Historic Pricing' tab.")
            else:
                results = []
                progress = st.progress(0, text="Auditing sites against carrier footprint...")
                total_rows = len(imported_df)

                for i, row in imported_df.iterrows():
                    addr = row.get('Raw_Address', row.get('Address'))
                    zip_code = row.get('ZIP_Code', row.get('ZIP Code'))
                    prod = row.get('Product')
                    speed = row.get('Speed', row.get('Speed (Mbps)'))
                    term = row.get('Term', row.get('Term (Months)'))
                    site_id = row.get('Site ID', f"SITE-{i+1:03d}")

                    eval_res = evaluate_site(
                        addr, zip_code, prod, speed, term, current_db, max_db_date,
                        freshness_months=lookback_window, sim_threshold=variation_sensitivity
                    )

                    ppm = eval_res['MRC'] / speed if pd.notnull(eval_res['MRC']) and speed and speed > 0 else np.nan

                    results.append({
                        "Site ID": site_id,
                        "Address": addr,
                        "ZIP": zip_code,
                        "Product": prod,
                        "Speed": speed,
                        "Status": eval_res["Status"],
                        "Match Category": eval_res["Match_Type"],
                        "Identified LMP": eval_res["LMP"],
                        "Recommended Rate": f"${eval_res['MRC']:,.2f}" if pd.notnull(eval_res['MRC']) else "Quote Req.",
                        "NRC": f"${eval_res['NRC']:,.2f}" if pd.notnull(eval_res['NRC']) else "$0.00",
                        "$/Mbps": f"${ppm:,.2f}" if pd.notnull(ppm) else "—",
                        "Age (Mo)": eval_res["Age_Mo"] if eval_res["Age_Mo"] is not None else "N/A",
                        "Action Note": eval_res["Action"]
                    })
                    progress.progress((i + 1) / total_rows)

                progress.empty()
                st.session_state['import_results'] = pd.DataFrame(results)

    if 'import_results' in st.session_state:
        res_df = st.session_state['import_results']
        total = len(res_df)
        greens = len(res_df[res_df['Status'] == "GREEN"])
        oranges = len(res_df[res_df['Status'] == "ORANGE"])
        reds = len(res_df[res_df['Status'] == "RED"])

        st.markdown(f"""
        <div class="kpis">
          <div class="kpi"><div class="l">Total Sites</div><div class="v">{total}</div></div>
          <div class="kpi"><div class="l">Green (Reusable)</div><div class="v" style="color:var(--good);">{greens} <span style="font-size:14px;color:var(--muted);">({greens/total*100:.0f}%)</span></div></div>
          <div class="kpi"><div class="l">Orange (Review)</div><div class="v" style="color:var(--warn);">{oranges} <span style="font-size:14px;color:var(--muted);">({oranges/total*100:.0f}%)</span></div></div>
          <div class="kpi"><div class="l">Red (Requote)</div><div class="v" style="color:var(--bad);">{reds} <span style="font-size:14px;color:var(--muted);">({reds/total*100:.0f}%)</span></div></div>
        </div>
        """, unsafe_allow_html=True)

        fc1, fc2 = st.columns([2, 4])
        with fc1:
            stat_filter = st.multiselect("Filter by Status", ["GREEN", "ORANGE", "RED"], default=["GREEN", "ORANGE", "RED"])
        with fc2:
            query_filter = st.text_input("Filter Plan, Address, or Provider", placeholder="e.g. Provider 34, Charlotte, 500M...")

        f_res = res_df[res_df['Status'].isin(stat_filter)]
        if query_filter.strip():
            qf = query_filter.lower()
            f_res = f_res[
                f_res['Address'].astype(str).str.lower().str.contains(qf) |
                f_res['Site ID'].astype(str).str.lower().str.contains(qf) |
                f_res['Identified LMP'].astype(str).str.lower().str.contains(qf)
            ]

        def color_status_rows(val):
            val_str = str(val).upper()
            if 'GREEN' in val_str:
                return 'background-color: #143326; color: #2ecc8f; font-weight: 600; border-left: 3px solid #2ecc8f;'
            elif 'ORANGE' in val_str:
                return 'background-color: #352b14; color: #f5a524; font-weight: 600; border-left: 3px solid #f5a524;'
            elif 'RED' in val_str:
                return 'background-color: #3a1d24; color: #ff5d6c; font-weight: 600; border-left: 3px solid #ff5d6c;'
            return ''

        styler = f_res.style
        if hasattr(styler, 'map'):
            styled_df = styler.map(color_status_rows, subset=['Status'])
        else:
            styled_df = styler.applymap(color_status_rows, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)

        csv_buffer = f_res.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export CSV",
            data=csv_buffer,
            file_name="organized_isp_rate_data.csv",
            mime="text/csv"
        )

# ---------------------------------------------------------
# SECTION 2: ORGANIZED DATA & MULTI-FILTER SEARCH
# ---------------------------------------------------------
with tab_data:
    st.markdown("### Organized Historical Data")

    col_p, col_r, col_s = st.columns([2, 2, 3])
    with col_p:
        all_provs = ["All providers"] + (sorted([p for p in db['LMP'].dropna().unique() if str(p).strip()]) if ('LMP' in db.columns and not db.empty) else [])
        sel_prov = st.selectbox("Provider", all_provs)
    with col_r:
        all_regions = ["All regions"] + (sorted([z for z in db['ZIP_Code'].dropna().unique() if str(z).strip()]) if ('ZIP_Code' in db.columns and not db.empty) else [])
        sel_region = st.selectbox("Region", all_regions)
    with col_s:
        plan_search = st.text_input("Search plan or address...", placeholder="Search plan, speed, address...")

    d_filtered = db.copy() if not db.empty else pd.DataFrame(columns=DEFAULT_DB_COLS)
    if sel_prov != "All providers" and 'LMP' in d_filtered.columns:
        d_filtered = d_filtered[d_filtered['LMP'] == sel_prov]
    if sel_region != "All regions" and 'ZIP_Code' in d_filtered.columns:
        d_filtered = d_filtered[d_filtered['ZIP_Code'] == sel_region]
    if plan_search.strip() and not d_filtered.empty:
        ps = plan_search.lower()
        d_filtered = d_filtered[
            d_filtered['Raw_Address'].astype(str).str.lower().str.contains(ps) |
            d_filtered['Product'].astype(str).str.lower().str.contains(ps) |
            d_filtered['Speed'].astype(str).str.lower().str.contains(ps)
        ]

    rec_count = len(d_filtered)
    prov_count = d_filtered['LMP'].nunique() if ('LMP' in d_filtered.columns and not d_filtered.empty) else 0
    avg_price = d_filtered['MRC'].mean() if (rec_count > 0 and 'MRC' in d_filtered.columns and d_filtered['MRC'].notnull().any()) else 0.0
    dates_sorted = d_filtered['Created_Date'].dropna().sort_values() if ('Created_Date' in d_filtered.columns and not d_filtered.empty) else pd.Series(dtype='datetime64[ns]')
    date_range_txt = f"{dates_sorted.iloc[0].strftime('%Y-%m-%d')} → {dates_sorted.iloc[-1].strftime('%Y-%m-%d')}" if not dates_sorted.empty else "—"

    st.markdown(f"""
    <div class="kpis">
      <div class="kpi"><div class="l">Records</div><div class="v">{rec_count:,}</div></div>
      <div class="kpi"><div class="l">Providers</div><div class="v">{prov_count}</div></div>
      <div class="kpi"><div class="l">Avg Monthly Price</div><div class="v">${avg_price:,.2f}</div></div>
      <div class="kpi"><div class="l">Date Range</div><div class="v" style="font-size:16px;">{date_range_txt}</div></div>
    </div>
    """, unsafe_allow_html=True)

    display_cols = [c for c in ['Created_Date', 'LMP', 'Product', 'Speed', 'MRC', 'PPM', 'ZIP_Code', 'Raw_Address'] if c in d_filtered.columns]
    view_df = d_filtered[display_cols].rename(columns={
        'Created_Date': 'Date', 'LMP': 'Provider', 'Product': 'Plan',
        'Speed': 'Speed (Mbps)', 'MRC': 'Price', 'PPM': '$/Mbps', 'ZIP_Code': 'Region', 'Raw_Address': 'Address'
    })

    st.dataframe(view_df.head(500), use_container_width=True)

    csv_data = view_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Organized CSV",
        data=csv_data,
        file_name="organized_isp_data.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# SECTION 3: RECOMMENDED RATES
# ---------------------------------------------------------
with tab_rates:
    st.markdown("### Recommended Rates & Model Analytics")

    prov_list = sorted([p for p in db['LMP'].dropna().unique() if str(p).strip()]) if ('LMP' in db.columns and not db.empty) else []
    if not prov_list:
        st.info("No provider records available. Please upload a dataset containing provider quotes.")
    else:
        selected_provider = st.selectbox("Select Provider for Analysis", prov_list, index=0)

        r_analysis = analyze_provider(
            selected_provider, db,
            lookback_months=lookback_window,
            target_pct=target_pct,
            apply_trend=apply_trend_proj
        )

        col_chart, col_rec = st.columns([2, 1])

        with col_chart:
            st.markdown('<div class="card"><h3>Price History & Linear Projection</h3></div>', unsafe_allow_html=True)
            if r_analysis:
                render_canvas_chart(r_analysis)
            else:
                st.write("Insufficient data points for this provider.")

        with col_rec:
            if r_analysis:
                rec_val = f"${r_analysis['rec']:,.2f}"
                avg_val = f"${r_analysis['avg']:,.2f}"
                low_val = f"${r_analysis['low']:,.2f}"
                high_val = f"${r_analysis['high']:,.2f}"
                trend_dir = "rising" if r_analysis['slope'] >= 0 else "falling"
                slope_val = f"${abs(r_analysis['slope']):,.2f}"
                guidance_txt = "Target is below average — good negotiating position." if r_analysis['rec'] < r_analysis['avg'] else "Prices trending up — consider locking in a contract soon."

                st.markdown(f"""
                <div class="card">
                  <h3>Recommendation</h3>
                  <div class="rec">
                    <div style="color:var(--muted); font-size:12px; text-transform:uppercase;">Recommended monthly rate</div>
                    <b>{rec_val}</b>
                  </div>
                  <p>Historical range: <b>{low_val}</b> – <b>{high_val}</b></p>
                  <p>Trend: <b>{trend_dir}</b> ~{slope_val}/period</p>
                  <p>Confidence: <b>{r_analysis['conf']}</b> <span style="color:var(--muted);">({r_analysis['n']} data points)</span></p>
                  <p style="color:var(--muted); font-size:13px;">{guidance_txt}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>All Providers Rate Benchmarks</h3></div>', unsafe_allow_html=True)

        table_rows = []
        for p in prov_list:
            an = analyze_provider(p, db, lookback_months=lookback_window, target_pct=target_pct, apply_trend=apply_trend_proj)
            if an:
                trend_tag = "up" if an['trend12'] > 1 else ("down" if an['trend12'] < -1 else "flat")
                sign = "+" if an['trend12'] >= 0 else ""
                table_rows.append({
                    "Provider": p,
                    "Avg Price": f"${an['avg']:,.2f}",
                    "12-mo Trend": f"{sign}${an['trend12']:,.2f}",
                    "Trend Tag": trend_tag,
                    "Low": f"${an['low']:,.2f}",
                    "High": f"${an['high']:,.2f}",
                    "Recommended Rate": f"${an['rec']:,.2f}",
                    "Confidence": an['conf']
                })

        summary_df = pd.DataFrame(table_rows)

        def highlight_trend_tag(val):
            if val == 'up': return 'background-color: #3a1d24; color: #ff5d6c; font-weight: 600;'
            elif val == 'down': return 'background-color: #143326; color: #2ecc8f; font-weight: 600;'
            elif val == 'flat': return 'background-color: #352b14; color: #f5a524; font-weight: 600;'
            return ''

        styler_prov = summary_df.style
        if hasattr(styler_prov, 'map'):
            styled_prov = styler_prov.map(highlight_trend_tag, subset=['Trend Tag'])
        else:
            styled_prov = styler_prov.applymap(highlight_trend_tag, subset=['Trend Tag'])
        st.dataframe(styled_prov, use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="card"><h3>Location Rate Profiler & Carrier Triage</h3></div>', unsafe_allow_html=True)

        sp1, sp2 = st.columns(2)
        with sp1:
            site_addr = st.text_input("Street Address", value="2625 W MAIN ST")
            site_zip = st.text_input("ZIP Code", value="77573")
        with sp2:
            site_prod = st.selectbox("Product", ["Ethernet - Switched", "DIA", "EVPL"])
            sp_s, sp_t = st.columns(2)
            site_speed = sp_s.number_input("Bandwidth (Mbps)", value=500, step=50)
            site_term = sp_t.selectbox("Term (Months)", [36, 12, 24, 60], index=0)

        if st.button("Evaluate Location Rate", type="primary"):
            ev = evaluate_site(
                site_addr, site_zip, site_prod, site_speed, site_term, db, max_db_date,
                freshness_months=lookback_window, sim_threshold=variation_sensitivity
            )

            border_c = "var(--good)" if ev["Status"] == "GREEN" else ("var(--warn)" if ev["Status"] == "ORANGE" else "var(--bad)")
            rate_disp = f"${ev['MRC']:,.2f} / mo" if pd.notnull(ev['MRC']) else "Quote Required"

            st.markdown(f"""
            <div class="card" style="border-left: 5px solid {border_c};">
              <div style="font-size: 18px; font-weight: 700; color: {border_c};">{ev['Status']} — {ev['Match_Type']}</div>
              <div class="rec" style="margin-top: 10px;">
                <div style="color:var(--muted); font-size:12px; text-transform:uppercase;">Recommended Rate</div>
                <b>{rate_disp}</b>
              </div>
              <p><b>Carrier (LMP):</b> {ev['LMP']}</p>
              <p><b>Action:</b> {ev['Action']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 4: SETTINGS
# ---------------------------------------------------------
with tab_settings:
    st.markdown("### Settings & Recommendation Engine")
    st.markdown("""
    <div class="card">
      <h3>Recommendation Model</h3>
      <p><b>Lookback window:</b> Filter quotes within the specified months preceding the latest date in dataset.</p>
      <p><b>Target percentile:</b> Selected percentile of historical prices (default 40th percentile).</p>
      <p><b>Linear trend projection:</b> Projects rate adjustment 3 months ahead based on slope.</p>
      <p style="color:var(--muted); font-size:13px;">Recommended rate = chosen percentile of prices in lookback window, adjusted by the linear price trend projected 3 months ahead.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <h3>Classification Triage Rules</h3>
      <p><span class="tag down">GREEN</span> <b>Reusable:</b> Exact address match, same product, identical bandwidth tier, and quoted within the lookback window.</p>
      <p><span class="tag flat">ORANGE</span> <b>Review:</b> Location quoted by known carrier, but quote is outside the lookback window, bandwidth differs, or street variation requires verification.</p>
      <p><span class="tag up">RED</span> <b>Requote:</b> Location has zero quote history. Requires full market survey RFQ.</p>
    </div>
    """, unsafe_allow_html=True)
