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
    st.error("⚠️ يرجى إضافة OPENAI_API_KEY في الـ Secrets أولاً.")

# --- 3. قائمة الأقسام الرئيسية (بناءً على الصورة) ---
MAIN_CATEGORIES = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

# --- 4. دالة توليد المخاطر ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze the risk subject: '{subject}'. 
    Provide a professional risk assessment in JSON format with exactly 28 fields.
    Constraint: The 'Main Category' MUST be one of these: {", ".join(MAIN_CATEGORIES)}.
    
    Fields:
    1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date, 
    6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s), 
    10. Main Category, 11. Sub Category, 12. Risk Owner, 13. Trigger Condition(s), 
    14. WBS / Activity, 15. Objective / Value, 16. Rank, 17. Risk Score, 
    18. Treatment Strategy, 19. Response Plan, 20. Action Owner, 
    21. Action Progress Status, 22. % Action Completion, 23. Action Finish Date, 
    24. Action Type, 25. Qualitative Impact, 26. Probability Level, 
    27. Residual Risk, 28. Notes.
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
        st.error(f"Error: {e}")
        return None

# --- 5. واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence Terminal")
st.markdown(f"<p style='color: #555;'>Categories: {', '.join(MAIN_CATEGORIES)}</p>", unsafe_allow_html=True)

subject_input = st.text_input("Enter Risk Subject (e.g., Delay in site access):")

if st.button("🚀 Generate 28-Point Analysis"):
    if subject_input:
        with st.spinner("AI is categorizing and analyzing..."):
            result = generate_risk_details(subject_input)
            if result:
                st.session_state['current_risk'] = result
                st.success("Analysis Generated!")
    else:
        st.warning("Please enter a subject.")

# --- 6. عرض وحفظ البيانات ---
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    # بطاقات المؤشرات الأساسية
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", data.get("Risk Score", "0"))
    c2.metric("Category", data.get("Main Category", "N/A"))
    c3.metric("Rank", data.get("Rank", "0"))
    c4.metric("Status", data.get("Risk Status", "N/A"))

    st.divider()

    # عرض الـ 28 نقطة في عمودين
    st.subheader("📋 Comprehensive Risk Registry")
    items = list(data.items())
    col_left, col_right = st.columns(2)
    
    for i, (key, value) in enumerate(items):
        if i < 14:
            col_left.write(f"**{i+1}. {key}:** {value}")
        else:
            col_right.write(f"**{i+1}. {key}:** {value}")

    st.divider()

    # زر التحميل (CSV)
    df = pd.DataFrame([data])
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Download Full Report (CSV)",
        data=csv_data,
        file_name=f"Risk_{data.get('Risk ID', 'Report')}.csv",
        mime='text/csv'
    )
