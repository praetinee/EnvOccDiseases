# praetinee/envoccdiseases/Envoccdiseases-main/app.py
import streamlit as st
import sys
import os

# --- PATH CORRECTION ---
# This code adds the project's root directory to Python's path.
# This ensures that Python can find the 'forms' module regardless of
# how the script is executed.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


# --- CORRECTED IMPORTS ---
# We are now importing each form's render function directly
# and giving it a unique alias to avoid name conflicts.
from forms.lead_occupational import render as lead_occupational_render
from forms.lead_occupational_medical import render as lead_occupational_medical_render
from forms.lead_env_adult_history import render as lead_env_adult_history_render
from forms.lead_env_adult_investigation import render as lead_env_adult_investigation_render
from forms.lead_env_child_history import render as lead_env_child_history_render
from forms.lead_env_child_investigation import render as lead_env_child_investigation_render
from forms.silicosis import render as silicosis_render
from forms.confined_space import render as confined_space_render
from forms.pesticide import render as pesticide_render
from forms.pm25 import render as pm25_render


# --- Page Configuration ---
st.set_page_config(
    page_title="SOP การสอบสวนโรค",
    layout="wide"
)

# --- A placeholder render function for pages under development ---
def render_placeholder():
    st.info("หน้านี้กำลังอยู่ในระหว่างการพัฒนา")

# --- PAGE MAPPING UPDATE ---
# The keys remain the same, but the render functions now point to our new aliases.
PAGE_MAP = {
    "home": ("หน้าหลัก", lambda: st.header("ยินดีต้อนรับสู่ระบบ SOP การสอบสวนโรค") or st.info("กรุณาเลือกแบบสอบสวนจากเมนูด้านซ้าย")),

    # Occupational Diseases
    "occ_lead_investigation": ("แบบสอบสวน (เจ้าหน้าที่)", lead_occupational_render),
    "occ_lead_medical": ("แบบบันทึกตรวจร่างกาย (แพทย์)", lead_occupational_medical_render),
    "occ_silica": ("โรคจากฝุ่นซิลิกา", silicosis_render),
    "occ_confined_space": ("โรคจากภาวะอับอากาศ", confined_space_render),
    "occ_pesticide": ("พิษจากสารกำจัดศัตรูพืช", pesticide_render),

    # Environmental Diseases
    "env_lead_adult_history": ("ซักประวัติผู้ใหญ่-ตะกั่ว (PbC04)", lead_env_adult_history_render),
    "env_lead_adult_investigation": ("สอบสวนผู้ใหญ่-ตะกั่ว (Pb-1)", lead_env_adult_investigation_render),
    "env_lead_child_history": ("ซักประวัติเด็ก-ตะกั่ว (PbC01)", lead_env_child_history_render),
    "env_lead_child_investigation": ("สอบสวนเด็ก-ตะกั่ว (Pb)", lead_env_child_investigation_render),
    "env_pm25": ("โรคจากฝุ่น PM2.5", pm25_render),
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
        st.markdown("**โรคจากตะกั่ว**")
        st.button("แบบสอบสวน (เจ้าหน้าที่)", on_click=set_page, args=("occ_lead_investigation",), use_container_width=True)
        st.button("แบบบันทึกตรวจร่างกาย (แพทย์)", on_click=set_page, args=("occ_lead_medical",), use_container_width=True)
        st.markdown("---")
        st.button("โรคจากฝุ่นซิลิกา", on_click=set_page, args=("occ_silica",), use_container_width=True)
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
