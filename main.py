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

def format_stock_display(stock):
    if isinstance(stock, dict):
        stars = "★" * stock.get("rating", 0)
        return f"{stock['name']} {stars}"
    return stock

def flatten_stocks(sectors):
    all_stocks_list = []
    for sector_name, sector_data in sectors.items():
        for industry, sub_data in sector_data.items():
            if isinstance(sub_data, dict):
                for sub_industry, stocks in sub_data.items():
                    if isinstance(stocks, list):
                        for s in stocks:
                            stock_name = s["name"] if isinstance(s, dict) else s
                            all_stocks_list.append((sector_name, industry, sub_industry, stock_name))
            elif isinstance(sub_data, list):
                for s in sub_data:
                    stock_name = s["name"] if isinstance(s, dict) else s
                    all_stocks_list.append((sector_name, industry, None, stock_name))
    return all_stocks_list

# -------------------
# App Initialization
# -------------------
st.set_page_config(page_title="Dashboard", layout="wide")
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

# --- Add Sector ---
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

# --- Add Industry ---
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

# --- Add Sub-Industry ---
with col3:
    st.subheader("📁 Sub-Industry")
    if sectors:
        selected_sector_sub = st.selectbox("Sector", list(sectors.keys()), key="sub_sector_select")
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

# --- Add Stock ---
with col4:
    st.subheader("📈 Stock")
    if sectors:
        selected_sector_stock = st.selectbox("Sector", list(sectors.keys()), key="stock_sector_select")
        industries = sectors[selected_sector_stock]
        if industries:
            selected_industry_stock = st.selectbox("Industry", list(industries.keys()), key="stock_industry_select")
            sub_data = industries[selected_industry_stock]

            # Check if sub-industries exist
            if isinstance(sub_data, dict) and sub_data:
                selected_subindustry_stock = st.selectbox("Sub-Industry", list(sub_data.keys()), key="stock_subindustry_select")
                new_stock = st.text_input("New Stock:", key="stock_input")
                if st.button("➕ Add Stock", key="add_stock"):
                    stocks = sub_data[selected_subindustry_stock]
                    if new_stock and all((new_stock != s.get("name") if isinstance(s, dict) else new_stock != s) for s in stocks):
                        stocks.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_subindustry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
            else:
                new_stock = st.text_input("New Stock Directly:", key="stock_input_direct")
                if st.button("➕ Add Stock Directly", key="add_stock_direct"):
                    if isinstance(sub_data, dict):
                        industries[selected_industry_stock] = []
                        sub_data = industries[selected_industry_stock]
                    if new_stock and all((new_stock != s.get("name") if isinstance(s, dict) else new_stock != s) for s in sub_data):
                        sub_data.append(new_stock)
                        save_data(sectors)
                        st.success(f"Added {new_stock} to {selected_industry_stock}")
                    else:
                        st.warning("Stock already exists or invalid.")
        else:
            st.info("Add an industry first.")
    else:
        st.info("Add a sector first.")


# Custom CSS for better styling
st.markdown("""
<style>
    .sector-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #3498db;
    }
    .industry-header {
        background: #ecf0f1;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sub-industry-box {
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
        margin: 5px 0;
        height: 100%;
    }
    .stock-item {
        padding: 5px 0;
        border-bottom: 1px solid #eee;
        font-size: 13px;
    }
    .stock-item:last-child {
        border-bottom: none;
    }
    .empty-state {
        color: #95a5a6;
        font-style: italic;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


def format_stock_display(stock_info):
    """
    Format stock display with symbol, name, and optional metrics
    stock_info can be string or dict with details
    """
    if isinstance(stock_info, str):
        return f"<span style='color:#2c3e50; font-weight:500;'>{stock_info}</span>"
    elif isinstance(stock_info, dict):
        symbol = stock_info.get('symbol', 'N/A')
        name = stock_info.get('name', '')
        price = stock_info.get('price', '')
        change = stock_info.get('change', 0)
        
        # Color based on change
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


# Main Dashboard Layout
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
            # Sector Header with expander for collapsible view
            with st.expander(f"🏦 **{sector}**", expanded=False):
                
                if not industries:
                    st.markdown("<p class='empty-state'>No industries added</p>", unsafe_allow_html=True)
                else:
                    for industry, sub_data in industries.items():
                        # Industry Header
                        st.markdown(f"""
                            <div class='industry-header'>
                                <strong style='color:#2c3e50; font-size:15px;'>🏭 {industry}</strong>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Check if sub_data is dict (has sub-industries) or list (direct stocks)
                        if isinstance(sub_data, dict):
                            if not sub_data:
                                st.markdown("<p class='empty-state'>No sub-industries</p>", unsafe_allow_html=True)
                            else:
                                # Display sub-industries in TWO COLUMNS
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
                                            # Sub-industry with stock count
                                            stock_count = len(stocks) if stocks else 0
                                            st.markdown(f"""
                                                <div class='sub-industry-box'>
                                                    <strong style='color:#7f8c8d; font-size:13px;'>
                                                        📁 {sub} ({stock_count})
                                                    </strong>
                                            """, unsafe_allow_html=True)
                                            
                                            if stocks:
                                                for s in stocks:
                                                    st.markdown(
                                                        f"<div class='stock-item'>• {format_stock_display(s)}</div>",
                                                        unsafe_allow_html=True
                                                    )
                                            else:
                                                st.markdown("<p class='empty-state'>No stocks</p>", unsafe_allow_html=True)
                                            
                                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        elif isinstance(sub_data, list):
                            # Direct stock list under industry - Display in TWO COLUMNS
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
