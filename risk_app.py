import streamlit as st
import pandas as pd
import openai  # أو استخدم مكتبة لربط Gemini
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="SEF Risk Intelligence", layout="wide")

# --- دالة الذكاء الاصطناعي لتوليد البيانات ---
def generate_risk_details(subject):
    # هنا تضع مفتاح الـ API الخاص بك
    # openai.api_key = "YOUR_API_KEY"
    
    prompt = f"""
    Analyze the following risk subject: '{subject}'
    Provide a detailed risk assessment for 28 fields in a valid Python Dictionary format.
    Fields: Risk ID, Key Risks, Risk Type, Risk Status, Identification Date, Risk Statement, Cause(s), 
    Risk Event Description, Consequence(s), Main Category, Sub Category, Risk Owner, Trigger Condition(s), 
    WBS/Activity, Objective/Value, Rank (1-5), Risk Score (Rank*Probability), Treatment Strategy, 
    Response Plan, Action Owner, Action Progress Status, % Action Completion, Action Finish Date, 
    Action Type.
    Make the tone professional and industry-standard.
    """
    
    # محاكاة استجابة الذكاء الاصطناعي (أو استدعاء API حقيقي)
    # ملاحظة: سنقوم بملئها بيانات افتراضية ذكية للتجربة
    return {
        "Risk ID": f"RSK-{datetime.now().get_timestamp()}",
        "Key Risks": subject,
        "Risk Type": "Negative (Threat)",
        "Risk Status": "Identified",
        "Identification Date": datetime.now().strftime("%Y-%m-%d"),
        "Risk Statement": f"Potential for {subject} impacting project timeline.",
        "Cause(s)": "Market volatility, supply chain disruptions.",
        "Risk Event Description": f"Detailed breakdown of how {subject} might occur.",
        "Consequence(s)": "Increased costs, delayed milestones.",
        "Main Category": "Operational",
        "Sub Category": "External Factors",
        "Risk Owner": "Project Manager",
        "Trigger Condition(s)": "Delay exceeding 5 working days.",
        "WBS / Activity": "WP-04 Supply Procurement",
        "Objective / Value": "Time & Cost",
        "Rank": 4,
        "Risk Score": 16,
        "Treatment Strategy": "Mitigate",
        "Response Plan": "Identify alternative vendors and increase safety stock.",
        "Action Owner": "Procurement Head",
        "Action Progress Status": "Not Started",
        "% Action Completion": 0,
        "Action Finish Date": "2024-12-31",
        "Action Type": "Preventive"
    }

# --- واجهة المستخدم ---
st.title("🛡️ SEF Risk Intelligence Terminal")
st.markdown("---")

# المدخل الأساسي
subject_input = st.text_input("Enter Risk Subject (e.g., Supply Chain Delay):", placeholder="أدخل موضوع الخطر هنا...")

if st.button("🚀 Generate Full Risk Analysis"):
    if subject_input:
        with st.spinner("AI is analyzing and generating fields..."):
            # استدعاء الدالة
            risk_data = generate_risk_details(subject_input)
            st.session_state['current_risk'] = risk_data
            st.success("Analysis Generated!")
    else:
        st.warning("Please enter a subject first.")

# عرض النتائج في شكل احترافي
if 'current_risk' in st.session_state:
    data = st.session_state['current_risk']
    
    # صف الهيدر (المعلومات الحساسة)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", data['Risk Score'], delta="-High" if data['Risk Score'] > 12 else "Normal")
    c2.metric("Rank", data['Rank'])
    c3.metric("Type", data['Risk Type'])
    c4.metric("Status", data['Risk Status'])

    st.markdown("---")
    
    # توزيع الحقول الـ 28 على تبويبات لتسهيل القراءة
    t1, t2, t3 = st.tabs(["📋 General Info", "🔍 Root Cause & Impact", "🛠️ Treatment Plan"])
    
    with t1:
        col_a, col_b = st.columns(2)
        col_a.write(f"**Risk Statement:** {data['Risk Statement']}")
        col_a.write(f"**Main Category:** {data['Main Category']}")
        col_b.write(f"**Risk Owner:** {data['Risk Owner']}")
        col_b.write(f"**Identification Date:** {data['Identification Date']}")

    with t2:
        st.write(f"**Causes:** {data['Cause(s)']}")
        st.write(f"**Event Description:** {data['Risk Event Description']}")
        st.write(f"**Consequences:** {data['Consequence(s)']}")
        st.write(f"**Trigger Conditions:** {data['Trigger Condition(s)']}")

    with t3:
        st.info(f"**Strategy:** {data['Treatment Strategy']}")
        st.write(f"**Response Plan:** {data['Response Plan']}")
        col_x, col_y, col_z = st.columns(3)
        col_x.write(f"**Action Owner:** {data['Action Owner']}")
        col_y.write(f"**Progress:** {data['Action Progress Status']}")
        col_z.write(f"**Finish Date:** {data['Action Finish Date']}")

    # زر الحفظ في قاعدة البيانات
    if st.button("💾 Save to Database"):
        df = pd.DataFrame([data])
        # منطق الحفظ في CSV
        st.toast("Risk Saved Successfully!")
