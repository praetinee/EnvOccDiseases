# -*- coding: utf-8 -*-
import streamlit as st
import datetime
from utils.g_sheets_connector import save_to_sheet

def render():
    """Renders the Lead Environmental Child History Form (PbC01)"""
    st.header("แบบซักประวัติพฤติกรรมที่เกี่ยวข้องกับการสัมผัสสารตะกั่ว")
    st.caption("ของเด็กแรกเกิดถึงอายุต่ำกว่า 15 ปี (แบบ PbC01)")

    form_data = {}
    SHEET_NAME = "LeadEnvChildHistory"

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        st.subheader("ข้อมูลหน่วยบริการสาธารณสุข")
        col1, col2, col3 = st.columns(3)
        form_data['โรงพยาบาล'] = col1.text_input("โรงพยาบาล")
        form_data['อำเภอ'] = col2.text_input("อำเภอ")
        form_data['จังหวัด'] = col3.text_input("จังหวัด")
        
        form_data['ขนาดโรงพยาบาล'] = st.selectbox(
            "ขนาดของโรงพยาบาล",
            ["-- เลือก --", "รพศ. (A)", "รพท. (S)", "รพท. ขนาดเล็ก (M1)", "รพช. แม่ข่าย (M2)",
             "รพช. ขนาดใหญ่ (F1)", "รพช. ขนาดกลาง (F2)", "รพช. ขนาดเล็ก (F3)"]
        )

        st.subheader("ข้อมูลเด็ก")
        form_data['ชื่อเด็ก'] = st.text_input("ชื่อ ด.ช./ด.ญ.:")
        form_data['เลขบัตรประชาชนเด็ก'] = st.text_input("เลขบัตรประชาชน:")
        
        col1, col2, col3 = st.columns(3)
        form_data['วันเกิด'] = col1.date_input("วัน/เดือน/ปีเกิด:")
        form_data['น้ำหนัก (กก.)'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง (ซม.)'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("ชื่อผู้ปกครอง:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, เบอร์โทร")

    # --- Section 2: Child's Information ---
    with st.expander("ส่วนที่ 2: ข้อมูลเด็ก", expanded=True):
        education_status = st.radio("1. การศึกษาของเด็ก:", ["ยังไม่ได้เข้าเรียน", "เข้าเรียน"])
        if education_status == "เข้าเรียน":
            education_level_option = st.radio(
                "ระดับชั้น:",
                ("ก่อนอนุบาล", "อนุบาล", "ประถม"), 
                key="education_level_radio"
            )

            education_detail = ""
            if education_level_option in ["อนุบาล", "ประถม"]:
                education_detail = st.text_input(f"ระบุ ({education_level_option})", key=f"{education_level_option}_detail")

            education_info = education_level_option
            if education_detail:
                education_info += f" ({education_detail})"

            st.write("เด็กเรียนอยู่ในโรงเรียนปัจจุบันเป็นระยะเวลา:")
            col1, col2 = st.columns(2)
            edu_years = col1.number_input("ปี", min_value=0, step=1, key="edu_years")
            edu_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="edu_months")
            form_data['การศึกษา'] = f"เข้าเรียน ระดับ {education_info} (ระยะเวลา {edu_years} ปี {edu_months} เดือน)"
        else:
            form_data['การศึกษา'] = "ยังไม่ได้เข้าเรียน"

        st.write("2. เด็กอาศัยอยู่ในที่อยู่ปัจจุบันมาประมาณ:")
        col1, col2 = st.columns(2)
        res_years = col1.number_input("ปี", min_value=0, step=1, key="res_years_child")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="res_months_child")
        form_data['ระยะเวลาอาศัย'] = f"{res_years} ปี {res_months} เดือน"

        comorbidity_status = st.radio("3. เด็กมีโรคประจำตัวหรือไม่:", ["ไม่มี", "มี"])
        if comorbidity_status == "มี":
            comorbidity_detail = st.text_input("ระบุโรคประจำตัว:", label_visibility="collapsed")
            form_data['โรคประจำตัว'] = f"มี ({comorbidity_detail})"
        else:
            form_data['โรคประจำตัว'] = "ไม่มี"

        medication_status = st.radio("4. เด็กรัปประทานยาประจำ:", ["ไม่ได้รับประทาน", "รับประทาน"])
        if medication_status == "รับประทาน":
            medication_detail = st.text_input("ระบุยาประจำ:", label_visibility="collapsed")
            form_data['ยาประจำ'] = f"รับประทาน ({medication_detail})"
        else:
            form_data['ยาประจำ'] = "ไม่ได้รับประทาน"

        form_data['จำนวนอาบน้ำ'] = st.number_input("5. เด็กอาบน้ำวันละกี่ครั้ง:", min_value=0, step=1)

        milk_status = st.radio("6. เด็กดื่มนมหรือไม่:", ["ไม่ดื่ม", "ดื่ม"])
        if milk_status == "ดื่ม":
            milk_type = st.radio("ประเภทนม:", ["นมแม่อย่างเดียว", "นมกระป๋อง/นมกล่อง", "ทั้งนมแม่และนมกระป๋อง/นมกล่อง"])
            form_data['การดื่มนม'] = f"ดื่ม ({milk_type})"
        else:
            form_data['การดื่มนม'] = "ไม่ดื่ม"

        visit_workplace = st.radio(
            "7. เด็กเคยไปบริเวณที่ทำงานเกี่ยวกับตะกั่วบ้างหรือไม่:",
            ("ไม่ไป", "ไป"), 
            key="visit_workplace"
        )
        form_data['เคยไปที่ทำงานเกี่ยวกับตะกั่ว'] = visit_workplace

        if visit_workplace == "ไป":
            form_data['ความถี่ในการไป'] = st.radio("8. เด็กไปที่บริเวณงานเกี่ยวกับตะกั่วบ่อยแค่ไหน:", ["นานๆ ไปครั้ง", "บ่อยมาก"])
            form_data['ระยะเวลาที่อยู่'] = st.radio("9. ระยะเวลาเฉลี่ยในแต่ละวันที่เด็กอยู่บริเวณงานเกี่ยวกับตะกั่ว:", ["น้อยกว่า 2 ชม.", "2 - 4 ชม.", "5 - 8 ชม.", "8 ชม. ขึ้นไป"])
        
        form_data['ประวัติรับสารตะกั่วอื่นๆ'] = st.text_area("10. ประวัติรับสารตะกั่วอื่นๆ:")

    # --- Section 3: Exam Results ---
    with st.expander("ส่วนที่ 3: ผลการตรวจต่างๆ ที่เกี่ยวข้อง", expanded=True):
        st.write("1. ตะกั่วในเลือด")
        col1, col2 = st.columns(2)
        blood_lead_result = col1.text_input("ผลการตรวจ (µg/dL)")
        blood_lead_date = col2.date_input("วันที่ตรวจ", key="blood_lead_date")
        form_data['ผลตรวจตะกั่วในเลือด'] = f"{blood_lead_result} (วันที่: {blood_lead_date})"

        st.write("2. พัฒนาการเด็ก")
        dev_check_status = st.radio("สถานะการตรวจ:", ["ไม่ได้ตรวจ", "ตรวจ"])
        
        if dev_check_status == "ไม่ได้ตรวจ":
            not_checked_reason = st.text_input("ระบุเหตุผลที่ไม่ได้ตรวจ:", key="dev_not_checked_reason")
            form_data['ผลตรวจพัฒนาการเด็ก'] = f"ไม่ได้ตรวจ (เหตุผล: {not_checked_reason})"
        else:
            dev_domains = st.multiselect(
                "ระบุด้านที่ตรวจ:",
                ["ด้านการเคลื่อนไหว (GM)", "ด้านการใช้กล้ามเนื้อมัดเล็กและสติปัญญา (FM)", 
                 "ด้านความเข้าใจภาษา (RL)", "ด้านการใช้ภาษา (EL)", "ด้านการช่วยเหลือตัวเองและสังคม (PS)"]
            )
            dev_check_date = st.date_input("วันที่ตรวจพัฒนาการ", key="dev_check_date")
            form_data['ผลตรวจพัฒนาการเด็ก'] = f"ตรวจ (ด้าน: {', '.join(dev_domains)}, วันที่: {dev_check_date})"

    # --- Section 4 & 5: Diagnosis & Recommendations ---
    with st.expander("ส่วนที่ 4 และ 5: การวินิจฉัยและข้อเสนอแนะ", expanded=True):
        form_data['การวินิจฉัยโรค'] = st.radio("ส่วนที่ 4: การวินิจฉัยโรค", ["สงสัยโรคจากตะกั่ว", "โรคจากตะกั่ว", "โรคอื่นๆ"])
        form_data['ข้อเสนอแนะ'] = st.text_area("ส่วนที่ 5: การรักษาพยาบาล หรือข้อเสนอแนะอื่นๆ")
        form_data['วันที่เก็บข้อมูล'] = st.date_input("วันที่เก็บข้อมูล:")

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        success = save_to_sheet(SHEET_NAME, form_data)
        if success:
            st.success("บันทึกข้อมูลเรียบร้อยแล้ว")
        else:
            st.error("การบันทึกข้อมูลล้มเหลว กรุณาตรวจสอบการตั้งค่าและลองอีกครั้ง")

