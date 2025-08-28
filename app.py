import streamlit as st
from forms import (
    lead_occupational,
    lead_env_adult_history,
    lead_env_adult_investigation,
    lead_env_child_history,
    lead_env_child_investigation
)

# --- Page Configuration ---
st.set_page_config(
    page_title="SOP การสอบสวนโรค",
    layout="wide"
)

# --- Sidebar Navigation ---
st.sidebar.title("SOP การสอบสวนโรค")
st.sidebar.markdown("จากการประกอบอาชีพและสิ่งแวดล้อม")

# Dictionary to map form names to their render functions
FORMS = {
    "หน้าหลัก": None, # Placeholder for a potential welcome page
    "โรคจากตะกั่ว (จากการประกอบอาชีพ)": lead_occupational.render,
    "ซักประวัติผู้ใหญ่-สิ่งแวดล้อม (PbC04)": lead_env_adult_history.render,
    "สอบสวนผู้ใหญ่-สิ่งแวดล้อม (Pb-1)": lead_env_adult_investigation.render,
    "ซักประวัติเด็ก-สิ่งแวดล้อม (PbC01)": lead_env_child_history.render,
    "สอบสวนเด็ก-สิ่งแวดล้อม (Pb)": lead_env_child_investigation.render,
}

selection = st.sidebar.radio("เลือกแบบสอบสวน", list(FORMS.keys()))

# --- Main Content Area ---

# Get the selected function from the dictionary
selected_form_func = FORMS[selection]

# Call the selected function to render the form
if selected_form_func:
    selected_form_func()
else:
    # Display a welcome message or instructions on the main page
    st.header("ยินดีต้อนรับสู่ระบบ SOP การสอบสวนโรค")
    st.info("กรุณาเลือกแบบสอบสวนที่ต้องการจากเมนูด้านซ้ายมือเพื่อเริ่มต้น")
    st.image("https://images.unsplash.com/photo-1584824486509-112e4181ff6b?q=80&w=2070&auto=format&fit=crop",
             caption="Medical Professional using a tablet",
             use_column_width=True)

