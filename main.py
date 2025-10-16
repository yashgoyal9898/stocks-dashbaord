import streamlit as st
import json
from pathlib import Path
import math

DATA_FILE = Path("sectors.json")

# -------------------
# Helper Functions
# -------------------
def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------
# App Initialization
# -------------------
st.set_page_config(page_title="DashBoard", layout="wide")
st.title("📊 Dashboard")

# Load data into session
if "sectors" not in st.session_state:
    st.session_state.sectors = load_data()

sectors = st.session_state.sectors

# -------------------
# Top Control Panel (Add Elements)
# -------------------
st.markdown("### ⚙️ Manage Hierarchy")
col1, col2, col3, col4 = st.columns(4)

# === Add Sector ===
with col1:
    st.subheader("🏦 Sector")
    new_sector = st.text_input("New Sector:", key="sector_input")
    if st.button("➕ Add Sector", key="add_sector"):
        if new_sector and new_sector not in sectors:
            sectors[new_sector] = {}
            save_data(sectors)
            st.success(f"Added sector: {new_sector}")
        else:
            st.warning("Sector already exists or invalid.")

# === Add Industry ===
with col2:
    st.subheader("🏭 Industry")
    if sectors:
        selected_sector = st.selectbox("Sector", list(sectors.keys()), key="sector_select")
        new_industry = st.text_input("New Industry:", key="industry_input")
        if st.button("➕ Add Industry", key="add_industry"):
            if new_industry and new_industry not in sectors[selected_sector]:
                sectors[selected_sector][new_industry] = {}
                save_data(sectors)
                st.success(f"Added industry: {new_industry}")
            else:
                st.warning("Industry already exists or invalid.")
    else:
        st.info("Add a sector first.")

# === Add Sub-Industry ===
with col3:
    st.subheader("📁 Sub-Industry")
    if sectors:
        sector_list = list(sectors.keys())
        selected_sector_sub = st.selectbox("Sector", sector_list, key="sub_sector_select")
        industries = sectors[selected_sector_sub]
        if industries:
            selected_industry = st.selectbox("Industry", list(industries.keys()), key="sub_industry_select")
            new_subindustry = st.text_input("New Sub-Industry:", key="subindustry_input")
            if st.button("➕ Add Sub-Industry", key="add_subindustry"):
                if isinstance(industries[selected_industry], dict):
                    if new_subindustry and new_subindustry not in industries[selected_industry]:
                        industries[selected_industry][new_subindustry] = []
                        save_data(sectors)
                        st.success(f"Added sub-industry: {new_subindustry}")
                    else:
                        st.warning("Sub-industry already exists or invalid.")
                else:
                    st.warning("Cannot add sub-industry: Industry already has direct stocks.")
        else:
            st.info("Add an industry first.")
    else:
        st.info("Add a sector first.")

# === Add Stock ===
with col4:
    st.subheader("📈 Stock")
    if sectors:
        sector_list = list(sectors.keys())
        selected_sector_stock = st.selectbox("Sector", sector_list, key="stock_sector_select")
        industries = sectors[selected_sector_stock]
        if industries:
            selected_industry_stock = st.selectbox("Industry", list(industries.keys()), key="stock_industry_select")
            sub_data = industries[selected_industry_stock]
            
            # Determine if sub-industries exist
            if isinstance(sub_data, dict) and sub_data:
                selected_subindustry_stock = st.selectbox("Sub-Industry", list(sub_data.keys()), key="stock_subindustry_select")
                new_stock = st.text_input("New Stock:", key="stock_input")
                if st.button("➕ Add Stock", key="add_stock"):
                    stocks = sub_data[selected_subindustry_stock]
                    if new_stock and new_stock not in stocks:
                        stocks.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_subindustry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
            else:
                # Industry directly has stocks or empty dict
                new_stock = st.text_input("New Stock:", key="stock_input_direct")
                if st.button("➕ Add Stock Directly", key="add_stock_direct"):
                    if isinstance(sub_data, dict):
                        # Convert empty dict to stock list
                        industries[selected_industry_stock] = []
                        sub_data = industries[selected_industry_stock]
                    if new_stock and new_stock not in sub_data:
                        sub_data.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_industry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
        else:
            st.info("Add an industry first.")
    else:
        st.info("Add a sector first.")

# -------------------
# Main Page Layout (Display)
# -------------------
sector_keys = list(sectors.keys())
n_sector_rows = math.ceil(len(sector_keys) / 3)

for r in range(n_sector_rows):
    cols = st.columns(3, gap="small")
    for c in range(3):
        idx = r*3 + c
        if idx >= len(sector_keys):
            break
        sector = sector_keys[idx]
        industries = sectors[sector]

        with cols[c]:
            # Sector Title
            st.markdown(
                f"<h2 style='font-size:20px; padding: 0px 0px 5px 0px; color:#2C3E50; font-weight:800;'>🏦 {sector}</h2>",
                unsafe_allow_html=True
            )

            if not industries:
                st.write("<p style='color:gray;'>No industries yet.</p>", unsafe_allow_html=True)
            else:
                for industry, sub_data in industries.items():
                    # Industry Title
                    st.markdown(
                        f"<h4 style='font-size:16px; color:#34495E; padding: 20px 0px 15px 0px; font-weight:700;'>🏭 {industry}</h4>",
                        unsafe_allow_html=True
                    )

                    if isinstance(sub_data, dict):
                        if not sub_data:
                            st.write("<p style='color:gray;'>No sub-industries yet.</p>", unsafe_allow_html=True)
                        else:
                            # Display sub-industries in 3 columns
                            sub_keys = list(sub_data.keys())
                            n_sub_rows = math.ceil(len(sub_keys) / 3)
                            for sr in range(n_sub_rows):
                                sub_cols = st.columns(3, gap="small")
                                for sc in range(3):
                                    sub_idx = sr*3 + sc
                                    if sub_idx >= len(sub_keys):
                                        break
                                    sub = sub_keys[sub_idx]
                                    stocks = sub_data[sub]
                                    with sub_cols[sc]:
                                        st.markdown(f"<b style='color:#7F8C8D; font-size: 14px;'>📁 {sub}</b>", unsafe_allow_html=True)
                                        if stocks:
                                            stock_html = "<br>".join(
                                                [f"<span style='font-size:12px; font-family: sans-serif;'>{s}</span>" for s in stocks]
                                            )
                                            st.markdown(stock_html, unsafe_allow_html=True)
                                        else:
                                            st.write("<p style='color:gray;'>No stocks yet.</p>", unsafe_allow_html=True)
                    elif isinstance(sub_data, list):
                        if sub_data:
                            stock_html = "<br>".join(
                                [f"<span style='font-size:12px; font-family: sans-serif;'>{s}</span>" for s in sub_data]
                            )
                            st.markdown(stock_html, unsafe_allow_html=True)
                        else:
                            st.write("<p style='color:gray;'>No stocks yet.</p>", unsafe_allow_html=True)
