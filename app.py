import streamlit as st
from forms import (
    lead_occupational,
    lead_env_adult_history,
    lead_env_adult_investigation,
    lead_env_child_history,
    lead_env_child_investigation,
    silicosis,
    # --- Temporarily disable missing forms to prevent errors ---
    # asbestosis, 
    # confined_space,
    # pesticide,
    # pm25
)

# --- Page Configuration ---
st.set_page_config(
    page_title="SOP การสอบสวนโรค",
    layout="wide"
)

# --- A placeholder render function for pages under development ---
def render_placeholder():
    st.info("หน้านี้กำลังอยู่ในระหว่างการพัฒนา")

# --- Page Rendering Dictionary ---
PAGE_MAP = {
    "home": ("หน้าหลัก", lambda: st.header("ยินดีต้อนรับสู่ระบบ SOP การสอบสวนโรค") or st.info("กรุณาเลือกแบบสอบสวนจากเมนูด้านซ้าย")),
    
    # Occupational Diseases
    "occ_lead": ("โรคจากตะกั่ว (อาชีพ)", lead_occupational.render),
    "occ_silica": ("โรคจากฝุ่นซิลิกา", silicosis.render),
    "occ_asbestos": ("โรคจากแอสเบสตอส", render_placeholder), # Using placeholder
    "occ_confined_space": ("โรคจากภาวะอับอากาศ", render_placeholder), # Using placeholder
    "occ_pesticide": ("พิษจากสารกำจัดศัตรูพืช", render_placeholder), # Using placeholder

    # Environmental Diseases
    "env_lead_adult_history": ("ซักประวัติผู้ใหญ่-ตะกั่ว (PbC04)", lead_env_adult_history.render),
    "env_lead_adult_investigation": ("สอบสวนผู้ใหญ่-ตะกั่ว (Pb-1)", lead_env_adult_investigation.render),
    "env_lead_child_history": ("ซักประวัติเด็ก-ตะกั่ว (PbC01)", lead_env_child_history.render),
    "env_lead_child_investigation": ("สอบสวนเด็ก-ตะกั่ว (Pb)", lead_env_child_investigation.render),
    "env_pm25": ("โรคจากฝุ่น PM2.5", render_placeholder), # Using placeholder
}

# --- Session State Initialization ---
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "home"

def set_page(page_key):
    st.session_state.selected_page = page_key

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("เมนูแบบสอบสวน")
    
    with st.expander("โรคจากการประกอบอาชีพ", expanded=True):
        st.button("โรคจากตะกั่ว", on_click=set_page, args=("occ_lead",), use_container_width=True)
        st.button("โรคจากฝุ่นซิลิกา", on_click=set_page, args=("occ_silica",), use_container_width=True)
        st.button("โรคจากแอสเบสตอส", on_click=set_page, args=("occ_asbestos",), use_container_width=True)
        st.button("โรคจากภาวะอับอากาศ", on_click=set_page, args=("occ_confined_space",), use_container_width=True)
        st.button("พิษจากสารกำจัดศัตรูพืช", on_click=set_page, args=("occ_pesticide",), use_container_width=True)

    with st.expander("โรคจากสิ่งแวดล้อม", expanded=True):
        st.button("โรคจากฝุ่น PM2.5", on_click=set_page, args=("env_pm25",), use_container_width=True)
        
        st.markdown("**โรคจากตะกั่ว (สิ่งแวดล้อม)**")
        st.button("ซักประวัติผู้ใหญ่ (PbC04)", on_click=set_page, args=("env_lead_adult_history",), use_container_width=True)
        st.button("สอบสวนผู้ใหญ่ (Pb-1)", on_click=set_page, args=("env_lead_adult_investigation",), use_container_width=True)
        st.button("ซักประวัติเด็ก (PbC01)", on_click=set_page, args=("env_lead_child_history",), use_container_width=True)
        st.button("สอบสวนเด็ก (Pb)", on_click=set_page, args=("env_lead_child_investigation",), use_container_width=True)

# --- Main Content Area ---
page_title, render_function = PAGE_MAP.get(st.session_state.selected_page, PAGE_MAP["home"])
render_function()
