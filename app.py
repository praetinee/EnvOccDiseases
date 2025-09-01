# praetinee/envoccdiseases/Envoccdiseases-main/app.py
import streamlit as st
import os
import importlib.util

# --- DYNAMIC MODULE LOADING ---
# Due to persistent import issues in the execution environment,
# we are now dynamically loading each form module directly from its file path.
# This is a robust way to bypass Python's standard path resolution mechanism.

def load_render_function(form_name):
    """Dynamically loads a form module from the 'forms' directory and returns its render function."""
    # Construct the full path to the form's .py file
    app_dir = os.path.dirname(os.path.abspath(__file__))
    forms_dir = os.path.join(app_dir, 'forms')
    file_path = os.path.join(forms_dir, f"{form_name}.py")
    
    # Load the module from the file path
    spec = importlib.util.spec_from_file_location(form_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Return the render function from the loaded module
    return module.render

# Load all render functions using our dynamic loader
lead_occupational_render = load_render_function("lead_occupational")
lead_occupational_medical_render = load_render_function("lead_occupational_medical")
lead_env_adult_history_render = load_render_function("lead_env_adult_history")
lead_env_adult_investigation_render = load_render_function("lead_env_adult_investigation")
lead_env_child_history_render = load_render_function("lead_env_child_history")
lead_env_child_investigation_render = load_render_function("lead_env_child_investigation")
# Add the new form
lead_env_child_risk_render = load_render_function("lead_env_child_risk")
silicosis_render = load_render_function("silicosis")
confined_space_render = load_render_function("confined_space")
pesticide_render = load_render_function("pesticide")
pm25_render = load_render_function("pm25")


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
    "occ_silica": ("โรคซิลิโคสิสและโรคจากแอสเบสตอส", silicosis_render),
    "occ_confined_space": ("โรคจากภาวะอับอากาศ", confined_space_render),
    "occ_pesticide": ("พิษจากสารกำจัดศัตรูพืช", pesticide_render),

    # Environmental Diseases
    "env_lead_adult_history": ("ซักประวัติผู้ใหญ่-ตะกั่ว (PbC04)", lead_env_adult_history_render),
    "env_lead_adult_investigation": ("สอบสวนผู้ใหญ่-ตะกั่ว (Pb-1)", lead_env_adult_investigation_render),
    "env_lead_child_history": ("ซักประวัติเด็ก-ตะกั่ว (PbC01)", lead_env_child_history_render),
    "env_lead_child_investigation": ("สอบสวนเด็ก-ตะกั่ว (Pb)", lead_env_child_investigation_render),
    "env_lead_child_risk": ("ประเมินความเสี่ยงเด็ก-ตะกั่ว (PbC03)", lead_env_child_risk_render), # Add new page
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
        st.button("โรคซิลิโคสิสและโรคจากแอสเบสตอส", on_click=set_page, args=("occ_silica",), use_container_width=True)
        st.button("โรคจากภาวะอับอากาศ", on_click=set_page, args=("occ_confined_space",), use_container_width=True)
        st.button("พิษจากสารกำจัดศัตรูพืช", on_click=set_page, args=("occ_pesticide",), use_container_width=True)

    with st.expander("โรคจากสิ่งแวดล้อม", expanded=True):
        st.button("โรคจากฝุ่น PM2.5", on_click=set_page, args=("env_pm25",), use_container_width=True)

        st.markdown("**โรคจากตะกั่ว (สิ่งแวดล้อม)**")
        st.button("ซักประวัติผู้ใหญ่ (PbC04)", on_click=set_page, args=("env_lead_adult_history",), use_container_width=True)
        st.button("สอบสวนผู้ใหญ่ (Pb-1)", on_click=set_page, args=("env_lead_adult_investigation",), use_container_width=True)
        st.button("ซักประวัติเด็ก (PbC01)", on_click=set_page, args=("env_lead_child_history",), use_container_width=True)
        st.button("สอบสวนเด็ก (Pb)", on_click=set_page, args=("env_lead_child_investigation",), use_container_width=True)
        st.button("ประเมินความเสี่ยงเด็ก (PbC03)", on_click=set_page, args=("env_lead_child_risk",), use_container_width=True) # Add button for new form

# --- Main Content Area ---
page_title, render_function = PAGE_MAP.get(st.session_state.selected_page, PAGE_MAP["home"])
render_function()
