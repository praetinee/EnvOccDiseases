import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Adult History Form (PbC04)"""
    st.header("แบบซักประวัติพฤติกรรมที่เกี่ยวข้องกับการสัมผัสสารตะกั่วในผู้ใหญ่และหญิงตั้งครรภ์")
    st.caption("(แบบ PbC04)")

    form_data = {}

    # --- Section 1: General Information ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        st.subheader("ข้อมูลหน่วยบริการสาธารณสุข")
        col1, col2, col3 = st.columns(3)
        form_data['โรงพยาบาล'] = col1.text_input("โรงพยาบาล", key="pbc04_hosp_name")
        form_data['อำเภอ'] = col2.text_input("อำเภอ", key="pbc04_hosp_district")
        form_data['จังหวัด'] = col3.text_input("จังหวัด", key="pbc04_hosp_province")
        
        form_data['ขนาดโรงพยาบาล'] = st.radio(
            "ขนาดของโรงพยาบาล",
            ["รพศ. (A)", "รพท. (S)", "รพท. ขนาดเล็ก (M1)", "รพช. แม่ข่าย (M2)",
             "รพช. ขนาดใหญ่ (F1)", "รพช. ขนาดกลาง (F2)", "รพช. ขนาดเล็ก (F3)"],
            key="pbc04_hosp_size", horizontal=True)

        st.subheader("ข้อมูลผู้ป่วย")
        col1, col2 = st.columns(2)
        form_data['ชื่อ-สกุล'] = col1.text_input("ชื่อ - สกุล", key="pbc04_fullname")
        form_data['เพศ'] = col2.selectbox("เพศ", ["ชาย", "หญิง"], key="pbc04_gender")
        
        col1, col2 = st.columns(2)
        form_data['อายุ'] = col1.number_input("อายุ (ปี)", min_value=0, step=1, key="pbc04_age")
        form_data['น้ำหนัก'] = col2.number_input("น้ำหนัก (กก.)", min_value=0.0, format="%.2f", key="pbc04_weight")
        
        col1, col2 = st.columns(2)
        form_data['ส่วนสูง'] = col1.number_input("ส่วนสูง (ซม.)", min_value=0.0, format="%.2f", key="pbc04_height")
        form_data['อาชีพปัจจุบัน'] = col2.text_input("อาชีพปัจจุบัน", key="pbc04_job_current")
        
        form_data['ลักษณะงาน'] = st.text_input("ลักษณะงาน/ตำแหน่งงาน/แผนกที่ทำงานปัจจุบัน", key="pbc04_job_desc")

        st.write("ระยะเวลาที่ทำงานต่อวัน:")
        c1, c2 = st.columns(2)
        work_hours = c1.number_input("ชั่วโมง/วัน", min_value=0, step=1, key="pbc04_work_hours")
        work_days = c2.number_input("และกี่วันต่อสัปดาห์ (วัน/สัปดาห์)", min_value=0, step=1, key="pbc04_work_days")
        form_data['ระยะเวลาทำงาน'] = f"{work_hours} ชม./วัน, {work_days} วัน/สัปดาห์"

        col1, col2 = st.columns([3,1])
        job_prev = col1.text_input("อาชีพเดิมก่อนมาทำงานปัจจุบัน คือ", key="pbc04_job_prev")
        job_prev_duration = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="pbc04_job_prev_duration", label_visibility="collapsed")
        form_data['อาชีพเดิม'] = f"{job_prev} (ระยะเวลา: {job_prev_duration} ปี)"


        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด", key="pbc04_address")
        form_data['ระยะเวลาอาศัย'] = st.text_input("ระยะเวลาที่อาศัยในพื้นที่ (ปี/เดือน)", key="pbc04_residence_duration")
        
        col1, col2 = st.columns(2)
        form_data['สถานภาพสมรส'] = col1.selectbox("สถานภาพสมรส", ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"], key="pbc04_marital")
        form_data['ระดับการศึกษา'] = col2.selectbox("ระดับการศึกษาสูงสุด", ["ไม่ได้ศึกษา", "ประถมศึกษา", "มัธยมศึกษา/ปวช.", "อนุปริญญา/ปวส.", "ปริญญาตรี", "สูงกว่าปริญญาตรี"], key="pbc04_education")

        st.subheader("กรณีเป็นหญิงตั้งครรภ์ (สอบถามเพิ่มเติม)")
        col1, col2 = st.columns(2)
        form_data['อายุครรภ์ (สัปดาห์)'] = col1.number_input("อายุครรภ์ (สัปดาห์)", min_value=0, step=1, key="pbc04_preg_weeks")
        form_data['ท้องคนที่'] = col2.number_input("ท้องคนที่", min_value=1, step=1, key="pbc04_preg_count")
        form_data['ฝากครรภ์'] = col1.text_input("ฝากครรภ์หรือไม่", key="pbc04_preg_anc")
        form_data['ประวัติการแท้ง (ครั้ง)'] = col2.number_input("ประวัติการแท้ง (ครั้ง)", min_value=0, step=1, key="pbc04_preg_miscarriage")
        form_data['บุตรน้ำหนักต่ำกว่าเกณฑ์ (คน)'] = st.number_input("บุตรน้ำหนักต่ำกว่าเกณฑ์ (คน)", min_value=0, step=1, key="pbc04_preg_low_birth_weight")

    # --- Section 2: Health Behavior ---
    with st.expander("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ", expanded=True):
        smoking_hist = st.radio("ประวัติการสูบบุหรี่:", ["ไม่สูบ", "เคยสูบแต่เลิกแล้ว", "สูบ/ปัจจุบันยังสูบ"])
        if smoking_hist == "เคยสูบแต่เลิกแล้ว":
            quit_years = st.number_input("เลิกมาแล้วกี่ปี:", min_value=0, step=1)
            form_data['ประวัติสูบบุหรี่'] = f"เคยสูบ (เลิกมาแล้ว {quit_years} ปี)"
        elif smoking_hist == "สูบ/ปัจจุบันยังสูบ":
            current_amount = st.number_input("วันละกี่มวน:", min_value=0, step=1)
            form_data['ประวัติสูบบุหรี่'] = f"ปัจจุบันยังสูบ ({current_amount} มวน/วัน)"
        else:
            form_data['ประวัติสูบบุหรี่'] = "ไม่สูบ"
        
        smoke_locs = st.multiselect("สถานที่หรือบริเวณที่ท่านสูบบุหรี่:", ["ไม่สูบ", "บริเวณสถานที่ทำงาน/สูบพร้อมขณะทำงาน", "บริเวณที่จัดไว้เป็นสถานที่สูบบุหรี่", "บริเวณรับประทานอาหาร/โรงอาหาร"])
        smoke_loc_other = st.text_input("สถานที่สูบบุหรี่อื่นๆ:")
        if smoke_loc_other: smoke_locs.append(smoke_loc_other)
        form_data['สถานที่สูบบุหรี่'] = ", ".join(smoke_locs)

        food_sources = st.multiselect("แหล่งที่มาของอาหาร (ตอบได้มากกว่า 1 ข้อ):", ["ปรุง/ทำอาหารเอง", "ซื้อจากผู้ประกอบการเป็นหลัก"])
        food_source_other = st.text_input("แหล่งอาหารอื่นๆ:")
        if food_source_other: food_sources.append(food_source_other)
        form_data['แหล่งที่มาอาหาร'] = ", ".join(food_sources)

        water_use = st.multiselect("แหล่งน้ำใช้:", ["น้ำประปา", "น้ำบาดาล", "แหล่งน้ำธรรมชาติ"])
        water_use_other = st.text_input("แหล่งน้ำใช้อื่นๆ (ระบุพิกัดถ้ามี):")
        if water_use_other: water_use.append(water_use_other)
        form_data['แหล่งน้ำใช้'] = ", ".join(water_use)

        water_drink = st.multiselect("แหล่งน้ำดื่ม:", ["น้ำประปา", "น้ำบาดาล", "น้ำซื้อ"])
        water_drink_other = st.text_input("แหล่งน้ำดื่มอื่นๆ:")
        if water_drink_other: water_drink.append(water_drink_other)
        form_data['แหล่งน้ำดื่ม'] = ", ".join(water_drink)
        
        diseases = st.multiselect("ประวัติโรคประจำตัว:", ["ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง"])
        disease_other = st.checkbox("อื่นๆ")
        form_data['โรคประจำตัว'] = ", ".join(diseases) if not disease_other else ", ".join(diseases) + ", อื่นๆ"

        other_history = st.multiselect("ประวัติอื่นๆ:", ["การใช้แป้งทาหน้างิ้ว", "ประวัติการรับกระสุนปืน"])
        herbal_med = st.text_input("ใช้ยาสมุนไพร (ระบุ):")
        if herbal_med: other_history.append(f"ใช้ยาสมุนไพร ({herbal_med})")
        form_data['ประวัติอื่นๆ'] = ", ".join(other_history)
        
    # --- Section 3: Exam Results ---
    with st.expander("ส่วนที่ 3: ผลการตรวจต่างๆ ที่เกี่ยวข้อง", expanded=True):
        st.subheader("การตรวจร่างกายตามระบบโดยแพทย์")
        # ... (Physical exam section can be added here, similar to lead_occupational_medical.py) ...
        st.info("ส่วนการตรวจร่างกายโดยแพทย์จะถูกเพิ่มในภายหลัง")

        st.subheader("ข้อมูลผลการตรวจทางห้องปฏิบัติการ")
        # ... (Lab results section can be added here, similar to lead_occupational_medical.py) ...
        st.info("ส่วนผลการตรวจทางห้องปฏิบัติการจะถูกเพิ่มในภายหลัง")

    # --- Section 4 & 5: Diagnosis & Recommendations ---
    with st.expander("ส่วนที่ 4 และ 5: การวินิจฉัยและข้อเสนอแนะ", expanded=True):
        form_data['การวินิจฉัย'] = st.multiselect("ส่วนที่ 4: การวินิจฉัยโรค", ["สงสัยโรคจากตะกั่ว", "โรคจากตะกั่ว", "โรคอื่นๆ"])
        form_data['ข้อเสนอแนะ'] = st.text_area("ส่วนที่ 5: การรักษาพยาบาล หรือข้อเสนอแนะอื่นๆ")
        
        st.subheader("ข้อมูลแพทย์ผู้ตรวจ")
        col1, col2 = st.columns(2)
        form_data['แพทย์ผู้ตรวจ'] = col1.text_input("ชื่อ - สกุล แพทย์ผู้ตรวจร่างกาย", key="pbc04_doc_name")
        form_data['เบอร์โทรแพทย์'] = col2.text_input("เบอร์โทร", key="pbc04_doc_phone")
        form_data['Line ID แพทย์'] = col1.text_input("ID Line", key="pbc04_doc_line")
        form_data['วันที่ตรวจ'] = col2.date_input("วัน/เดือน/ปี", datetime.date.today(), key="pbc04_doc_date")

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)
