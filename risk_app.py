import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk AI")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Key Missing")
    st.stop()

st.title("🛡️ Risk Analysis")
u = st.text_input("Subject:")

if st.button("Run"):
    if u:
        with st.spinner("Wait"):
            try:
                # لا يوجد f-string هنا لمنع الخطأ
                p = "Analyze risk: " + u + ". Return ONLY JSON with 28 fields."
                r = model.generate_content(p)
                t = r.text.strip().replace('```json', '').replace('```', '')
                d = json.loads(t)
                st.session_state['d'] = d
            except Exception as e:
                st.error(str(e))

if 'd' in st.session_state:
    data = st.session_state['d']
    st.table(pd.DataFrame(list(data.items())))
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("Save CSV", csv, "risk.csv")
