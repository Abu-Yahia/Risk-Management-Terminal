import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk AI", layout="wide")

# إعداد المفتاح
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("API Key Missing")
    st.stop()

st.title("🛡️ Risk Terminal")
u_input = st.text_input("Enter Risk Subject:")

if st.button("Analyze"):
    if u_input:
        with st.spinner("Wait..."):
            try:
                # استخدمنا الجمع العادي بدل f-string لمنع الخطأ
                p = "Analyze this risk: " + u_input + ". Return ONLY JSON with 28 fields."
                res = model.generate_content(p)
                txt = res.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(txt)
                st.session_state['data'] = data
            except Exception as e:
                st.error("Error: " + str(e))

if 'data' in st.session_state:
    d = st.session_state['data']
    st.success("Analysis Complete")
    # عرض النتائج في جدول
    df = pd.DataFrame(list(d.items()), columns=['Field', 'Value'])
    st.table(df)
    
    csv_data = pd.DataFrame([d]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("Download CSV", csv_data, "risk.csv")
