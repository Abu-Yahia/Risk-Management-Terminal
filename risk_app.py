import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk AI", layout="wide")

# الربط بالمفتاح
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Key Missing")
    st.stop()

st.title("🛡️ Risk Intelligence")
subj = st.text_input("Enter Risk:")

if st.button("Analyze"):
    if subj:
        with st.spinner("Wait..."):
            try:
                # برومبت مختصر جداً لمنع القطع
                p = f"Analyze risk: {subj}. Return ONLY JSON with 28 fields."
                r = model.generate_content(p)
                t = r.text.strip().replace('```json', '').replace('```', '')
                d = json.loads(t)
                st.session_state['res'] = d
            except Exception as e:
                st.error(f"Error: {e}")

if 'res' in st.session_state:
    res = st.session_state['res']
    # عرض البيانات كجدول لسهولة القراءة
    df = pd.DataFrame(list(res.items()), columns=['Field', 'Value'])
    st.table(df)
    
    csv = pd.DataFrame([res]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("Download CSV", csv, "report.csv")
