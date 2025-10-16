import streamlit as st
import json
from pathlib import Path

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
                if new_subindustry and new_subindustry not in sectors[selected_sector_sub][selected_industry]:
                    sectors[selected_sector_sub][selected_industry][new_subindustry] = []
                    save_data(sectors)
                    st.success(f"Added sub-industry: {new_subindustry}")
                else:
                    st.warning("Sub-industry already exists or invalid.")
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
            subindustries = industries[selected_industry_stock]
            if subindustries:
                selected_subindustry_stock = st.selectbox("Sub-Industry", list(subindustries.keys()), key="stock_subindustry_select")
                new_stock = st.text_input("New Stock:", key="stock_input")
                if st.button("➕ Add Stock", key="add_stock"):
                    stocks = subindustries[selected_subindustry_stock]
                    if new_stock and new_stock not in stocks:
                        stocks.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_subindustry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
            else:
                st.info("Add a sub-industry first.")
        else:
            st.info("Add an industry first.")
    else:
        st.info("Add a sector first.")


# -------------------
# Main Page Layout (Display)
# -------------------
# Use 8 columns per row, with small gaps
cols = st.columns(8, gap="small")

for i, (sector, industries) in enumerate(sectors.items()):
    with cols[i % 8]:
        # Sector Title
        st.markdown(
            f"<h2 style='font-size:16px; color:#2C3E50; font-weight:800;'>🏦 {sector}</h2>",
            unsafe_allow_html=True
        )

        if not industries:
            st.write("<p style='color:gray;'>No industries yet.</p>", unsafe_allow_html=True)
        else:
            for industry, sub_data in industries.items():
                # Industry Title
                st.markdown(
                    f"<h4 style='font-size:14px; color:#34495E; font-weight:700;'>🏭 {industry}</h4>",
                    unsafe_allow_html=True
                )

                if not sub_data:
                    st.write("<p style='color:gray;'>No sub-industries yet.</p>", unsafe_allow_html=True)
                else:
                    for sub, stocks in sub_data.items():
                        # Sub-Industry
                        st.markdown(
                            f"<b style='color:#7F8C8D;'>📁 {sub}</b>",
                            unsafe_allow_html=True
                        )
                        # Stocks
                        if stocks:
                            stock_html = "<br>".join(
                                [f"<span style='font-size:12px;'>{s}</span>" for s in stocks]
                            )
                            st.markdown(stock_html, unsafe_allow_html=True)
                        else:
                            st.write("<p style='color:gray;'>No stocks yet.</p>", unsafe_allow_html=True)
