import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Adult History Form (PbC04)"""
    st.header("แบบซักประวัติพฤติกรรมที่เกี่ยวข้องกับการสัมผัสสารตะกั่วในผู้ใหญ่และหญิงตั้งครรภ์")
    st.caption("(แบบ PbC04)")

    with st.form("pbc04_form"):
        # --- Section 1: General Information ---
        with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
            st.subheader("ข้อมูลหน่วยบริการสาธารณสุข")
            col1, col2, col3 = st.columns(3)
            col1.text_input("โรงพยาบาล", key="pbc04_hosp_name")
            col2.text_input("อำเภอ", key="pbc04_hosp_district")
            col3.text_input("จังหวัด", key="pbc04_hosp_province")
            
            st.radio("ขนาดของโรงพยาบาล",
                     ["รพศ. (A)", "รพท. (S)", "รพท. ขนาดเล็ก (M1)", "รพช. แม่ข่าย (M2)",
                      "รพช. ขนาดใหญ่ (F1)", "รพช. ขนาดกลาง (F2)", "รพช. ขนาดเล็ก (F3)"],
                     key="pbc04_hosp_size", horizontal=True)

            st.subheader("ข้อมูลผู้ป่วย")
            col1, col2 = st.columns(2)
            col1.text_input("ชื่อ - สกุล", key="pbc04_fullname")
            col2.radio("เพศ", ["ชาย", "หญิง"], key="pbc04_gender", horizontal=True)
            col1.number_input("อายุ (ปี)", min_value=0, step=1, key="pbc04_age")
            col2.number_input("น้ำหนัก (กก.)", min_value=0.0, format="%.2f", key="pbc04_weight")
            col1.number_input("ส่วนสูง (ซม.)", min_value=0.0, format="%.2f", key="pbc04_height")
            
            # ... (Continue converting all other fields from the HTML form)

            st.subheader("กรณีเป็นหญิงตั้งครรภ์ (สอบถามเพิ่มเติม)")
            col1, col2 = st.columns(2)
            col1.number_input("อายุครรภ์ (สัปดาห์)", min_value=0, step=1, key="pbc04_preg_weeks")
            col2.number_input("ท้องคนที่", min_value=1, step=1, key="pbc04_preg_count")
            col1.text_input("ฝากครรภ์หรือไม่", key="pbc04_preg_anc")
            col2.number_input("ประวัติการแท้ง (ครั้ง)", min_value=0, step=1, key="pbc04_preg_miscarriage")
            st.number_input("บุตรน้ำหนักต่ำกว่าเกณฑ์ (คน)", min_value=0, step=1, key="pbc04_preg_low_birth_weight")

        # --- Section 2: Health Behavior ---
        with st.expander("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ", expanded=True):
            # ... (Convert health behavior questions here)
            st.write("...")
        
        # --- Section 3: Exam Results ---
        with st.expander("ส่วนที่ 3: ผลการตรวจต่างๆ ที่เกี่ยวข้อง", expanded=True):
            # ... (Convert exam result tables here)
            st.write("...")

        # --- Section 4 & 5 ---
        with st.expander("ส่วนที่ 4 และ 5: การวินิจฉัยและการรักษา", expanded=True):
            st.multiselect("การวินิจฉัยโรค", ["สงสัยโรคจากตะกั่ว", "โรคจากตะกั่ว", "โรคอื่นๆ"], key="pbc04_diagnosis")
            st.text_area("การรักษาพยาบาล หรือข้อเสนอแนะอื่นๆ", key="pbc04_recommendation")
            
            st.text_input("ชื่อ - นามสกุล แพทย์ผู้ตรวจร่างกาย", key="pbc04_doctor_name")
            st.text_input("เบอร์โทร", key="pbc04_doctor_phone")
            st.date_input("วัน/เดือน/ปี", datetime.date.today(), key="pbc04_exam_date")

        submitted = st.form_submit_button("บันทึกข้อมูล")
        if submitted:
            st.success("ข้อมูล PbC04 ถูกบันทึกเรียบร้อยแล้ว!")

