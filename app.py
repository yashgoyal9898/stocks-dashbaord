# Home.py
import streamlit as st
from stock_dashbaord.stock_dashboard import stock_dashboard

st.set_page_config(page_title="Main Dashboard", layout="wide")

page = st.sidebar.selectbox("Go to Page", ["Home", "Stock Dashboard"])

if page == "Home":
    st.write("Welcome to the main dashboard!")
elif page == "Stock Dashboard":
    stock_dashboard()  # Calls your stock page
