import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# --- 2. تهيئة عميل OpenAI ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Error: Check your OpenAI API Key in Streamlit Secrets.")
    st.stop()

# --- 3. قائمة الأقسام المعتمدة من صورتك ---
MAIN_CATEGORIES = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

# --- 4. دالة التحليل الذكي ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze the risk subject: '{subject}'. 
    Provide a professional assessment in JSON format with exactly 28 fields.
    Constraint: The 'Main Category' MUST be one of these: {", ".join(MAIN_CATEGORIES)}.
    Fields: 1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date, 6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s), 10. Main Category, 11. Sub Category, 12. Risk Owner, 13. Trigger Condition(s), 14. WBS / Activity, 15. Objective / Value, 16. Rank, 17. Risk Score, 18. Treatment Strategy, 19. Response Plan, 20. Action Owner, 21. Action Progress Status, 22. % Action Completion, 23. Action Finish Date, 24. Action Type, 25. Qualitative Impact, 26. Probability Level, 27. Residual Risk, 28. Notes.
    Return ONLY a valid JSON.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a professional Risk Manager."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # إصلاح خطأ التوقيت يدوياً هنا
        return {
            "Risk ID": f"RSK-{int(datetime.now().timestamp())}",
            "Key Risks": subject,
            "Main Category": "ANALYSIS_ERROR",
            "Notes": str(e)
        }

# --- 5. واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence Terminal")
st.markdown("---")

subject_input = st.text_input("Enter Risk Subject (e.g., Late delivery of materials):")

if st.button("🚀 Run Comprehensive 28-Point Analysis"):
    if subject_input:
        with st.spinner("AI is analyzing all 28 dimensions..."):
            result = generate_risk_details(subject_input)
            st.session_state['current_risk'] = result
    else:
        st.warning("Please enter a subject.")

# --- 6. عرض النتائج وحفظها ---
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    # مؤشرات علوية ملونة
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", data.get("Risk Score", "N/A"))
    c2.metric("Category", data.get("Main Category", "N/A"))
    c3.metric("Rank", data.get("Rank", "N/A"))
    c4.metric("Status", data.get("Risk Status", "N/A"))

    st.markdown("### 📋 Full Risk Registry")
    
    # توزيع الـ 28 حقل في عمودين
    items = list(data.items())
    col_left, col_right = st.columns(2)
    
    for i, (key, value) in enumerate(items):
        if i % 2 == 0:
            col_left.write(f"**{key}:** {value}")
        else:
            col_right.write(f"**{key}:** {value}")

    st.divider()
    
    # زر التحميل
    df = pd.DataFrame([data])
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Download This Analysis (CSV)",
        data=csv_data,
        file_name=f"Risk_{data.get('Risk ID','Report')}.csv",
        mime='text/csv'
    )
