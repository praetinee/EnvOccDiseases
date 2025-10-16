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
        job_prev_duration = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="pbc04_job_prev_duration")
        form_data['อาชีพเดิม'] = f"{job_prev} (ระยะเวลา: {job_prev_duration} ปี)"


        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด", key="pbc04_address")
        form_data['ระยะเวลาอาศัย'] = st.text_input("ระยะเวลาที่อาศัยในพื้นที่ (ปี/เดือน)", key="pbc04_residence_duration")
        
        col1, col2 = st.columns(2)
        marital_status = col1.selectbox("สถานภาพสมรส", ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"], key="pbc04_marital")
        if marital_status == "อื่นๆ":
            other_marital_status = col1.text_input("ระบุ:", key="pbc04_marital_other", label_visibility="collapsed")
            form_data['สถานภาพสมรส'] = other_marital_status
        else:
            form_data['สถานภาพสมรส'] = marital_status
            
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

        water_use_selection = st.multiselect("แหล่งน้ำใช้:", ["น้ำประปา", "น้ำบาดาล", "แหล่งน้ำธรรมชาติ", "อื่นๆ"])
        
        processed_water_use = list(water_use_selection)
        
        if "แหล่งน้ำธรรมชาติ" in processed_water_use:
            coords = st.text_input("ระบุพิกัดของแหล่งน้ำธรรมชาติ:")
            if coords:
                try:
                    idx = processed_water_use.index("แหล่งน้ำธรรมชาติ")
                    processed_water_use[idx] = f"แหล่งน้ำธรรมชาติ (พิกัด: {coords})"
                except ValueError:
                    pass
        
        if "อื่นๆ" in processed_water_use:
            other_text = st.text_input("ระบุแหล่งน้ำใช้อื่นๆ:")
            try:
                idx = processed_water_use.index("อื่นๆ")
                if other_text:
                    processed_water_use[idx] = f"อื่นๆ ({other_text})"
                else:
                    processed_water_use.pop(idx)
            except ValueError:
                pass

        form_data['แหล่งน้ำใช้'] = ", ".join(processed_water_use)

        water_drink = st.multiselect("แหล่งน้ำดื่ม:", ["น้ำประปา", "น้ำบาดาล", "น้ำซื้อ"])
        water_drink_other = st.text_input("แหล่งน้ำดื่มอื่นๆ:")
        if water_drink_other: water_drink.append(water_drink_other)
        form_data['แหล่งน้ำดื่ม'] = ", ".join(water_drink)
        
        diseases = st.multiselect("ประวัติโรคประจำตัว:", ["ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง"])
        disease_other_check = st.checkbox("อื่นๆ")
        
        other_disease_input = ""
        if disease_other_check:
            other_disease_input = st.text_input("ระบุ:", key="disease_other_input")

        final_disease_list = diseases
        if other_disease_input:
            final_disease_list.append(other_disease_input)

        form_data['โรคประจำตัว'] = ", ".join(final_disease_list)

        other_history = st.multiselect("ประวัติอื่นๆ:", ["การใช้แป้งทาหน้างิ้ว", "ประวัติการรับกระสุนปืน"])
        herbal_med = st.text_input("ใช้ยาสมุนไพร (ระบุ):")
        if herbal_med: other_history.append(f"ใช้ยาสมุนไพร ({herbal_med})")
        form_data['ประวัติอื่นๆ'] = ", ".join(other_history)
        
    # --- Section 3: Exam Results ---
    with st.expander("ส่วนที่ 3: ผลการตรวจต่างๆ ที่เกี่ยวข้อง", expanded=True):
        st.subheader("การตรวจร่างกายตามระบบโดยแพทย์")
        physical_exam_data = {}
        
        col1, col2, col3, col4 = st.columns(4)
        physical_exam_data['BP'] = col1.text_input("BP (mmHg):")
        physical_exam_data['PR'] = col2.number_input("PR (/min):", min_value=0, step=1)
        physical_exam_data['RR'] = col3.number_input("RR (/min):", min_value=0, step=1)
        physical_exam_data['BT'] = col4.number_input("BT (°C):", min_value=0.0, format="%.1f")

        exam_items_before_neuro = [
            ("1) General appearance", "exam_general"),
            ("2) HEENT: conjunctivae", "exam_heent"),
            ("3) Lung", "exam_lung"),
            ("4) Abdomen", "exam_abdomen"),
            ("5) Skin", "exam_skin"),
            ("6) Hand writing", "exam_handwriting"),
        ]
        
        exam_items_after_neuro = [
            ("8) Gait", "exam_gait"),
            ("9) Sensation", "exam_sensation"),
            ("10) Cognition", "exam_cognition"),
            ("11) Mood", "exam_mood"),
            ("12) IQ หรือ Mentality", "exam_iq")
        ]

        def create_exam_row(label, key):
            col1, col2 = st.columns([1,2])
            with col1:
                st.write(label)
            with col2:
                status = st.radio(label, ["Normal", "Abnormal"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "Abnormal":
                    detail = st.text_input("ระบุความผิดปกติ", key=f"{key}_detail", label_visibility="collapsed")
                physical_exam_data[label] = f"{status}{f' ({detail})' if detail else ''}"

        for label, key in exam_items_before_neuro:
            create_exam_row(label, key)
        
        st.divider()
        st.write("7) Neuro sign: motor power grade")
        
        def create_motor_power_row(label, key_prefix):
            st.markdown(f"**{label}**")
            
            h_spacer, h_r, h_l = st.columns([2, 2, 2])
            with h_r:
                st.markdown("<p style='text-align: center;'><b>R</b></p>", unsafe_allow_html=True)
            with h_l:
                st.markdown("<p style='text-align: center;'><b>L</b></p>", unsafe_allow_html=True)
        
            # Proximal
            cols1 = st.columns([1, 1, 2, 2])
            with cols1[0]:
                st.markdown("**Proximal:**")
            with cols1[1]:
                st.markdown("Flexor")
            with cols1[2]:
                r_input_col, r_text_col = st.columns([4, 1])
                with r_input_col:
                    physical_exam_data[f'{key_prefix}_prox_flex_R'] = st.text_input(f"{key_prefix}_prox_flex_R", key=f"pbc04_{key_prefix}_prox_flex_R", label_visibility="collapsed")
                with r_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
            with cols1[3]:
                l_input_col, l_text_col = st.columns([4, 1])
                with l_input_col:
                    physical_exam_data[f'{key_prefix}_prox_flex_L'] = st.text_input(f"{key_prefix}_prox_flex_L", key=f"pbc04_{key_prefix}_prox_flex_L", label_visibility="collapsed")
                with l_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
        
            cols2 = st.columns([1, 1, 2, 2])
            with cols2[1]:
                st.markdown("extensor")
            with cols2[2]:
                r_input_col, r_text_col = st.columns([4, 1])
                with r_input_col:
                    physical_exam_data[f'{key_prefix}_prox_ext_R'] = st.text_input(f"{key_prefix}_prox_ext_R", key=f"pbc04_{key_prefix}_prox_ext_R", label_visibility="collapsed")
                with r_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
            with cols2[3]:
                l_input_col, l_text_col = st.columns([4, 1])
                with l_input_col:
                    physical_exam_data[f'{key_prefix}_prox_ext_L'] = st.text_input(f"{key_prefix}_prox_ext_L", key=f"pbc04_{key_prefix}_prox_ext_L", label_visibility="collapsed")
                with l_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
                
            # Distal
            cols3 = st.columns([1, 1, 2, 2])
            with cols3[0]:
                st.markdown("**Distal:**")
            with cols3[1]:
                st.markdown("Flexor")
            with cols3[2]:
                r_input_col, r_text_col = st.columns([4, 1])
                with r_input_col:
                    physical_exam_data[f'{key_prefix}_dist_flex_R'] = st.text_input(f"{key_prefix}_dist_flex_R", key=f"pbc04_{key_prefix}_dist_flex_R", label_visibility="collapsed")
                with r_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
            with cols3[3]:
                l_input_col, l_text_col = st.columns([4, 1])
                with l_input_col:
                    physical_exam_data[f'{key_prefix}_dist_flex_L'] = st.text_input(f"{key_prefix}_dist_flex_L", key=f"pbc04_{key_prefix}_dist_flex_L", label_visibility="collapsed")
                with l_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
                
            cols4 = st.columns([1, 1, 2, 2])
            with cols4[1]:
                st.markdown("extensor")
            with cols4[2]:
                r_input_col, r_text_col = st.columns([4, 1])
                with r_input_col:
                    physical_exam_data[f'{key_prefix}_dist_ext_R'] = st.text_input(f"{key_prefix}_dist_ext_R", key=f"pbc04_{key_prefix}_dist_ext_R", label_visibility="collapsed")
                with r_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
            with cols4[3]:
                l_input_col, l_text_col = st.columns([4, 1])
                with l_input_col:
                    physical_exam_data[f'{key_prefix}_dist_ext_L'] = st.text_input(f"{key_prefix}_dist_ext_L", key=f"pbc04_{key_prefix}_dist_ext_L", label_visibility="collapsed")
                with l_text_col:
                    st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
            st.divider()

        create_motor_power_row("(1) Upper extremities", "upper")
        create_motor_power_row("(2) Lower extremities", "lower")

        for label, key in exam_items_after_neuro:
            create_exam_row(label, key)

        form_data['การตรวจร่างกาย'] = physical_exam_data

        st.subheader("ข้อมูลผลการตรวจทางห้องปฏิบัติการ")
        lab_results_data = {}

        st.markdown("###### การตรวจสารบ่งชี้ทางชีวภาพ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("ระดับตะกั่วในเลือด")
        with col2:
            lab_results_data['ระดับตะกั่วในเลือด'] = st.number_input("µg/dL", min_value=0.0, format="%.2f", key="lab_lead_level", label_visibility="collapsed")
        with col3:
            lab_results_data['วันที่ตรวจ_ระดับตะกั่ว'] = st.date_input("วันที่ตรวจ (ตะกั่ว)", key="lab_lead_date", label_visibility="collapsed")

        st.markdown("###### การตรวจทางห้องปฏิบัติการอื่นๆ")
        
        # Header
        h_col1, h_col2, h_col3 = st.columns([1,2,1])
        h_col1.markdown("**รายการตรวจ**")
        h_col2.markdown("**ผลการตรวจ**")
        h_col3.markdown("**วันที่ตรวจ**")

        other_lab_tests = ["CBC", "BUN/Cr", "SGPT/SGOT", "TB/DB", "Uric acid", "UA"]
        for test in other_lab_tests:
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                st.write(test)
            with col2:
                status = st.radio(test, ["ปกติ", "ผิดปกติ"], key=f"lab_{test}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "ผิดปกติ":
                    detail = st.text_input("ระบุ:", key=f"lab_{test}_detail", label_visibility="collapsed")
                lab_results_data[test] = f"{status}{f' ({detail})' if detail else ''}"
            with col3:
                lab_results_data[f'วันที่ตรวจ_{test}'] = st.date_input(f"วันที่ตรวจ_{test}", key=f"lab_{test}_date", label_visibility="collapsed")
        
        form_data['ผลทางห้องปฏิบัติการ'] = lab_results_data


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
