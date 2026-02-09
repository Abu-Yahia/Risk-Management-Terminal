import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEF Risk Terminal (Offline)", layout="wide")

# 1. مكتبة المخاطر (يمكنك توسيعها كما تشاء)
RISK_LIBRARY = {
    "Equipment Failure": {
        "Risk ID": "RSK-001",
        "Key Risks": "Mechanical breakdown of heavy machinery",
        "Risk Type": "Negative",
        "Risk Status": "Active",
        "Main Category": "CONSTRUCTION",
        "Risk Owner": "Site Manager",
        "Risk Score": "12 (High)",
        "Response Plan": "Regular maintenance schedule and onsite spare parts.",
        "Notes": "Impacts timeline by 2 weeks."
        # يمكنك إضافة الـ 28 حقل هنا لكل خطر
    },
    "Design Delay": {
        "Risk ID": "RSK-002",
        "Key Risks": "Late approval of shop drawings",
        "Risk Type": "Negative",
        "Risk Status": "Identified",
        "Main Category": "DESIGN",
        "Risk Owner": "Technical Manager",
        "Risk Score": "9 (Medium)",
        "Response Plan": "Weekly coordination meetings with consultant.",
        "Notes": "Critical path item."
    }
}

st.title("🛡️ SEF Risk Intelligence (Static Mode)")

# 2. اختيار الخطر من القائمة
selected_risk = st.selectbox("Select a Risk to Analyze:", [""] + list(RISK_LIBRARY.keys()))

if selected_risk != "":
    data = RISK_LIBRARY[selected_risk]
    
    st.success(f"Analysis for: {selected_risk}")
    
    # عرض البيانات في جدول
    df = pd.DataFrame(list(data.items()), columns=['Field', 'Value'])
    st.table(df)
    
    # زر التحميل
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download Report", csv, "risk_report.csv")
else:
    st.info("Please select a risk from the menu to see the analysis.")
