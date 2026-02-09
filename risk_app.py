import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# 2. الربط بـ Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Missing GEMINI_API_KEY in Secrets!")
    st.stop()

# 3. القائمة الرسمية للأقسام (بناءً على صورتك)
CATS = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

st.title("🛡️ SEF Risk Intelligence Terminal")

subj = st.text_input("Enter Risk Subject:", placeholder="e.g., Delay in soil investigation")

if st.button("🚀 Analyze Risk (Full 28 Fields)"):
    if subj:
        with st.spinner("AI is analyzing all 28 fields..."):
            # الـ Prompt الكامل بأسماء الـ 28 حقل
            full_prompt = f"""
            Analyze the project risk: '{subj}'.
            Return ONLY a JSON object with exactly these 28 fields:
            1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date,
            6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s),
            10. Main Category (Must be one of: {CATS}), 11. Sub Category, 
            12. Risk Owner, 13. Trigger Condition(s), 14. WBS / Activity, 
            15. Objective / Value, 16. Rank, 17. Risk Score, 18. Treatment Strategy, 
            19. Response Plan, 20. Action Owner, 21. Action Progress Status, 
            22. % Action Completion, 23. Action Finish Date, 24. Action Type, 
            25. Qualitative Impact, 26. Probability Level, 27. Residual Risk, 28. Notes.
            """
            try:
                response = model.generate_content(full_prompt)
                # تنظيف الرد لتحويله لـ JSON
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                risk_data = json.loads(res_text)
                st.session_state['current_analysis'] = risk_data
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a subject first.")

# 4. عرض النتائج
if 'current_analysis' in st.session_state:
    data = st.session_state['current_analysis']
    
    # عرض الـ Metrics الأساسية
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Score", data.get("Risk Score", "N/A"))
    col_m2.metric("Category", data.get("Main Category", "N/A"))
    col_m3.metric("Rank", data.get("Rank", "N/A"))
    col_m4.metric("Status", data.get("Risk Status", "N/A"))
    
    st.divider()
    
    # عرض الـ 28 حقل كاملة
    st.subheader("📋 Full 28-Field Risk Registry")
    all_items = list(data.items())
    c_left, c_right = st.columns(2)
    
    for i, (key, value) in enumerate(all_items):
        if i < 14:
            c_left.write(f"**{key}:** {value}")
        else:
            c_right.write(f"**{key}:** {value}")
            
    st.divider()
    
    # تصدير البيانات
    df = pd.DataFrame([data])
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download CSV", csv, "Risk_Report.csv", "text/csv")
