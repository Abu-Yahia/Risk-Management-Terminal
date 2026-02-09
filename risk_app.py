import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk Terminal")

# 1. الربط باستخدام gemini-pro (الموديل الأكثر توافقاً)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # استخدمنا gemini-pro لأنه الوحيد اللي شغال على كل الإصدارات القديمة والجديدة
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Missing API Key")
    st.stop()

st.title("🛡️ Risk Intelligence")
u = st.text_input("Risk Subject:")

if st.button("Analyze"):
    if u:
        with st.spinner("Analyzing..."):
            try:
                # طلب بسيط جداً لضمان عدم حدوث خطأ في الـ Prompt
                p = "Analyze risk: " + u + ". Return ONLY JSON with 28 fields."
                r = model.generate_content(p)
                t = r.text.strip()
                
                # تنظيف الـ JSON
                if "```json" in t:
                    t = t.split("```json")[1].split("```")[0]
                elif "```" in t:
                    t = t.split("```")[1].split("```")[0]
                
                d = json.loads(t)
                st.session_state['d'] = d
            except Exception as e:
                st.error("Error: " + str(e))
                # السطر ده هيطبع لك الموديلات المتاحة فعلاً في الـ Logs تحت
                try:
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.write("Available models in your account: " + str(models))
                except:
                    pass

if 'd' in st.session_state:
    data = st.session_state['d']
    st.success("Analysis Complete!")
    # عرض البيانات في جدول مرتب
    df = pd.DataFrame(list(data.items()), columns=['Field', 'Value'])
    st.table(df)
    
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("Save CSV", csv, "risk_report.csv")
