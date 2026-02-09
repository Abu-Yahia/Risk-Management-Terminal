import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# --- 2. تهيئة عميل OpenAI ---
try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("⚠️ OPENAI_API_KEY not found in Secrets.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Error: {e}")
    st.stop()

# --- 3. الأقسام المعتمدة ---
MAIN_CATEGORIES = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

# --- 4. دالة التحليل ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze risk: '{subject}'. Return JSON with 28 fields.
    Main Category must be one of: {MAIN_CATEGORIES}.
    Include: Risk ID, Key Risks, Risk Type, Risk Status, Identification Date, Risk Statement, Cause(s), Risk Event Description, Consequence(s), Main Category, Sub Category, Risk Owner, Trigger Condition(s), WBS / Activity, Objective / Value, Rank, Risk Score, Treatment Strategy, Response Plan, Action Owner, Action Progress Status, % Action Completion, Action Finish Date, Action Type, Qualitative Impact, Probability Level, Residual Risk, Notes.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"Risk ID": "ERR-001", "Key Risks": subject, "Notes": str(e)}

# --- 5. الواجهة ---
st.title("🛡️ SEF Risk Intelligence Terminal")

subject_input = st.text_input("Enter Risk Subject:")

if st.button("🚀 Run 28-Point Analysis"):
    if subject_input:
        with st.spinner("Analyzing..."):
            res = generate_risk_details(subject_input)
            st.session_state['current_risk'] = res
    else:
        st.warning("Enter a subject.")

# --- 6. العرض وحفظ البيانات ---
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    # عرض الـ Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", data.get("Risk Score", "N/A"))
    c2.metric("Category", data.get("Main Category", "N/A"))
    c3.metric("Rank", data.get("Rank", "N/A"))
    c4.metric("Status", data.get
