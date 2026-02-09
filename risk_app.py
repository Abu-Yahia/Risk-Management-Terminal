import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# 2. الربط بـ Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Missing GEMINI_API_KEY in Secrets!")
    st.stop()

# 3. القائمة الرسمية (الـ 10 أقسام)
CATS = ["CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", "PROCUREMENT", 
        "HEALTH_SAFETY", "PROJECT_MANAGEMENT", "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"]

st.title("🛡️ SEF Risk Intelligence Terminal")

subj = st.text_input("Enter Risk Subject (e.g., Equipment failure):")

if st.button("🚀 Analyze Risk (28 Fields)"):
    if subj:
        with st.spinner("AI is generating 28 points analysis..."):
            prompt = f"Analyze
