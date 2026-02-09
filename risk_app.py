import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# 1. الإعدادات
st.set_page_config(page_title="Risk AI", layout="wide")

# 2. الربط (حل مشكلة 404)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # الموديل ده هو الأكثر استقراراً للـ API الحالي
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Add API Key in Secrets")
    st.stop()

st.title("🛡️ Risk Intelligence Terminal")
subj = st.text_input("Enter Risk:")

if st.button("Analyze"):
    if subj:
        with st.spinner("Wait..."):
            try:
                # برومبت بسيط لتقليل احتمالية الخطأ
                p = f"Analyze risk: {subj}. Return ONLY JSON with 28 project risk fields."
                r = model.generate_content(p)
                t = r.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(t)
                st.session_state['risk'] = data
            except Exception as e:
                st.error(f"Error: {e}")

# 3. العرض (تأكد أن هذا الجزء تم نسخه كاملاً)
if 'risk' in st.session_state:
    res = st.session_state['risk']
    st.write("### Analysis Results (28 Fields)")
    st.json(res) # عرض سريع للتأكد من البيانات
    
    df = pd.DataFrame([res])
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("Download CSV", csv, "report.csv")
