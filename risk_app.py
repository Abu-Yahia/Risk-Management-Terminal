import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk Intelligence 2026", layout="wide")

# 1. الربط باستخدام الموديل الموجود في حسابك فعلياً
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # اخترنا gemini-2.0-flash لأنه أسرع وأدق في تحليل البيانات
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("API Key Missing")
    st.stop()

st.title("🛡️ SEF Risk Intelligence (v2.0)")
u = st.text_input("Risk Subject (e.g., Supply chain disruption):")

if st.button("🚀 Run Analysis"):
    if u:
        with st.spinner("AI is analyzing (Gemini 2.0)..."):
            try:
                # طلب التحليل للـ 28 حقل
                p = "Analyze risk: " + u + ". Return ONLY a JSON object with exactly 28 project risk fields (ID, Description, Category, Owner, Mitigation, Score, etc.)."
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
                st.error("Error during analysis: " + str(e))

if 'd' in st.session_state:
    data = st.session_state['d']
    st.success("Analysis Complete for 28 Fields")
    
    # عرض النتائج في جدول احترافي
    df = pd.DataFrame(list(data.items()), columns=['Risk Field', 'AI Analysis'])
    st.table(df)
    
    # تحويل البيانات لـ CSV للتحميل
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download Full Report (CSV)", csv, "risk_report.csv", "text/csv")
