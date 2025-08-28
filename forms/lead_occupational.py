import streamlit as st
import datetime
import pandas as pd

def render():
    """
    Renders the improved Lead Occupational Investigation Form with evaluation and reporting.
    """

    st.header("แบบสอบสวนโรคจากตะกั่วหรือสารประกอบของตะกั่ว")
    st.caption("สำหรับกลุ่มงานอาชีวเวชกรรม (อ้างอิงเอกสารแนบที่ 1 หน้า 30-33)")

    # --- Data Collection Dictionary ---
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    with st.form("lead_investigation_form"):
        form_data = {}

        with st.container(border=True):
            st.subheader("ข้อมูลการสอบสวน")
            col1, col2 = st.columns(2)
            form_data['วันที่สอบสวน'] = col1.date_input("วัน/เดือน/ปี ที่ดำเนินการสอบสวน:", datetime.date.today())
            form_data['ชื่อสถานประกอบการ'] = col2.text_input("ชื่อโรงงาน/สถานประกอบการ/สถานที่เกิดเหตุ:")
            form_data['ประเภทกิจการ'] = st.text_input("ประเภทสถานประกอบกิจการ:")

        # --- Section 1: Personal Information ---
        with st.container(border=True):
            st.subheader("ส่วนที่ 1: ข้อมูลส่วนบุคคล")
            form_data['ชื่อ-นามสกุล'] = st.text_input("1.1 ชื่อ - นามสกุล:")
            form_data['ที่อยู่ปัจจุบัน'] = st.text_area("1.2 ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด")

            col1, col2 = st.columns(2)
            with col1:
                st.write("1.3 อาศัยอยู่ในพื้นที่มาแล้ว:")
                res_years = st.number_input("ปี", min_value=0, step=1, key="res_years")
            with col2:
                st.write("‎") # Spacer for alignment
                res_months = st.number_input("เดือน", min_value=0, max_value=11, step=1, key="res_months")
            form_data['อาศัยอยู่ในพื้นที่มาแล้ว'] = f"{res_years} ปี {res_months} เดือน"

            col1, col2 = st.columns(2)
            form_data['อายุ'] = col1.number_input("1.4 อายุ (ปี):", min_value=0, step=1)
            form_data['เพศ'] = col2.radio("1.5 เพศ:", ["ชาย", "หญิง"], horizontal=True)

            col1, col2 = st.columns(2)
            marital_status_option = col1.radio("1.6 สถานภาพสมรส:",
                         ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"])
            if marital_status_option == "อื่นๆ":
                marital_status_other = col1.text_input("อื่นๆ (โปรดระบุ):", key="marital_other")
                form_data['สถานภาพสมรส'] = marital_status_other
            else:
                form_data['สถานภาพสมรส'] = marital_status_option

            form_data['ระดับการศึกษาสูงสุด'] = col2.selectbox("1.7 ระดับการศึกษาสูงสุด:",
                         ["-- เลือก --", "ไม่ได้ศึกษา", "ประถมศึกษา", "มัธยมศึกษา/ปวช.",
                          "อนุปริญญา/ปวส.", "ปริญญาตรี", "สูงกว่าปริญญาตรี"])

            st.write("1.8 จํานวนสมาชิกในครอบครัว:")
            col1, col2 = st.columns(2)
            fam_total = col1.number_input("รวมทั้งหมด (คน)", min_value=0, step=1)
            fam_children = col2.number_input("เด็กอายุ < 7 ปี (คน)", min_value=0, step=1)
            form_data['จำนวนสมาชิกในครอบครัว'] = f"รวม: {fam_total} คน, เด็ก < 7 ปี: {fam_children} คน"

        # --- Section 2: Health and Behavior ---
        with st.container(border=True):
            st.subheader("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ")
            smoking_hist = st.radio("2.1 ประวัติการสูบบุหรี่:", ["ไม่สูบ", "เคยสูบแต่เลิกแล้ว", "ปัจจุบันยังสูบ"])
            if smoking_hist == "เคยสูบแต่เลิกแล้ว":
                quit_years = st.number_input("เลิกมาแล้ว (ปี)", min_value=0, step=1, key="smoke_quit")
                form_data['ประวัติการสูบบุหรี่'] = f"เคยสูบแต่เลิกแล้ว ({quit_years} ปี)"
            elif smoking_hist == "ปัจจุบันยังสูบ":
                current_amount = st.number_input("ปัจจุบันยังสูบ (มวน/วัน)", min_value=0, step=1, key="smoke_current")
                form_data['ประวัติการสูบบุหรี่'] = f"ปัจจุบันยังสูบ ({current_amount} มวน/วัน)"
            else:
                form_data['ประวัติการสูบบุหรี่'] = smoking_hist

            smoking_place_opt = st.radio("2.2 สถานที่หรือบริเวณที่ท่านสูบบุหรี่:",
                       ["ไม่สูบ", "บริเวณสถานที่ทำงาน/สูบพร้อมขณะทำงาน", "บริเวณที่จัดไว้",
                        "บริเวณรับประทานอาหาร/โรงอาหาร", "อื่นๆ"])
            if smoking_place_opt == "อื่นๆ":
                smoking_place_other = st.text_input("อื่นๆ (โปรดระบุ):", key="smoke_place_other")
                form_data['สถานที่สูบบุหรี่'] = smoking_place_other
            else:
                form_data['สถานที่สูบบุหรี่'] = smoking_place_opt

            eating_place_opt = st.radio("2.3 ท่านรับประทานอาหารในสถานที่ทํางานหรือไม่:",
                 ["ไม่ได้รับประทาน", "รับประทานในบริเวณเดียวกับที่ปฏิบัติงาน", "รับประทานในโรงอาหาร", "อื่นๆ"])
            if eating_place_opt == "อื่นๆ":
                eating_place_other = st.text_input("อื่นๆ (โปรดระบุ):", key="eat_place_other")
                form_data['การรับประทานอาหารในที่ทำงาน'] = eating_place_other
            else:
                form_data['การรับประทานอาหารในที่ทำงาน'] = eating_place_opt

            food_source_opts = st.multiselect("2.4 แหล่งที่มาของอาหาร (ตอบได้มากกว่า 1 ข้อ):",
                       ["ปรุง/ทำอาหารเอง", "ซื้อจากผู้ประกอบการเป็นหลัก", "อื่นๆ"])
            if "อื่นๆ" in food_source_opts:
                food_source_other = st.text_input("อื่นๆ (โปรดระบุ):", key="food_src_other")
                form_data['แหล่งที่มาของอาหาร'] = ", ".join(food_source_opts) + f", อื่นๆ: {food_source_other}"
            else:
                form_data['แหล่งที่มาของอาหาร'] = ", ".join(food_source_opts)


            water_source_opt = st.radio("2.5 แหล่งน้ำดื่ม:", ["น้ำประปา", "น้ำซื้อ", "นายจ้างจัดให้", "อื่นๆ"])
            if water_source_opt == "อื่นๆ":
                water_source_other = st.text_input("อื่นๆ (โปรดระบุ):", key="water_src_other")
                form_data['แหล่งน้ำดื่ม'] = water_source_other
            else:
                form_data['แหล่งน้ำดื่ม'] = water_source_opt

            disease_opts = st.multiselect("2.6 ประวัติโรคประจําตัว:", ["ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง", "อื่นๆ"])
            if "อื่นๆ" in disease_opts:
                disease_other = st.text_input("อื่นๆ (โปรดระบุ):", key="disease_other")
                form_data['ประวัติโรคประจำตัว'] = ", ".join(disease_opts) + f", อื่นๆ: {disease_other}"
            else:
                form_data['ประวัติโรคประจำตัว'] = ", ".join(disease_opts) if disease_opts else "ไม่มี"

        # --- Section 3: Work Info ---
        with st.container(border=True):
            st.subheader("ส่วนที่ 3: ลักษณะงานและการประกอบอาชีพ")
            col1, col2 = st.columns([3, 1])
            job_current = col1.text_input("3.1 อาชีพปัจจุบัน:")
            job_current_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_current_years")
            form_data['อาชีพปัจจุบัน'] = f"{job_current} ({job_current_years} ปี)"

            form_data['ลักษณะงานปัจจุบัน'] = st.text_input("3.2 ลักษณะงาน/ตำแหน่งงาน/แผนกที่ทํางานปัจจุบัน:")

            st.write("3.3 ระยะเวลาที่ทํางาน:")
            col1, col2 = st.columns(2)
            work_hours = col1.number_input("ชั่วโมง/วัน", min_value=0, step=1, key="work_hours")
            work_days = col2.number_input("วัน/สัปดาห์", min_value=0, step=1, key="work_days")
            form_data['ระยะเวลาทำงาน'] = f"{work_hours} ชม./วัน, {work_days} วัน/สัปดาห์"

            col1, col2 = st.columns([3, 1])
            job_previous = col1.text_input("3.4 อาชีพเดิมก่อนมาทํางานปัจจุบัน:")
            job_previous_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_prev_years")
            form_data['อาชีพเดิม'] = f"{job_previous} ({job_previous_years} ปี)"

        # --- Section 4: Risk Factors ---
        with st.container(border=True):
            st.subheader("ส่วนที่ 4: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่ว")
            risk_jobs_list = [
                "งานเกี่ยวกับแบตเตอรี่", "ถลุง/หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
                "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน", "ซ่อมเรือประมง", "ซ่อมเครื่องใช้ไฟฟ้า",
                "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ/เครื่องปั้นดินเผา", "งานโรงพิมพ์/หล่อตัวพิมพ์",
                "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
            ]

            risk_jobs_household = st.multiselect("4.1 ปัจจุบันท่านหรือสมาชิกในบ้านมีผู้ใดประกอบอาชีพต่อไปนี้หรือไม่:", risk_jobs_list)
            risk_jobs_household_other = st.text_input("อาชีพเสี่ยงอื่นๆ (โปรดระบุ):", key="risk_job_other")
            if risk_jobs_household_other:
                risk_jobs_household.append(risk_jobs_household_other)
            form_data['อาชีพเสี่ยงในครัวเรือน'] = ", ".join(risk_jobs_household)

            risk_places_nearby = st.multiselect("4.2 โรงงาน/สถานประกอบการ/ร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย):", risk_jobs_list, key="risk_places")
            risk_places_nearby_other = st.text_input("สถานประกอบการเสี่ยงอื่นๆ (โปรดระบุ):", key="risk_place_other")
            if risk_places_nearby_other:
                risk_places_nearby.append(risk_places_nearby_other)
            form_data['สถานประกอบการเสี่ยงใกล้ที่พัก'] = ", ".join(risk_places_nearby)

            st.markdown("---")
            st.write("**4.3 ท่านใช้อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลใดระหว่างการทํางาน:**")
            ppe_items = ["ถุงมือยาง/หนัง", "หมวก/ผ้าคลุมผม", "หน้ากากป้องกันฝุ่น/ผ้าปิดจมูก", "แว่นตา", "รองเท้าบูธ/ผ้าใบ", "เสื้อแขนยาว", "กางเกงขายาว"]
            ppe_options = ["ไม่ใช้", "ใช้บางครั้ง", "ใช้ทุกครั้ง"]
            
            # Create a more compact layout for PPE
            cols = st.columns(3)
            for i, item in enumerate(ppe_items):
                with cols[i % 3]:
                    form_data[f'PPE: {item}'] = st.radio(f"{i+1}. {item}", ppe_options, horizontal=True, key=f"ppe_{i}")
            
            ppe_other_name = st.text_input("8. อื่นๆ ระบุ", key="ppe_other_name")
            if ppe_other_name:
                form_data[f'PPE: {ppe_other_name}'] = st.radio(" ", ppe_options, horizontal=True, key="ppe_other_opt", label_visibility="collapsed")

            st.markdown("---")
            
            ppe_source = st.multiselect("4.4 อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลที่ท่านใช้ ได้มาอย่างไร:", ["ซื้อเอง", "ได้รับจากโรงงาน/บริษัท", "อื่นๆ"])
            if "อื่นๆ" in ppe_source:
                ppe_source_other = st.text_input("แหล่งอื่นๆ (โปรดระบุ):", key="ppe_src_other")
                form_data['แหล่งที่มาของอุปกรณ์คุ้มครอง'] = ", ".join(ppe_source) + f", อื่นๆ: {ppe_source_other}"
            else:
                 form_data['แหล่งที่มาของอุปกรณ์คุ้มครอง'] = ", ".join(ppe_source)

            col1, col2 = st.columns(2)
            form_data['ที่เก็บอุปกรณ์'] = col1.radio("4.5 ท่านเก็บอุปกรณ์ฯ ไว้ที่ใด:", ["บ้าน", "ที่ทำงาน"])

            ppe_care_opt = col2.radio("4.6 ท่านจัดเก็บรักษาอุปกรณ์ฯ หลังใช้งานอย่างไร:", ["ตามพื้น/ผนังห้องภายในบ้าน", "ล็อกเกอร์หรือตู้เก็บเฉพาะ", "อื่นๆ"])
            if ppe_care_opt == "อื่นๆ":
                ppe_care_other = col2.text_input("อื่นๆ (โปรดระบุ):", key="ppe_care_other", label_visibility="collapsed")
                form_data['วิธีเก็บรักษาอุปกรณ์'] = ppe_care_other
            else:
                form_data['วิธีเก็บรักษาอุปกรณ์'] = ppe_care_opt
            
            st.markdown("---")
            st.write("**4.7 พฤติกรรมด้านสุขลักษณะและความปลอดภัยในการทํางาน:**")
            hygiene_items = ["ล้างมือก่อนรับประทานอาหาร", "อาบน้ำก่อนออกจากสถานที่ทำงาน", "เปลี่ยนเสื้อผ้าก่อนออกจากสถานที่ปฏิบัติงาน", "เปลี่ยนรองเท้าก่อนออกจากสถานที่ทำงาน", "นำหรือสวมเสื้อผ้าที่ปนเปื้อนกลับบ้าน"]
            hygiene_options = ["ไม่ได้ปฏิบัติ/ไม่ใช่", "บางครั้ง", "ทุกครั้ง/ประจํา"]
            
            cols_hygiene = st.columns(2)
            for i, item in enumerate(hygiene_items):
                 with cols_hygiene[i % 2]:
                    form_data[f'สุขลักษณะ: {item}'] = st.radio(f"{i+1}. {item}", hygiene_options, horizontal=True, key=f"hygiene_{i}")

        # --- Section 5: Symptoms ---
        with st.container(border=True):
            st.subheader("ส่วนที่ 5: ลักษณะอาการที่ส่งผลกระทบทางสุขภาพ (3 สัปดาห์ที่ผ่านมา)")
            symptoms = [
                "อ่อนเพลีย", "เบื่ออาหาร", "คลื่นไส้ อาเจียน", "ท้องผูก", "ปวดท้องรุนแรงเป็นพัก ๆ",
                "ปวดตามข้อ กล้ามเนื้อ", "อาการปวดเมื่อยตามร่างกาย", "ปวดศีรษะ", "ซีด", "ซึม", "ชัก",
                "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย", "น้ำหนักลดโดยไม่ทราบสาเหตุ", "มือสั่น",
                "มือ เท้า อ่อนแรง", "ผื่น"
            ]
            symptom_options = ["ไม่มี", "นาน ๆ ครั้ง", "เป็นประจําหรือแทบทุกวัน"]
            
            cols_symptoms = st.columns(3)
            for i, symptom in enumerate(symptoms):
                with cols_symptoms[i % 3]:
                    form_data[f'อาการ: {symptom}'] = st.radio(symptom, symptom_options, key=f"occ_symptom_{symptom.replace(' ', '_')}", horizontal=False)

        # --- Submitter Information ---
        with st.container(border=True):
            st.subheader("ข้อมูลผู้บันทึก (เจ้าหน้าที่)")
            col1, col2 = st.columns(2)
            form_data['ผู้บันทึกข้อมูล'] = col1.text_input("ผู้บันทึกข้อมูล ชื่อ:")
            form_data['เบอร์ติดต่อผู้บันทึก'] = col2.text_input("เบอร์ติดต่อ:")
        
        st.session_state.form_data = form_data
        submitted = st.form_submit_button("ประเมินความเสี่ยงและสร้างรายงาน", use_container_width=True, type="primary")

    if submitted:
        evaluate_and_display_results(st.session_state.form_data)


def evaluate_lead_risk(form_data):
    """
    Evaluates lead exposure risk based on form data and returns risk level and recommendations.
    """
    risk_score = 0
    recommendations_occ = []
    recommendations_patient = []

    # Risk Factor Scoring
    if form_data.get('อาชีพเสี่ยงในครัวเรือน'):
        risk_score += len(form_data['อาชีพเสี่ยงในครัวเรือน'].split(',')) * 2
    if form_data.get('สถานประกอบการเสี่ยงใกล้ที่พัก'):
        risk_score += len(form_data['สถานประกอบการเสี่ยงใกล้ที่พัก'].split(',')) * 2

    # PPE Scoring
    for key, value in form_data.items():
        if key.startswith('PPE:'):
            if value == "ไม่ใช้":
                risk_score += 2
            elif value == "ใช้บางครั้ง":
                risk_score += 1

    # Hygiene Scoring
    hygiene_scores = {
        "ล้างมือก่อนรับประทานอาหาร": {"ไม่ได้ปฏิบัติ/ไม่ใช่": 2, "บางครั้ง": 1, "ทุกครั้ง/ประจํา": 0},
        "อาบน้ำก่อนออกจากสถานที่ทำงาน": {"ไม่ได้ปฏิบัติ/ไม่ใช่": 2, "บางครั้ง": 1, "ทุกครั้ง/ประจํา": 0},
        "เปลี่ยนเสื้อผ้าก่อนออกจากสถานที่ปฏิบัติงาน": {"ไม่ได้ปฏิบัติ/ไม่ใช่": 2, "บางครั้ง": 1, "ทุกครั้ง/ประจํา": 0},
        "เปลี่ยนรองเท้าก่อนออกจากสถานที่ทำงาน": {"ไม่ได้ปฏิบัติ/ไม่ใช่": 2, "บางครั้ง": 1, "ทุกครั้ง/ประจํา": 0},
        "นำหรือสวมเสื้อผ้าที่ปนเปื้อนกลับบ้าน": {"ไม่ได้ปฏิบัติ/ไม่ใช่": 0, "บางครั้ง": 1, "ทุกครั้ง/ประจํา": 2}
    }
    for item, scores in hygiene_scores.items():
        value = form_data.get(f'สุขลักษณะ: {item}')
        if value in scores:
            risk_score += scores[value]

    # Symptom Scoring
    for key, value in form_data.items():
        if key.startswith('อาการ:'):
            if value == "เป็นประจําหรือแทบทุกวัน":
                risk_score += 2
            elif value == "นาน ๆ ครั้ง":
                risk_score += 1

    # Determine Risk Level and Recommendations
    if risk_score >= 25:
        risk_level = "ความเสี่ยงสูง"
        recommendations_occ.extend([
            "ดำเนินการสอบสวนโรคในสถานประกอบการ หรือสถานที่ทำงาน เพื่อค้นหาสาเหตุหรือปัจจัยเสี่ยงที่ก่อให้เกิดโรค",
            "พิจารณาส่งตรวจระดับตะกั่วในเลือด (Blood Lead Level) เพื่อยืนยันการสัมผัส",
            "เสนอมาตรการป้องกันควบคุมโรคอย่างเร่งด่วน และค้นหาผู้ป่วยเพิ่มเติม"
        ])
        recommendations_patient.extend([
            "ควรหยุดพักงานในพื้นที่เสี่ยงทันทีและปรึกษาแพทย์ผู้เชี่ยวชาญ",
            "ปฏิบัติตามหลักสุขอนามัยส่วนบุคคลอย่างเคร่งครัดสูงสุด",
            "งดการนำเสื้อผ้าและอุปกรณ์การทำงานกลับบ้านโดยเด็ดขาด"
        ])
    elif 10 <= risk_score < 25:
        risk_level = "ความเสี่ยงปานกลาง"
        recommendations_occ.extend([
            "ควรพิจารณาเดินสำรวจ (Walk-through survey) ในสถานประกอบการเพื่อประเมินความเสี่ยงเพิ่มเติม",
            "แนะนำให้มีการตรวจสุขภาพตามปัจจัยเสี่ยง (ตรวจระดับตะกั่วในเลือด) สำหรับผู้ปฏิบัติงาน",
            "ทบทวนและให้ความรู้เรื่องการใช้อุปกรณ์ป้องกันส่วนบุคคลและสุขอนามัย"
        ])
        recommendations_patient.extend([
            "ต้องสวมใส่อุปกรณ์ป้องกันส่วนบุคคล (PPE) ที่เหมาะสมตลอดเวลาการทำงาน",
            "ล้างมือทุกครั้งก่อนรับประทานอาหาร ดื่มน้ำ และสูบบุหรี่",
            "อาบน้ำและเปลี่ยนเสื้อผ้าก่อนกลับบ้านทุกครั้ง"
        ])
    else:
        risk_level = "ความเสี่ยงต่ำ"
        recommendations_occ.extend([
            "เฝ้าระวังและติดตามอาการอย่างต่อเนื่อง",
            "จัดให้มีการอบรมให้ความรู้ด้านอาชีวอนามัยและความปลอดภัยเป็นประจำทุกปี",
            "ส่งเสริมสุขอนามัยที่ดีในสถานที่ทำงาน"
        ])
        recommendations_patient.extend([
            "รักษาสุขภาพและปฏิบัติตามหลักชีวอนามัยพื้นฐาน",
            "สังเกตอาการผิดปกติของตนเอง หากมีอาการควรรีบปรึกษาแพทย์",
            "เข้ารับการตรวจสุขภาพประจำปีอย่างสม่ำเสมอ"
        ])

    return risk_level, risk_score, recommendations_occ, recommendations_patient

def generate_report(form_data, risk_level, risk_score, recommendations_occ, recommendations_patient):
    """
    Generates a formatted Markdown report from the form data.
    """
    report = f"# รายงานสรุปผลการสอบสวนโรคจากตะกั่ว\n\n"
    report += f"**วันที่สอบสวน:** {form_data.get('วันที่สอบสวน', 'N/A')}\n\n"
    report += f"**สถานประกอบการ:** {form_data.get('ชื่อสถานประกอบการ', 'N/A')}\n\n"
    report += f"**ประเภทกิจการ:** {form_data.get('ประเภทกิจการ', 'N/A')}\n\n"

    report += "## ส่วนที่ 1: ข้อมูลส่วนบุคคล\n"
    report += f"- **ชื่อ-นามสกุล:** {form_data.get('ชื่อ-นามสกุล', 'N/A')}\n"
    report += f"- **อายุ:** {form_data.get('อายุ', 'N/A')} ปี\n"
    report += f"- **เพศ:** {form_data.get('เพศ', 'N/A')}\n"
    report += f"- **ที่อยู่:** {form_data.get('ที่อยู่ปัจจุบัน', 'N/A')}\n"
    report += f"- **ระยะเวลาอาศัย:** {form_data.get('อาศัยอยู่ในพื้นที่มาแล้ว', 'N/A')}\n"
    report += f"- **สถานภาพสมรส:** {form_data.get('สถานภาพสมรส', 'N/A')}\n"
    report += f"- **การศึกษา:** {form_data.get('ระดับการศึกษาสูงสุด', 'N/A')}\n"
    report += f"- **สมาชิกในครอบครัว:** {form_data.get('จำนวนสมาชิกในครอบครัว', 'N/A')}\n\n"

    report += "## ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ\n"
    report += f"- **ประวัติการสูบบุหรี่:** {form_data.get('ประวัติการสูบบุหรี่', 'N/A')}\n"
    report += f"- **สถานที่สูบบุหรี่:** {form_data.get('สถานที่สูบบุหรี่', 'N/A')}\n"
    report += f"- **การรับประทานอาหารในที่ทำงาน:** {form_data.get('การรับประทานอาหารในที่ทำงาน', 'N/A')}\n"
    report += f"- **แหล่งอาหาร:** {form_data.get('แหล่งที่มาของอาหาร', 'N/A')}\n"
    report += f"- **แหล่งน้ำดื่ม:** {form_data.get('แหล่งน้ำดื่ม', 'N/A')}\n"
    report += f"- **โรคประจำตัว:** {form_data.get('ประวัติโรคประจำตัว', 'N/A')}\n\n"

    report += "## ส่วนที่ 3: ลักษณะงานและการประกอบอาชีพ\n"
    report += f"- **อาชีพปัจจุบัน:** {form_data.get('อาชีพปัจจุบัน', 'N/A')}\n"
    report += f"- **ลักษณะงานปัจจุบัน:** {form_data.get('ลักษณะงานปัจจุบัน', 'N/A')}\n"
    report += f"- **ระยะเวลาทำงาน:** {form_data.get('ระยะเวลาทำงาน', 'N/A')}\n"
    report += f"- **อาชีพเดิม:** {form_data.get('อาชีพเดิม', 'N/A')}\n\n"

    report += "## ส่วนที่ 4: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่ว\n"
    report += f"- **อาชีพเสี่ยงในครัวเรือน:** {form_data.get('อาชีพเสี่ยงในครัวเรือน', 'ไม่มี')}\n"
    report += f"- **สถานประกอบการเสี่ยงใกล้ที่พัก:** {form_data.get('สถานประกอบการเสี่ยงใกล้ที่พัก', 'ไม่มี')}\n"
    report += "### การใช้อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคล (PPE)\n"
    for key, value in form_data.items():
        if key.startswith('PPE:'):
            report += f"- **{key.replace('PPE: ', '')}:** {value}\n"
    report += "\n### พฤติกรรมด้านสุขลักษณะ\n"
    for key, value in form_data.items():
        if key.startswith('สุขลักษณะ:'):
            report += f"- **{key.replace('สุขลักษณะ: ', '')}:** {value}\n"
    report += "\n"

    report += "## ส่วนที่ 5: อาการที่ส่งผลกระทบทางสุขภาพ\n"
    symptoms_reported = []
    for key, value in form_data.items():
        if key.startswith('อาการ:') and value != "ไม่มี":
            symptoms_reported.append(f"- **{key.replace('อาการ: ', '')}:** {value}")
    if symptoms_reported:
        report += "\n".join(symptoms_reported)
    else:
        report += "ไม่มีอาการผิดปกติที่รายงาน"
    report += "\n\n"
    
    report += "-----\n\n"
    report += "## ผลการประเมินและคำแนะนำ\n"
    report += f"### คะแนนความเสี่ยง: **{risk_score}**\n"
    report += f"### ระดับความเสี่ยง: **{risk_level}**\n\n"
    
    report += "### คำแนะนำสำหรับกลุ่มงานอาชีวเวชกรรม:\n"
    for rec in recommendations_occ:
        report += f"- {rec}\n"
    report += "\n"
    
    report += "### คำแนะนำในการปฏิบัติตัวสำหรับผู้ป่วย:\n"
    for rec in recommendations_patient:
        report += f"- {rec}\n"
    
    return report

def evaluate_and_display_results(form_data):
    """
    Calls evaluation, generates report, and displays them in the UI.
    """
    risk_level, risk_score, recommendations_occ, recommendations_patient = evaluate_lead_risk(form_data)

    if risk_level == "ความเสี่ยงสูง":
        st.error(f"**ผลการประเมิน: {risk_level}** (คะแนน: {risk_score})", icon="�")
    elif risk_level == "ความเสี่ยงปานกลาง":
        st.warning(f"**ผลการประเมิน: {risk_level}** (คะแนน: {risk_score})", icon="⚠️")
    else:
        st.success(f"**ผลการประเมิน: {risk_level}** (คะแนน: {risk_score})", icon="✅")

    with st.expander("ดูคำแนะนำและรายงานสรุป", expanded=True):
        st.subheader("คำแนะนำเบื้องต้น")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**สำหรับกลุ่มงานอาชีวเวชกรรม:**")
            for rec in recommendations_occ:
                st.write(f"- {rec}")
        with col2:
            st.markdown("**สำหรับผู้ป่วย:**")
            for rec in recommendations_patient:
                st.write(f"- {rec}")

        st.markdown("---")
        
        report_text = generate_report(form_data, risk_level, risk_score, recommendations_occ, recommendations_patient)
        st.subheader("รายงานสรุปสำหรับพิมพ์")
        st.info("คุณสามารถคัดลอกข้อความด้านล่าง หรือใช้ฟังก์ชันพิมพ์ของเบราว์เซอร์ (Ctrl+P หรือ Cmd+P) เพื่อบันทึกเป็น PDF")
        st.markdown(report_text)

�
