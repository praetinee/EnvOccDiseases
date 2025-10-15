# -*- coding: utf-8 -*-
import streamlit as st
import datetime
from utils.g_sheets_connector import save_to_sheet

def render():
    """Renders the Confined Space Investigation Form."""
    
    st.header("แบบสอบสวนผู้บาดเจ็บหรือเสียชีวิตด้วยโรคจากภาวะอับอากาศ")

    # Initialize session state for conditional UI elements
    if 'cs_comorbidity_status' not in st.session_state:
        st.session_state.cs_comorbidity_status = 'ไม่มี'
    if 'cs_symptom_status' not in st.session_state:
        st.session_state.cs_symptom_status = 'มี' # Default to 'มี' to show questions initially

    # --- Data Collection Dictionary ---
    form_data = {}

    with st.container(border=True):
        respondent_type_opt = st.radio(
            "ผู้ตอบแบบสอบถาม:",
            ["ผู้ร่วมอยู่ในเหตุการณ์ขณะเกิดเหตุ", "ทีมกู้ภัย/ทีมกู้ชีพ", "ญาติ/คนในครอบครัว", "อื่นๆ"],
            key="cs_respondent_type"
        )
        if respondent_type_opt == "อื่นๆ":
            respondent_type_other = st.text_input("ระบุอื่นๆ:", key="cs_respondent_other")
            form_data['ผู้ตอบแบบสอบถาม'] = respondent_type_other
        else:
            form_data['ผู้ตอบแบบสอบถาม'] = respondent_type_opt

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns([3, 1])
        form_data['ชื่อ-นามสกุล'] = col1.text_input("1.1 ชื่อ - นามสกุล:")
        form_data['อายุ'] = col2.number_input("อายุ (ปี):", min_value=0, step=1)

        col1, col2 = st.columns(2)
        form_data['เพศ'] = col1.radio("1.2 เพศ:", ["ชาย", "หญิง"], horizontal=True)
        
        nationality_opt = col2.radio("1.3 สัญชาติ:", ["ไทย", "กัมพูชา", "พม่า", "อื่นๆ"], horizontal=True)
        if nationality_opt == "อื่นๆ":
            nationality_other = col2.text_input("ระบุสัญชาติอื่นๆ:", key="cs_nationality_other")
            form_data['สัญชาติ'] = nationality_other
        else:
            form_data['สัญชาติ'] = nationality_opt

        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("1.4 ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่ที่, ถนน, ตรอก/ซอย, ตำบล, อำเภอ, จังหวัด, เบอร์โทร")

        occupation_opt = st.radio("1.5 อาชีพ:", ["รับจ้าง", "ค้าขาย", "แม่บ้าน", "เกษตร", "อื่นๆ"])
        
        if occupation_opt == "รับจ้าง":
            occupation_detail = st.text_input("ระบุ (รับจ้าง):", key="cs_occupation_detail")
            form_data['อาชีพ'] = f"รับจ้าง ({occupation_detail})"
        elif occupation_opt == "อื่นๆ":
            occupation_other = st.text_input("ระบุ (อื่นๆ):", key="cs_occupation_other")
            form_data['อาชีพ'] = f"อื่นๆ ({occupation_other})"
        else:
            form_data['อาชีพ'] = occupation_opt


        col1, col2 = st.columns(2)
        form_data['การดื่มแอลกอฮอล์'] = col1.radio("1.6 ปัจจุบันท่านดื่มเครื่องดื่มแอลกอฮอล์ หรือไม่:", ["ไม่ดื่ม", "ดื่มเป็นบางครั้ง", "ดื่มเป็นประจำ"])
        form_data['การสูบบุหรี่'] = col2.radio("1.7 ปัจจุบันท่านสูบบุหรี่/ยาเส้น หรือไม่:", ["ไม่สูบ", "สูบเป็นบางครั้ง", "สูบเป็นประจำ"])

    # --- Section 2: Medical History ---
    with st.expander("ส่วนที่ 2: ข้อมูลประวัติการเจ็บป่วย", expanded=True):
        st.radio(
            "2.1 ท่านมีโรคประจําตัว หรือไม่:",
            ["ไม่มี", "มี"],
            key='cs_comorbidity_status',
            horizontal=True
        )
        if st.session_state.cs_comorbidity_status == 'มี':
            comorbidities = st.multiselect(
                "ระบุโรคประจำตัว:",
                ["โรคหลอดลมอักเสบเรื้อรัง", "โรคหอบหืด", "โรคลมชัก", "โรคหัวใจ", "โรคความดันโลหิตสูง", "โรคภูมิแพ้"]
            )
            other_comorbidity = st.text_input("โรคประจำตัวอื่นๆ:")
            if other_comorbidity:
                comorbidities.append(other_comorbidity)
            form_data['โรคประจำตัว'] = ", ".join(comorbidities)
        else:
            form_data['โรคประจำตัว'] = "ไม่มี"

    # --- Section 3: Exposure History ---
    with st.expander("ส่วนที่ 3: ประวัติการสัมผัส", expanded=True):
        st.write("3.1 ขณะเกิดเหตุการณ์ ท่านอยู่จุดใด:")
        col1, col2 = st.columns(2)
        location = col1.text_input("ระบุตำแหน่ง:", key="cs_location")
        distance = col2.number_input("ระยะห่างจากที่เกิดเหตุ (เมตร):", min_value=0.0, format="%.2f", key="cs_distance")
        form_data['จุดที่อยู่ขณะเกิดเหตุ'] = f"ตำแหน่ง: {location}, ระยะห่าง: {distance} เมตร"

        
        smell_opt = st.radio("3.2 ท่านได้กลิ่น/ไอระเหยสารเคมี ในระหว่างอยู่ในสถานที่เกิดเหตุ หรือไม่:", ["ไม่เคย", "เคย"])
        if smell_opt == "เคย":
            smell_desc = st.text_input("อธิบายกลิ่น:")
            form_data['ได้กลิ่นสารเคมี'] = f"เคย ({smell_desc})"
        else:
            form_data['ได้กลิ่นสารเคมี'] = "ไม่เคย"

        smell_duration_opt = st.radio("3.3 ท่านได้กลิ่น/รับสัมผัสกลิ่นช่วงเวลาใด:", ["รู้สึกได้กลิ่นตลอดระยะเวลา", "รู้สึกได้กลิ่นเป็นช่วงๆ", "อื่นๆ"])
        if smell_duration_opt == "อื่นๆ":
            smell_duration_other = st.text_input("ระบุ (ช่วงเวลาได้กลิ่น):", key="cs_smell_duration_other")
            form_data['ลักษณะการได้กลิ่น'] = smell_duration_other
        else:
            form_data['ลักษณะการได้กลิ่น'] = smell_duration_opt
        
        st.radio("3.4 ท่านมีอาการผิดปกติระหว่าง หรือหลังจากได้กลิ่น หรือไม่:", ["มี", "ไม่มี (สิ้นสุดการสัมภาษณ์)"], key='cs_symptom_status', horizontal=True)
        
        if st.session_state.cs_symptom_status == 'มี':
            symptoms = st.multiselect(
                "ระบุอาการ:",
                ["ปวดศีรษะ", "มึนงง", "วิงเวียน", "หน้ามืด", "หายใจไม่ออก", "คลื่นไส้", "อาเจียน"]
            )
            form_data['อาการผิดปกติ'] = ", ".join(symptoms)
            
            action_opt = st.radio("3.5 เมื่อท่านมีอาการแล้ว ท่านปฏิบัติตัวอย่างไร:", ["ไม่ได้ทำอะไร", "ไปพบแพทย์", "อื่นๆ"])
            if action_opt != "ไม่ได้ทำอะไร":
                action_detail = st.text_input("ระบุสถานพยาบาล/การปฏิบัติ:")
                form_data['การปฏิบัติตัวหลังมีอาการ'] = f"{action_opt} ({action_detail})"
            else:
                form_data['การปฏิบัติตัวหลังมีอาการ'] = "ไม่ได้ทำอะไร"

    # --- Conditional Sections based on symptoms ---
    if st.session_state.cs_symptom_status == 'มี':
        # --- Section 4: Treatment Information ---
        with st.expander("ส่วนที่ 4: ข้อมูลการรักษา", expanded=True):
            st.write("4.1 ท่านเข้ารับการรักษาในโรงพยาบาล:")
            hospital_name = st.text_input("ชื่อโรงพยาบาล:", key="cs_hospital_name")
            
            col1, col2, col3, col4 = st.columns(4)
            treat_date = col1.date_input("วันที่เข้ารับการรักษา", datetime.date.today())
            treat_time = col2.time_input("เวลา", datetime.datetime.now().time())
            patient_type = col3.selectbox("ประเภทผู้ป่วย", ["เสียชีวิต", "ผู้ป่วยนอก", "ผู้ป่วยใน"])
            
            ipd_days = 0
            if patient_type == "ผู้ป่วยใน":
                ipd_days = col4.number_input("จำนวนวัน (ผู้ป่วยใน)", min_value=0, step=1)
            
            treatment_info = f"โรงพยาบาล: {hospital_name}, วันที่ {treat_date} เวลา {treat_time}, ประเภท: {patient_type}"
            if patient_type == "ผู้ป่วยใน":
                treatment_info += f", จำนวน {ipd_days} วัน"
            form_data['ข้อมูลการรักษา'] = treatment_info


        # --- Recorder Info ---
        with st.expander("ข้อมูลผู้บันทึก", expanded=True):
            col1, col2, col3 = st.columns(3)
            form_data['ผู้บันทึก'] = col1.text_input("ชื่อ - สกุล:")
            form_data['เบอร์โทรผู้บันทึก'] = col2.text_input("เบอร์โทรศัพท์:")
            form_data['หน่วยงานผู้บันทึก'] = col3.text_input("หน่วยงาน:")

        st.markdown("---")
        if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
            success = save_to_sheet("ConfinedSpace", form_data)
            if success:
                st.success("บันทึกข้อมูลเรียบร้อยแล้ว")
            else:
                st.error("การบันทึกข้อมูลล้มเหลว กรุณาตรวจสอบการตั้งค่าและลองอีกครั้ง")

