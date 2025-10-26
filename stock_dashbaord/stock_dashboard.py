# stock.py
import streamlit as st
import json
from pathlib import Path
import math

DATA_FILE = Path("sectors.json")

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def format_stock_display(stock_info):
    if isinstance(stock_info, str):
        return f"<span style='color:#2c3e50; font-weight:500;'>{stock_info}</span>"
    elif isinstance(stock_info, dict):
        symbol = stock_info.get('symbol', 'N/A')
        name = stock_info.get('name', '')
        price = stock_info.get('price', '')
        change = stock_info.get('change', 0)
        
        color = "#27ae60" if change > 0 else "#e74c3c" if change < 0 else "#95a5a6"
        change_symbol = "▲" if change > 0 else "▼" if change < 0 else "●"
        
        display = f"<span style='color:#2c3e50; font-weight:600;'>{symbol}</span>"
        if name:
            display += f"<span style='color:#7f8c8d; font-size:11px;'> - {name}</span>"
        if price:
            display += f"<span style='color:#34495e; margin-left:5px;'>₹{price}</span>"
        if change:
            display += f"<span style='color:{color}; margin-left:5px;'>{change_symbol} {abs(change)}%</span>"
        return display
    return str(stock_info)

# -------------------
# Main Function
# -------------------
def stock_dashboard():
    st.title("📊 Stock Dashboard")

    # Load data into session
    if "sectors" not in st.session_state:
        st.session_state.sectors = load_data()
    
    sectors = st.session_state.sectors

    # -------------------
    # Sidebar: Add/Delete Elements
    # -------------------
    st.sidebar.header("⚙️ Manage Hierarchy")
    st.sidebar.subheader("➕ Add Elements")

    # --- Add Sector ---
    new_sector = st.sidebar.text_input("New Sector:", key="sector_input")
    if st.sidebar.button("Add Sector"):
        if new_sector and new_sector not in sectors:
            sectors[new_sector] = {}
            save_data(sectors)
            st.success(f"Added sector: {new_sector}")
        else:
            st.warning("Sector already exists or invalid.")

    # --- Add Industry ---
    if sectors:
        selected_sector = st.sidebar.selectbox("Select Sector for Industry", list(sectors.keys()), key="sector_select")
        new_industry = st.sidebar.text_input("New Industry:", key="industry_input")
        if st.sidebar.button("Add Industry"):
            if new_industry and new_industry not in sectors[selected_sector]:
                sectors[selected_sector][new_industry] = {}
                save_data(sectors)
                st.success(f"Added industry: {new_industry}")
            else:
                st.warning("Industry already exists or invalid.")
    else:
        st.sidebar.info("Add a sector first.")

    # --- Add Sub-Industry ---
    if sectors:
        selected_sector_sub = st.sidebar.selectbox("Select Sector for Sub-Industry", list(sectors.keys()), key="sub_sector_select")
        industries = sectors[selected_sector_sub]
        if industries:
            selected_industry = st.sidebar.selectbox("Select Industry", list(industries.keys()), key="sub_industry_select")
            new_subindustry = st.sidebar.text_input("New Sub-Industry:", key="subindustry_input")
            if st.sidebar.button("Add Sub-Industry"):
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
            st.sidebar.info("Add an industry first.")

    # --- Add Stock ---
    if sectors:
        selected_sector_stock = st.sidebar.selectbox("Select Sector for Stock", list(sectors.keys()), key="stock_sector_select")
        industries = sectors[selected_sector_stock]
        if industries:
            selected_industry_stock = st.sidebar.selectbox("Select Industry", list(industries.keys()), key="stock_industry_select")
            sub_data = industries[selected_industry_stock]

            if isinstance(sub_data, dict) and sub_data:
                selected_subindustry_stock = st.sidebar.selectbox("Select Sub-Industry", list(sub_data.keys()), key="stock_subindustry_select")
                new_stock = st.sidebar.text_input("New Stock:", key="stock_input")
                if st.sidebar.button("Add Stock"):
                    stocks = sub_data[selected_subindustry_stock]
                    if new_stock and all((new_stock != s.get("name") if isinstance(s, dict) else new_stock != s) for s in stocks):
                        stocks.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_subindustry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
            else:
                new_stock_direct = st.sidebar.text_input("New Stock Directly under Industry:", key="stock_input_direct")
                if st.sidebar.button("Add Stock Directly"):
                    if isinstance(sub_data, dict):
                        industries[selected_industry_stock] = []
                        sub_data = industries[selected_industry_stock]
                    if new_stock_direct and all((new_stock_direct != s.get("name") if isinstance(s, dict) else new_stock_direct != s) for s in sub_data):
                        sub_data.append(new_stock_direct)
                        save_data(sectors)
                        st.success(f"Added {new_stock_direct} to {selected_industry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")

    # -------------------
    # DELETE SECTION
    # -------------------
    st.sidebar.subheader("🗑️ Delete Elements")
    # [You can copy the delete section here from your original code]

    # -------------------
    # Custom CSS
    # -------------------
    st.markdown("""
    <style>
        .sector-card {background: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #3498db;}
        .industry-header {background: #ecf0f1; padding: 10px; border-radius: 5px; margin: 10px 0;}
        .sub-industry-box {background: white; border: 1px solid #ddd; border-radius: 4px; padding: 10px; margin: 5px 0; height: 100%;}
        .stock-item {padding: 5px 0; border-bottom: 1px solid #eee; font-size: 13px;}
        .stock-item:last-child {border-bottom: none;}
        .empty-state {color: #95a5a6; font-style: italic; font-size: 12px;}
    </style>
    """, unsafe_allow_html=True)

    # -------------------
    # Main Dashboard Layout
    # -------------------
    sector_keys = list(sectors.keys())
    n_sector_rows = math.ceil(len(sector_keys) / 3)  # 3 sectors per row

    for r in range(n_sector_rows):
        cols = st.columns(3, gap="medium")
        
        for c in range(3):
            idx = r*3 + c
            if idx >= len(sector_keys):
                break
            
            sector = sector_keys[idx]
            industries = sectors[sector]
            
            with cols[c]:
                with st.expander(f"🏦 **{sector}**", expanded=False):
                    if not industries:
                        st.markdown("<p class='empty-state'>No industries added</p>", unsafe_allow_html=True)
                    else:
                        for industry, sub_data in industries.items():
                            st.markdown(f"""
                                <div class='industry-header'>
                                    <strong style='color:#2c3e50; font-size:15px;'>🏭 {industry}</strong>
                                </div>
                            """, unsafe_allow_html=True)

                            if isinstance(sub_data, dict):
                                if not sub_data:
                                    st.markdown("<p class='empty-state'>No sub-industries</p>", unsafe_allow_html=True)
                                else:
                                    sub_keys = list(sub_data.keys())
                                    n_sub_rows = math.ceil(len(sub_keys) / 2)
                                    for sub_row in range(n_sub_rows):
                                        sub_cols = st.columns(2, gap="small")
                                        for sub_col in range(2):
                                            sub_idx = sub_row * 2 + sub_col
                                            if sub_idx >= len(sub_keys):
                                                break
                                            sub = sub_keys[sub_idx]
                                            stocks = sub_data[sub]
                                            with sub_cols[sub_col]:
                                                stock_count = len(stocks) if stocks else 0
                                                st.markdown(f"""
                                                    <div class='sub-industry-box'>
                                                        <strong style='color:#7f8c8d; font-size:13px;'>📁 {sub} ({stock_count})</strong>
                                                """, unsafe_allow_html=True)
                                                if stocks:
                                                    for s in stocks:
                                                        st.markdown(f"<div class='stock-item'>• {format_stock_display(s)}</div>", unsafe_allow_html=True)
                                                else:
                                                    st.markdown("<p class='empty-state'>No stocks</p>", unsafe_allow_html=True)
                                                st.markdown("</div>", unsafe_allow_html=True)
                            elif isinstance(sub_data, list):
                                if sub_data:
                                    n_stock_rows = math.ceil(len(sub_data) / 2)
                                    for stock_row in range(n_stock_rows):
                                        stock_cols = st.columns(2, gap="small")
                                        for stock_col in range(2):
                                            stock_idx = stock_row * 2 + stock_col
                                            if stock_idx >= len(sub_data):
                                                break
                                            with stock_cols[stock_col]:
                                                st.markdown(f"""
                                                    <div class='sub-industry-box'>
                                                        <div class='stock-item'>• {format_stock_display(sub_data[stock_idx])}</div>
                                                    </div>
                                                """, unsafe_allow_html=True)
                                else:
                                    st.markdown("<p class='empty-state'>No stocks</p>", unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
