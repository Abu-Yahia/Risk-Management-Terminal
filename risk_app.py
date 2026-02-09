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
    st.error("⚠️ لم يتم العثور على مفتاح API في الـ Secrets. يرجى إضافته أولاً.")

# --- 3. دالة توليد المخاطر (28 حقل) ---
def generate_risk_details(subject):
    prompt = f"""
    Analyze the risk: '{subject}'. 
    Provide a professional assessment for exactly 28 fields in JSON format.
    Fields to include:
    1. Risk ID, 2. Key Risks, 3. Risk Type, 4. Risk Status, 5. Identification Date, 
    6. Risk Statement, 7. Cause(s), 8. Risk Event Description, 9. Consequence(s), 
    10. Main Category, 11. Sub Category, 12. Risk Owner, 13. Trigger Condition(s), 
    14. WBS / Activity, 15. Objective / Value, 16. Rank, 17. Risk Score, 
    18. Treatment Strategy, 19. Response Plan, 20. Action Owner, 
    21. Action Progress Status, 22. % Action Completion, 23. Action Finish Date, 
    24. Action Type, 25. Qualitative Impact, 26. Probability Level, 27. Residual Risk, 28. Notes.
    
    Return ONLY the JSON object.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # أو gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # بيانات احتياطية في حال فشل الاتصال
        return {
            "Risk ID": f"RSK-{int(datetime.now().timestamp())}",
            "Key Risks": subject,
            "Risk Score": "Error in AI Connection",
            "Notes": str(e)
        }

# --- 4. واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence Terminal")
st.markdown("<p style='color: gray;'>Created by Abu Yahia | Professional Risk Management</p>", unsafe_allow_html=True)

subject_input = st.text_input("Enter Risk Subject (e.g., Delay in construction):")

if st.button("🚀 Generate Full 28-Field Analysis"):
    if subject_input:
        with st.spinner("AI is analyzing all 28 risk dimensions..."):
            risk_data = generate_risk_details(subject_input)
            st.session_state['current_risk'] = risk_data
            st.success("Analysis Complete!")
    else:
        st.warning("Please enter a subject.")

# --- 5. عرض النتائج وحفظها ---
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    # عرض المؤشرات الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Risk Score", data.get("Risk Score", "N/A"))
    col2.metric("Rank", data.get("Rank", "N/A"))
    col3.metric("Owner", data.get("Risk Owner", "N/A"))
    col4.metric("Status", data.get("Risk Status", "N/A"))

    st.divider()

    # عرض الـ 28 حقل كاملة
    st.subheader("📋 Comprehensive Risk Registry (28 Points)")
    
    # تقسيم العرض لسهولة القراءة
    items = list(data.items())
    half = len(items) // 2
    
    left_col, right_col = st.columns(2)
    with left_col:
        for key, value in items[:half]:
            st.write(f"**{key}:** {value}")
            
    with right_col:
        for key, value in items[half:]:
            st.write(f"**{key}:** {value}")

    st.divider()

    # زر الحفظ
    if st.button("💾 Save Risk to CSV Database"):
        df = pd.DataFrame([data])
        # في Streamlit Cloud لا يمكن تعديل ملفات السورس بسهولة، لكن سنعرضه للتحميل
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download Registry as CSV", data=csv, file_name=f"risk_{data['Risk ID']}.csv")
        st.toast("Risk ready for download!")
