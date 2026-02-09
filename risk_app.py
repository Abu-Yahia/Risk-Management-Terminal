import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# --- 2. تهيئة Google Gemini من الـ Secrets ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # استخدام الموديل الأكثر استقراراً
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    else:
        st.error("⚠️ يرجى إضافة GEMINI_API_KEY في Secrets")
        st.stop()
except Exception as e:
    st.error(f"⚠️ خطأ في الإعداد: {e}")
    st.stop()

# --- 3. قائمة الأقسام الـ 10 المعتمدة ---
MAIN_CATEGORIES = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

# --- 4. دالة التحليل ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze risk: '{subject}'. 
    Return a professional assessment in JSON format with exactly 28 fields.
    Constraint: 'Main Category' MUST be one of: {", ".join(MAIN_CATEGORIES)}.
    Fields: 1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date, 6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s), 10. Main Category, 11. Sub Category, 12. Risk Owner, 13. Trigger Condition(s), 14. WBS / Activity, 15. Objective / Value, 16. Rank, 17. Risk Score, 18. Treatment Strategy, 19. Response Plan, 20. Action Owner, 21. Action Progress Status, 22. % Action Completion, 23. Action Finish Date, 24. Action Type, 25. Qualitative Impact, 26. Probability Level, 27. Residual Risk, 28. Notes.
    Return ONLY JSON.
    """
    try:
        response = model.generate_content(prompt)
        # تنظيف استجابة JSON
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text_response)
    except Exception as e:
        return {
            "Risk ID": f"RSK-{int(datetime.now().timestamp())}",
            "Key Risks": subject,
            "Notes": f"Error detail: {str(e)}"
        }

# --- 5. واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence (Final Fixed)")

subject_input = st.text_input("Enter Risk Subject (e.g., Delay in structural steel delivery):")

if st.button("🚀 Analyze Now"):
    if subject_input:
        with st.spinner("AI is analyzing..."):
            result = generate_risk_details(subject_input)
            st.session_state['current_risk'] = result
    else:
        st.warning("Please enter a subject.")

# --- 6. عرض النتائج وحفظها ---
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", data.get("Risk Score", "N/A"))
    c2.metric("Category", data.get("Main Category", "N/A"))
    c3.metric("Rank", data.get("Rank", "N/A"))
    c4.metric("Status", data.get("Risk Status", "N/A"))

    st.divider()
    
    items = list(data.items())
    col_left, col_right = st.columns(2)
    for i, (key, value) in enumerate(items):
        if i % 2 == 0: col_left.write(f"**{key}:** {value}")
        else: col_right.write(f"**{key}:** {value}")

    st.divider()
    df = pd.DataFrame([data])
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download Full Report", csv_data, f"Risk_{data.get('Risk ID','ID')}.csv")
