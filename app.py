import streamlit as st
import os
import glob

# --- Page Configuration ---
st.set_page_config(
    page_title="SOP การสอบสวนโรค",
    layout="wide"
)

# --- Helper Functions ---

def read_html_file(path):
    """อ่านไฟล์ HTML และคืนค่าเป็น string"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"<p>Error: ไม่พบไฟล์ {os.path.basename(path)}</p>"

def get_html_pages(folder_path):
    """ค้นหาไฟล์ HTML ทั้งหมดในโฟลเดอร์ที่ระบุ และจัดเรียงตามชื่อ"""
    search_path = os.path.join(folder_path, "*.html")
    files = glob.glob(search_path)
    # จัดเรียงไฟล์เพื่อให้เมนูเป็นไปตามลำดับ
    files.sort()
    # สร้าง dictionary โดยมี key เป็นชื่อที่สวยงามสำหรับแสดงผล และ value เป็น path ของไฟล์
    pages = {os.path.basename(f).split('_', 1)[1].replace('.html', '').replace('_', ' ').title(): f for f in files}
    return pages

# --- Main Application ---

st.title("ระบบ SOP การสอบสวนโรค")
st.markdown("จากการประกอบอาชีพและสิ่งแวดล้อม")

# --- Sidebar Navigation ---
PAGES_DIR = "pages"
pages_dict = get_html_pages(PAGES_DIR)

st.sidebar.header("เมนูนำทาง")
selection = st.sidebar.radio("เลือกหน้าที่ต้องการ", list(pages_dict.keys()))

# --- HTML Content Display ---

# อ่านส่วนหัวและส่วนท้ายที่ใช้ร่วมกัน
header_html = read_html_file(os.path.join("common", "header.html"))
footer_html = read_html_file(os.path.join("common", "footer.html"))

# อ่านเนื้อหาของหน้าที่ถูกเลือก
selected_page_path = pages_dict[selection]
page_content_html = read_html_file(selected_page_path)

# รวม HTML ทั้งหมดเข้าด้วยกัน
full_html = f"{header_html}{page_content_html}{footer_html}"

# แสดงผล HTML
# ปรับความสูงให้ยืดหยุ่นตามเนื้อหา
st.components.v1.html(full_html, height=1800, scrolling=True)

st.sidebar.info(f"กำลังแสดงผล: **{selection}**")
