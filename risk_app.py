import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk Terminal")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # جربنا هنا gemini-1.5-flash-8b لأنه الأكثر توافقاً مع v1beta
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
else:
    st.error("Missing API Key")
    st.stop()

st.title("🛡️ Risk Intelligence")
u = st.text_input("Risk Subject:")

if st.button("Analyze"):
    if u:
        with st.spinner("Analyzing..."):
            try:
                p = "Analyze risk: " + u + ". Return ONLY JSON with 28 fields."
                # محاولة توليد المحتوى
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
                # لو فشل، بيعطيك أسماء الموديلات المتاحة عندك في الـ Logs
                st.error("Error: " + str(e))
                st.write("Check logs for available models.")
                # سطر برمجي لمساعدتنا في معرفة الموديلات المتاحة لو استمر الخطأ
                print([m.name for m in genai.list_models()])

if 'd' in st.session_state:
    data = st.session_state['d']
    st.table(pd.DataFrame(list(data.items()), columns=['Field', 'Value']))
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("Save CSV", csv, "risk.csv")
