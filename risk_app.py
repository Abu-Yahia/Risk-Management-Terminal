import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk Terminal")

# 1. الربط - جربنا gemini-1.5-flash مباشرة
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # استخدمنا الاسم الأساسي للموديل بدون إضافات لحل 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key")
    st.stop()

st.title("🛡️ Risk Intelligence")
u = st.text_input("Risk Subject:")

if st.button("Analyze"):
    if u:
        with st.spinner("Wait..."):
            try:
                # استخدمنا الجمع العادي بدل f-string عشان مشكلة القص
                p = "Analyze risk: " + u + ". Return ONLY JSON with 28 fields."
                r = model.generate_content(p)
                t = r.text.strip()
                
                # تنظيف الـ JSON لو فيه مارك داون
                if "```json" in t:
                    t = t.split("```json")[1].split("```")[0]
                elif "```" in t:
                    t = t.split("```")[1].split("```")[0]
                
                d = json.loads(t)
                st.session_state['d'] = d
            except Exception as e:
                st.error("Error: " + str(e))

if 'd' in st.session_state:
    data = st.session_state['d']
    st.success("Complete!")
    st.table(pd.DataFrame(list(data.items()), columns=['Field', 'Value']))
    
    # تحميل النتائج
    df = pd.DataFrame([data])
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("Save CSV", csv, "risk.csv")
