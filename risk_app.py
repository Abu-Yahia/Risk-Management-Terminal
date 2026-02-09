import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# --- 2. تهيئة عميل OpenAI من الـ Secrets ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ خطأ: لم يتم العثور على OPENAI_API_KEY في إعدادات Secrets.")
    st.stop()

# --- 3. قائمة الأقسام الرئيسية (بناءً على صورتك المرفقة) ---
MAIN_CATEGORIES = [
    "CONSTRUCTION", "DESIGN", "INTERFACES", "COMMERCIAL", 
    "PROCUREMENT", "HEALTH_SAFETY", "PROJECT_MANAGEMENT", 
    "ORGANIZATION", "ENVIRONMENT", "EXTERNAL"
]

# --- 4. دالة توليد المخاطر (28 حقل) ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze the risk subject: '{subject}'. 
    Provide a professional risk assessment in JSON format with exactly 28 fields.
    Constraint: The 'Main Category' MUST be one of these: {", ".join(MAIN_CATEGORIES)}.
    
    Fields to include:
    1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date, 
    6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s), 
    10. Main Category, 11. Sub Category, 12. Risk Owner, 13. Trigger Condition(s), 
    14. WBS / Activity, 15. Objective / Value, 16. Rank, 17. Risk Score, 
    18. Treatment Strategy, 19. Response Plan, 20. Action Owner, 
    21. Action Progress Status, 22. % Action Completion, 23. Action Finish Date, 
    24. Action Type, 25. Qualitative Impact, 26. Probability Level, 
    27. Residual Risk, 28. Notes.
    
    Return ONLY a valid JSON object.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional Risk Manager expert in construction and project management."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # هنا تم إصلاح المسافات (Indentation Fixed)
        return {
            "Risk ID": f"RSK-{int(datetime.now().timestamp())}",
            "Key Risks": subject,
            "Risk Score": "Error",
            "Notes": f"API Error: {str(e)}"
        }

# --- 5. واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence Terminal")
st.markdown(f"<p style='color: #666;'>Authorized Categories: {', '.join(MAIN_CATEGORIES)}</p>", unsafe_allow_html=True)

subject_input = st.text_input("Enter
