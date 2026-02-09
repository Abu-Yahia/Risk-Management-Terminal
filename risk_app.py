import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Risk Intelligence", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # غيرنا الموديل لنسخة Flash Latest الموجودة في قائمتك لتجنب الـ 429 على الموديل السابق
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("API Key Missing")
    st.stop()

st.title("🛡️ SEF Risk Intelligence")
u = st.text_input("Risk Subject:")

if st.button("🚀 Run Analysis"):
    if u:
        with st.spinner("AI is analyzing (Switched to Stable Model)..."):
            try:
                p = "Analyze risk: " + u + ". Return ONLY JSON with 28 fields."
                r = model.generate_content(p)
                t = r.text.strip()
                
                if "```json" in t:
                    t = t.split("```json")[1].split("```")[0]
                elif "```" in t:
                    t = t.split("```")[1].split("```")[0]
                
                d = json.loads(t)
                st.session_state['d'] = d
            except Exception as e:
                st.error("Quota or API Error: " + str(e))
                st.info("Try again in 1 minute if it's a rate limit issue.")

if 'd' in st.session_state:
    data = st.session_state['d']
    st.success("Analysis Complete")
    st.table(pd.DataFrame(list(data.items()), columns=['Field', 'Value']))
    csv = pd.DataFrame([data]).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Save CSV", csv, "risk.csv")
