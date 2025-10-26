import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
import json
import os
from datetime import datetime

# Setup folder
REPORT_FOLDER = "saved_reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

st.set_page_config(layout="wide")
st.title("Professional Equity Research Template Manager")

# ------------------------
# Load previous report
st.sidebar.header("Load Previous Report")
all_files = [f for f in os.listdir(REPORT_FOLDER) if f.endswith(".json")]
all_files.sort(reverse=True)
selected_file = st.sidebar.selectbox("Select a report to load", ["New Report"] + all_files)

data = {}
if selected_file != "New Report":
    file_path = os.path.join(REPORT_FOLDER, selected_file)
    with open(file_path, "r") as f:
        data = json.load(f)
    st.sidebar.success(f"Loaded report: {selected_file}")

# ------------------------
# 0. Report Date
st.header("Report Date")
report_date = st.text_input("Report Date (YYYY-MM-DD)", data.get("report_date",""))
if st.button("Use Today's Date"):
    report_date = datetime.now().strftime("%Y-%m-%d")
    st.success(f"Report Date set: {report_date}")

# ------------------------
# 1. Company Overview
st.header("1. Company Overview")
company_overview_text = st.text_area("Paste Company Overview Table Here", data.get("company_overview",""), height=150)
col1, col2, col3 = st.columns(3)
company_name = col1.text_input("Company Name", data.get("company_name",""))
ticker = col2.text_input("Ticker Symbol", data.get("ticker",""))
recommendation = col3.selectbox("Recommendation", ["Buy", "Hold", "Sell"], index=["Buy","Hold","Sell"].index(data.get("recommendation","Buy")))

# ------------------------
# 2. Investment Thesis
st.header("2. Investment Thesis")
investment_thesis_text = st.text_area("Paste Investment Thesis / Table", data.get("investment_thesis",""), height=150)

# ------------------------
# 3. Financial Analysis
st.header("3. Financial Analysis")
financial_text = st.text_area("Paste Financial Table / Ratios", data.get("financial_analysis",""), height=150)

# ------------------------
# 4. Valuation
st.header("4. Valuation")
valuation_text = st.text_area("Paste Valuation Table / DCF / Relative Valuation", data.get("valuation",""), height=150)

# ------------------------
# 5. Business Quality Assessment
st.header("5. Business Quality Assessment")
business_quality_text = st.text_area("Paste Business Quality Table / Notes", data.get("business_quality",""), height=150)

# ------------------------
# 6. Risk Analysis
st.header("6. Risk Analysis")
risk_text = st.text_area("Paste Risk Analysis Table / Notes", data.get("risk_analysis",""), height=150)

# ------------------------
# 7. ESG / Sustainability
st.header("7. ESG / Sustainability")
esg_text = st.text_area("Paste ESG / Sustainability Table / Notes", data.get("esg",""), height=150)

# ------------------------
# 8. Technical / Trading Notes
st.header("8. Technical / Trading Notes")
technical_text = st.text_area("Paste Technical Analysis / Charts / Levels", data.get("technical",""), height=150)

# ------------------------
# 9. Conclusion
st.header("9. Conclusion")
conclusion_text = st.text_area("Paste Final Recommendation / Notes / Horizon", data.get("conclusion",""), height=150)

# ------------------------
# PDF Generation
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)  # Portrait A4
    width, height = A4
    x_margin = 40
    y_margin = 50
    y = height - y_margin

    def write_section(title, text, bold=True, size=14):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Courier", size)
        c.setFillColor(colors.darkblue if bold else colors.black)
        c.drawString(x_margin, y, title)
        y -= 20
        c.setFont("Courier", 11)
        for line in text.splitlines():
            c.drawString(x_margin + 10, y, line)
            y -= 15
            if y < y_margin:
                c.showPage()
                y = height - y_margin

    # Report Date
    write_section(f"Report Date: {report_date}", "", bold=False, size=12)

    # Sections
    write_section("1. Company Overview", company_overview_text)
    write_section("Key Info", f"Company: {company_name} | Ticker: {ticker} | Recommendation: {recommendation}", bold=False)
    write_section("2. Investment Thesis", investment_thesis_text)
    write_section("3. Financial Analysis", financial_text)
    write_section("4. Valuation", valuation_text)
    write_section("5. Business Quality Assessment", business_quality_text)
    write_section("6. Risk Analysis", risk_text)
    write_section("7. ESG / Sustainability", esg_text)
    write_section("8. Technical / Trading Notes", technical_text)
    write_section("9. Conclusion", conclusion_text)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ------------------------
# Save JSON Data
def save_json():
    data_to_save = {
        "report_date": report_date,
        "company_overview": company_overview_text,
        "company_name": company_name,
        "ticker": ticker,
        "recommendation": recommendation,
        "investment_thesis": investment_thesis_text,
        "financial_analysis": financial_text,
        "valuation": valuation_text,
        "business_quality": business_quality_text,
        "risk_analysis": risk_text,
        "esg": esg_text,
        "technical": technical_text,
        "conclusion": conclusion_text
    }
    filename = f"{company_name}_{report_date}.json"
    path = os.path.join(REPORT_FOLDER, filename)
    with open(path, "w") as f:
        json.dump(data_to_save, f, indent=4)
    return path

# ------------------------
if st.button("Save & Download Professional PDF"):
    if report_date == "":
        st.warning("Please set a report date (or click 'Use Today's Date').")
    else:
        pdf_buffer = generate_pdf()
        json_file = save_json()
        st.success(f"Data saved: {json_file}")
        st.download_button(
            "Download PDF",
            data=pdf_buffer,
            file_name=f"{company_name}_{report_date}_Equity_Research.pdf",
            mime="application/pdf"
        )
