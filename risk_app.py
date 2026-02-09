import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# 2. الربط بـ Gemini - استخدام الموديل المستقر
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # تغيير الاسم هنا لحل مشكلة 404
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
else:
    st.error("⚠️ Missing GEMINI_API_KEY in Secrets!")
    st.stop()

# 3. القائمة الرسمية للأقسام
CATS = ["CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", "PROCUREMENT", 
        "HEALTH_SAFETY", "PROJECT_MANAGEMENT", "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"]

st.title("🛡️ SEF Risk Intelligence Terminal")

subj = st.text_input("Enter Risk Subject:")

if st.button("🚀 Analyze Risk (28 Fields)"):
    if subj:
        with st.spinner("Analyzing..."):
            prompt = f"Analyze risk: '{subj}'. Return ONLY JSON with 28 fields. Categories: {CATS}."
            try:
                # طلب توليد المحتوى
                response = model.generate_content(prompt)
                # تنظيف النص من أي زوائد
                res_text = response.text.strip()
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0]
                elif "```" in res_text:
                    res_text = res_text.split("```")[1].split("```")[0]
                
                risk_data = json.loads(res_text)
                st.session_state['current_analysis'] = risk_data
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a subject.")

# 4. عرض النتائج
if 'current_analysis' in st.session_state:
    data = st.session_state['current_analysis']
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Score", data.get("Risk Score", "N/A"))
    col_m2.metric("Category", data.get("Main Category", "N/A"))
    col_m3.metric("Status", data.get("Risk Status", "N/A"))
    
    st.divider()
    
    all_items = list(data.items())
    c_left, c_right = st.columns(2)
    for i, (key, value) in enumerate(all_items):
        if i < 14: c_left.write(f"**{key}:** {value}")
        else: c_right.write(f"**{key}:** {value}")
            
    st.divider()
    df = pd.DataFrame([data])
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download CSV", csv, "Risk_Report.csv", "text/csv")
