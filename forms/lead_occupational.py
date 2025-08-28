import streamlit as st
import datetime
import pandas as pd

def render():
    """Renders the Lead Occupational Investigation Form using Streamlit widgets."""
    
    st.header("แบบสอบสวนโรคจากตะกั่วหรือสารประกอบของตะกั่ว")
    st.caption("สำหรับกลุ่มงานอาชีวเวชกรรม (อ้างอิงเอกสารแนบที่ 1 หน้า 30-33)")

    # --- Data Collection Dictionary ---
    form_data = {}

    with st.container(border=True):
        col1, col2 = st.columns(2)
        form_data['วันที่สอบสวน'] = col1.date_input("วัน/เดือน/ปี ที่ดำเนินการสอบสวน:", datetime.date.today())
        form_data['ชื่อสถานประกอบการ'] = col1.text_input("ชื่อโรงงาน/สถานประกอบการ/สถานที่เกิดเหตุ:")
        form_data['ประเภทกิจการ'] = col2.text_input("ประเภทสถานประกอบกิจการ:")

    # --- Section 1: Personal Information ---
    with st.expander("ส่วนที่ 1: ข้อมูลส่วนบุคคล", expanded=True):
        form_data['ชื่อ-นามสกุล'] = st.text_input("1.1 ชื่อ - นามสกุล:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("1.2 ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด")
        
        st.write("1.3 อาศัยอยู่ในพื้นที่มาแล้ว:")
        col1, col2 = st.columns(2)
        res_years = col1.number_input("ปี", min_value=0, step=1, key="res_years")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="res_months")
        form_data['อาศัยอยู่ในพื้นที่มาแล้ว'] = f"{res_years} ปี {res_months} เดือน"

        col1, col2 = st.columns(2)
        form_data['อายุ'] = col1.number_input("1.4 อายุ (ปี):", min_value=0, step=1)
        form_data['เพศ'] = col2.radio("1.5 เพศ:", ["ชาย", "หญิง"], horizontal=True)

        col1, col2 = st.columns(2)
        marital_status_option = col1.radio("1.6 สถานภาพสมรส:", 
                     ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"])
        marital_status_other = col1.text_input("อื่นๆ (โปรดระบุ):", key="marital_other", label_visibility="collapsed")
        form_data['สถานภาพสมรส'] = marital_status_other if marital_status_option == "อื่นๆ" else marital_status_option
        
        form_data['ระดับการศึกษาสูงสุด'] = col2.selectbox("1.7 ระดับการศึกษาสูงสุด:",
                         ["-- เลือก --", "ไม่ได้ศึกษา", "ประถมศึกษา", "มัธยมศึกษา/ปวช.", 
                          "อนุปริญญา/ปวส.", "ปริญญาตรี", "สูงกว่าปริญญาตรี"])

        st.write("1.8 จํานวนสมาชิกในครอบครัว:")
        col1, col2 = st.columns(2)
        fam_total = col1.number_input("รวมทั้งหมด (คน)", min_value=0, step=1)
        fam_children = col2.number_input("เด็กอายุ < 7 ปี (คน)", min_value=0, step=1)
        form_data['จำนวนสมาชิกในครอบครัว'] = f"รวม: {fam_total} คน, เด็ก < 7 ปี: {fam_children} คน"

    # --- Section 2: Health and Behavior ---
    with st.expander("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ", expanded=True):
        smoking_hist = st.radio("2.1 ประวัติการสูบบุหรี่:",
                 ["ไม่สูบ", "เคยสูบแต่เลิกแล้ว", "ปัจจุบันยังสูบ"])
        col1, col2 = st.columns([1,2])
        quit_years = col1.number_input("เลิกมาแล้ว (ปี)", min_value=0, step=1, key="smoke_quit")
        current_amount = col2.number_input("ปัจจุบันยังสูบ (มวน/วัน)", min_value=0, step=1, key="smoke_current")
        if smoking_hist == "เคยสูบแต่เลิกแล้ว":
            form_data['ประวัติการสูบบุหรี่'] = f"เคยสูบแต่เลิกแล้ว ({quit_years} ปี)"
        elif smoking_hist == "ปัจจุบันยังสูบ":
            form_data['ประวัติการสูบบุหรี่'] = f"ปัจจุบันยังสูบ ({current_amount} มวน/วัน)"
        else:
            form_data['ประวัติการสูบบุหรี่'] = smoking_hist
        
        smoking_place_opt = st.radio("2.2 สถานที่หรือบริเวณที่ท่านสูบบุหรี่:",
                       ["ไม่สูบ", "บริเวณสถานที่ทำงาน/สูบพร้อมขณะทำงาน", "บริเวณที่จัดไว้", 
                        "บริเวณรับประทานอาหาร/โรงอาหาร", "อื่นๆ"])
        smoking_place_other = st.text_input("อื่นๆ (โปรดระบุ):", key="smoke_place_other", label_visibility="collapsed")
        form_data['สถานที่สูบบุหรี่'] = smoking_place_other if smoking_place_opt == "อื่นๆ" else smoking_place_opt

        eating_place_opt = st.radio("2.3 ท่านรับประทานอาหารในสถานที่ทํางานหรือไม่:",
                 ["ไม่ได้รับประทาน", "รับประทานในบริเวณเดียวกับที่ปฏิบัติงาน", "รับประทานในโรงอาหาร", "อื่นๆ"])
        eating_place_other = st.text_input("อื่นๆ (โปรดระบุ):", key="eat_place_other", label_visibility="collapsed")
        form_data['การรับประทานอาหารในที่ทำงาน'] = eating_place_other if eating_place_opt == "อื่นๆ" else eating_place_opt

        food_source_opts = st.multiselect("2.4 แหล่งที่มาของอาหาร (ตอบได้มากกว่า 1 ข้อ):",
                       ["ปรุง/ทำอาหารเอง", "ซื้อจากผู้ประกอบการเป็นหลัก"])
        food_source_other = st.text_input("อื่นๆ (โปรดระบุ):", key="food_src_other")
        if food_source_other: food_source_opts.append(food_source_other)
        form_data['แหล่งที่มาของอาหาร'] = ", ".join(food_source_opts)

        water_source_opt = st.radio("2.5 แหล่งน้ำดื่ม:",
                 ["น้ำประปา", "น้ำซื้อ", "นายจ้างจัดให้", "อื่นๆ"])
        water_source_other = st.text_input("อื่นๆ (โปรดระบุ):", key="water_src_other", label_visibility="collapsed")
        form_data['แหล่งน้ำดื่ม'] = water_source_other if water_source_opt == "อื่นๆ" else water_source_opt

        disease_opts = st.multiselect("2.6 ประวัติโรคประจําตัว:",
                       ["ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง"])
        disease_other = st.text_input("อื่นๆ (โปรดระบุ):", key="disease_other")
        if disease_other: disease_opts.append(disease_other)
        form_data['ประวัติโรคประจำตัว'] = ", ".join(disease_opts) if disease_opts else "ไม่มี"

    # --- Section 3: Work Info ---
    with st.expander("ส่วนที่ 3: ลักษณะงานและการประกอบอาชีพ", expanded=True):
        st.write("3.1 อาชีพปัจจุบัน:")
        col1, col2 = st.columns([2,1])
        job_current = col1.text_input("ระบุอาชีพ", key="job_current_name", label_visibility="collapsed")
        job_current_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_current_years")
        form_data['อาชีพปัจจุบัน'] = f"{job_current} ({job_current_years} ปี)"
        
        form_data['ลักษณะงานปัจจุบัน'] = st.text_input("3.2 ลักษณะงาน/ตำแหน่งงาน/แผนกที่ทํางานปัจจุบัน:")
        
        st.write("3.3 ระยะเวลาที่ทํางาน:")
        col1, col2 = st.columns(2)
        work_hours = col1.number_input("ชั่วโมง/วัน", min_value=0, step=1, key="work_hours")
        work_days = col2.number_input("วัน/สัปดาห์", min_value=0, step=1, key="work_days")
        form_data['ระยะเวลาทำงาน'] = f"{work_hours} ชม./วัน, {work_days} วัน/สัปดาห์"

        st.write("3.4 อาชีพเดิมก่อนมาทํางานปัจจุบัน:")
        col1, col2 = st.columns([2,1])
        job_previous = col1.text_input("ระบุอาชีพเดิม", key="job_prev_name", label_visibility="collapsed")
        job_previous_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_prev_years")
        form_data['อาชีพเดิม'] = f"{job_previous} ({job_previous_years} ปี)"

    # --- Section 4: Risk Factors ---
    with st.expander("ส่วนที่ 4: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่ว", expanded=True):
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุง/หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน", "ซ่อมเรือประมง", "ซ่อมเครื่องใช้ไฟฟ้า",
            "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ/เครื่องปั้นดินเผา", "งานโรงพิมพ์/หล่อตัวพิมพ์",
            "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]
        
        risk_jobs_household = st.multiselect("4.1 ปัจจุบันท่านหรือสมาชิกในบ้านมีผู้ใดประกอบอาชีพต่อไปนี้หรือไม่ (ตอบได้มากกว่า 1 ข้อ):", risk_jobs_list)
        risk_jobs_household_other = st.text_input("อื่นๆ (โปรดระบุ):", key="risk_job_other")
        if risk_jobs_household_other: risk_jobs_household.append(risk_jobs_household_other)
        form_data['อาชีพเสี่ยงในครัวเรือน'] = ", ".join(risk_jobs_household)

        risk_places_nearby = st.multiselect("4.2 โรงงาน/สถานประกอบการ/ร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย):", risk_jobs_list, key="risk_places")
        risk_places_nearby_other = st.text_input("อื่นๆ (โปรดระบุ):", key="risk_place_other")
        if risk_places_nearby_other: risk_places_nearby.append(risk_places_nearby_other)
        form_data['สถานประกอบการเสี่ยงใกล้ที่พัก'] = ", ".join(risk_places_nearby)

        st.write("4.3 ท่านใช้อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลใดระหว่างการทํางาน:")
        ppe_items = ["ถุงมือยาง/หนัง", "หมวก/ผ้าคลุมผม", "หน้ากากป้องกันฝุ่น/ผ้าปิดจมูก", "แว่นตา", "รองเท้าบูธ/ผ้าใบ", "เสื้อแขนยาว", "กางเกงขายาว"]
        ppe_options = ["ไม่ใช้", "ใช้บางครั้ง", "ใช้ทุกครั้ง"]
        for i, item in enumerate(ppe_items):
            form_data[f'PPE: {item}'] = st.radio(f"{i+1}. {item}", ppe_options, horizontal=True, key=f"ppe_{i}")
        
        col1, col2 = st.columns([1,2])
        ppe_other_name = col1.text_input("8. อื่นๆ ระบุ", key="ppe_other_name")
        if ppe_other_name:
            form_data[f'PPE: {ppe_other_name}'] = col2.radio(" ", ppe_options, horizontal=True, key="ppe_other_opt", label_visibility="collapsed")

        ppe_source = st.multiselect("4.4 อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลที่ท่านใช้ ได้มาอย่างไร:", ["ซื้อเอง", "ได้รับจากโรงงาน/บริษัท"])
        ppe_source_other = st.text_input("แหล่งอื่นๆ (โปรดระบุ):", key="ppe_src_other")
        if ppe_source_other: ppe_source.append(ppe_source_other)
        form_data['แหล่งที่มาของอุปกรณ์คุ้มครอง'] = ", ".join(ppe_source)

        col1, col2 = st.columns(2)
        form_data['ที่เก็บอุปกรณ์'] = col1.radio("4.5 ท่านเก็บอุปกรณ์ฯ ไว้ที่ใด:", ["บ้าน", "ที่ทำงาน"])
        
        ppe_care_opt = col2.radio("4.6 ท่านจัดเก็บรักษาอุปกรณ์ฯ หลังใช้งานอย่างไร:", ["ตามพื้น/ผนังห้องภายในบ้าน", "ล็อกเกอร์หรือตู้เก็บเฉพาะ", "อื่นๆ"])
        ppe_care_other = col2.text_input("อื่นๆ (โปรดระบุ):", key="ppe_care_other", label_visibility="collapsed")
        form_data['วิธีเก็บรักษาอุปกรณ์'] = ppe_care_other if ppe_care_opt == "อื่นๆ" else ppe_care_opt

        st.write("4.7 พฤติกรรมด้านสุขลักษณะและความปลอดภัยในการทํางาน:")
        hygiene_items = ["ล้างมือก่อนรับประทานอาหาร", "อาบน้ำก่อนออกจากสถานที่ทำงาน", "เปลี่ยนเสื้อผ้าก่อนออกจากสถานที่ปฏิบัติงาน", "เปลี่ยนรองเท้าก่อนออกจากสถานที่ทำงาน", "นำหรือสวมเสื้อผ้าที่ปนเปื้อนกลับบ้าน"]
        hygiene_options = ["ไม่ได้ปฏิบัติ/ไม่ใช่", "บางครั้ง", "ทุกครั้ง/ประจํา"]
        for i, item in enumerate(hygiene_items):
            form_data[f'สุขลักษณะ: {item}'] = st.radio(f"{i+1}. {item}", hygiene_options, horizontal=True, key=f"hygiene_{i}")

    # --- Section 5: Symptoms ---
    with st.expander("ส่วนที่ 5: ลักษณะอาการที่ส่งผลกระทบทางสุขภาพ (3 สัปดาห์ที่ผ่านมา)", expanded=True):
        symptoms = [
            "อ่อนเพลีย", "เบื่ออาหาร", "คลื่นไส้ อาเจียน", "ท้องผูก", "ปวดท้องรุนแรงเป็นพัก ๆ",
            "ปวดตามข้อ กล้ามเนื้อ", "อาการปวดเมื่อยตามร่างกาย", "ปวดศีรษะ", "ซีด", "ซึม", "ชัก",
            "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย", "น้ำหนักลดโดยไม่ทราบสาเหตุ", "มือสั่น",
            "มือ เท้า อ่อนแรง", "ผื่น"
        ]
        symptom_options = ["ไม่มี", "นาน ๆ ครั้ง", "เป็นประจําหรือแทบทุกวัน"]
        for symptom in symptoms:
            form_data[f'อาการ: {symptom}'] = st.radio(symptom, symptom_options, key=f"occ_symptom_{symptom.replace(' ', '_')}", horizontal=True)

    # --- NEW SECTION: Medical Examination ---
    with st.expander("🩺 ส่วนที่ 6: แบบบันทึกการตรวจร่างกายโดยแพทย์", expanded=True):
        st.subheader("Vitals")
        col1, col2, col3, col4 = st.columns(4)
        form_data['BP (mmHg)'] = col1.text_input("BP (mmHg):")
        form_data['PR (/min)'] = col2.number_input("PR (/min):", min_value=0, step=1)
        form_data['RR (/min)'] = col3.number_input("RR (/min):", min_value=0, step=1)
        form_data['BT (°C)'] = col4.number_input("BT (°C):", min_value=0.0, format="%.1f")

        st.subheader("การตรวจร่างกาย")
        exam_items = {
            "General appearance": "exam_general", "HEENT: conjunctive": "exam_heent", "Lung": "exam_lung",
            "Abdomen": "exam_abdomen", "Skin": "exam_skin", "Hand writing": "exam_handwriting",
            "CNS: motor power grade": "exam_cns", "(1) Upper extremities": "exam_upper",
            "(2) Lower extremities": "exam_lower", "Gait": "exam_gait", "Sensation": "exam_sensation",
            "Cognition": "exam_cognition", "Mood": "exam_mood", "IQ หรือ Mentality": "exam_iq"
        }
        for item, key in exam_items.items():
            col1, col2 = st.columns([2, 3])
            col1.markdown(f"**{item}**")
            exam_status = col2.radio("Status", ["Normal", "Abnormal"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
            exam_detail = col2.text_input("Detail", key=f"{key}_detail", placeholder="ระบุความผิดปกติ (ถ้ามี)")
            form_data[f'ตรวจร่างกาย: {item}'] = exam_detail if exam_status == "Abnormal" and exam_detail else exam_status

        st.subheader("ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        blood_lead_level = st.number_input("ระดับตะกั่วในเลือด (µg/dL):", min_value=0.0, format="%.2f", key="lab_blood_lead")
        form_data['ระดับตะกั่วในเลือด (µg/dL)'] = blood_lead_level
        
        is_pregnant = st.radio("เป็นหญิงตั้งครรภ์หรือไม่:", ["ไม่ใช่", "ใช่"], key="is_pregnant", horizontal=True)
        form_data['เป็นหญิงตั้งครรภ์'] = is_pregnant

        lab_items = {"CBC": "lab_cbc", "BUN/Cr": "lab_bun", "SGPT/SGOT": "lab_sgpt", "TB/DB": "lab_tb", "Uric acid": "lab_uric", "UA": "lab_ua"}
        for item, key in lab_items.items():
            col1, col2 = st.columns([1, 2])
            col1.markdown(item)
            lab_status = col2.radio("Status", ["ปกติ", "ผิดปกติ"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
            lab_detail = col2.text_input("Detail", key=f"{key}_detail", placeholder="ระบุผล")
            form_data[f'ผลตรวจ: {item}'] = lab_detail if lab_status == "ผิดปกติ" and lab_detail else lab_status
        
        st.subheader("ข้อมูลแพทย์ผู้ตรวจ")
        col1, col2 = st.columns(2)
        form_data['แพทย์ผู้ตรวจ'] = col1.text_input("ชื่อ - นามสกุล แพทย์ผู้ตรวจร่างกาย:")
        form_data['เบอร์โทรแพทย์'] = col2.text_input("เบอร์โทรศัพท์:")

        st.markdown("---")
        if st.button("ประเมินผล", use_container_width=True, type="primary"):
            # Dummy assessment logic
            if blood_lead_level > 10:
                st.error("ผลการประเมิน: มีความเสี่ยง", icon="⚠️")
                with st.expander("ดูคำแนะนำ", expanded=True):
                    st.subheader("คำแนะนำสำหรับกลุ่มงานอาชีวเวชกรรม")
                    st.markdown("- ติดตามผลเลือดซ้ำ\n- ตรวจสอบสภาพแวดล้อมการทำงาน")
                    st.subheader("คำแนะนำสำหรับผู้ป่วย")
                    st.markdown("- ปรึกษาแพทย์เพื่อรับคำแนะนำ\n- หลีกเลี่ยงการสัมผัสตะกั่วเพิ่มเติม")
            else:
                st.success("ผลการประเมิน: ปกติ", icon="✅")
                with st.expander("ดูคำแนะนำ", expanded=True):
                    st.subheader("คำแนะนำสำหรับกลุ่มงานอาชีวเวชกรรม")
                    st.markdown("- ตรวจสุขภาพตามระยะเวลาที่กำหนด")
                    st.subheader("คำแนะนำสำหรับผู้ป่วย")
                    st.markdown("- รักษาสุขภาพและปฏิบัติตามหลักชีวอนามัย")


    # --- Submitter Information ---
    with st.expander("ข้อมูลผู้บันทึก (เจ้าหน้าที่)", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ผู้บันทึกข้อมูล'] = col1.text_input("ผู้บันทึกข้อมูล ชื่อ:")
        form_data['เบอร์ติดต่อผู้บันทึก'] = col2.text_input("เบอร์ติดต่อ:")

    # --- Actions ---
    st.markdown("---")
    if st.button("📋 คัดลอกข้อมูลทั้งหมด", use_container_width=True):
        report_text = []
        for key, value in form_data.items():
            if isinstance(value, str) and value.strip() and value not in ["-- เลือก --", "Normal", "ปกติ", "ไม่ใช่"]:
                report_text.append(f"**{key}:** {value}")
            elif not isinstance(value, str) and value:
                 report_text.append(f"**{key}:** {value}")
        
        if report_text:
            st.success("ข้อมูลพร้อมสำหรับคัดลอกด้านล่าง")
            st.text_area("ข้อมูลสำหรับคัดลอก", "\n".join(report_text), height=400)
        else:
            st.warning("ยังไม่มีข้อมูลให้คัดลอก กรุณากรอกแบบฟอร์มก่อน")

    st.info("สำหรับการพิมพ์หรือบันทึกเป็น PDF กรุณาใช้ฟังก์ชันของเบราว์เซอร์ (Ctrl+P หรือ Cmd+P)")
