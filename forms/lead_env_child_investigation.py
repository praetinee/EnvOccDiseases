# -*- coding: utf-8 -*-
import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Child Investigation Form (Pb), correctly structured as per the source document."""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของเด็กในบ้านพักอาศัย และในชุมชน")
    st.caption("(แบบสอบสวน Pb)")

    # This dictionary will hold all the collected data.
    form_data = {}

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อเด็ก'] = col1.text_input("1.1 ชื่อ ด.ช./ด.ญ.:")
        form_data['เลขบัตรประชาชน'] = col2.text_input("เลขบัตรประชาชน:")
        
        col1, col2, col3 = st.columns(3)
        form_data['วันเกิด'] = col1.date_input("1.2 วัน/เดือน/ปีเกิด:")
        form_data['น้ำหนัก'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("1.3 ชื่อผู้ปกครอง:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, เบอร์โทร")
        
        st.write("จำนวนสมาชิกในครอบครัว:")
        col1, col2 = st.columns(2)
        form_data['สมาชิกทั้งหมด'] = col1.number_input("รวม (คน)", min_value=0, step=1, key="pb_total_fam")
        form_data['สมาชิกเด็ก<7ปี'] = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1, key="pb_u7_fam")

        # --- Section 1.4: Child History ---
        st.subheader("1.4 ประวัติเด็ก")
        child_history_data = {}

        edu_status = st.radio("1) การศึกษาของเด็ก", ["ยังไม่ได้เข้าเรียน", "เข้าเรียน"], key="pb_edu_status")
        if edu_status == "เข้าเรียน":
            edu_level = st.radio("ระดับ", ["ก่อนอนุบาล", "อนุบาล", "ประถม"], horizontal=True, key="pb_edu_level")
            col1, col2 = st.columns(2)
            edu_years = col1.number_input("เด็กเรียนอยู่ในโรงเรียนปัจจุบันเป็นระยะเวลา (ปี)", min_value=0, step=1, key="pb_edu_years")
            edu_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="pb_edu_months")
            child_history_data['การศึกษา'] = f"{edu_level}, ระยะเวลา {edu_years} ปี {edu_months} เดือน"
        else:
            child_history_data['การศึกษา'] = edu_status

        col1, col2 = st.columns(2)
        res_years = col1.number_input("2) เด็กอาศัยอยู่ที่ปัจจุบันประมาณ (ปี)", min_value=0, step=1, key="pb_res_years")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="pb_res_months")
        child_history_data['ระยะเวลาอาศัย'] = f"{res_years} ปี {res_months} เดือน"
        
        comorbidity = st.radio("3) เด็กมีโรคประจำตัวหรือไม่", ["ไม่มี", "มี"], key="pb_comorbidity")
        if comorbidity == "มี":
            comorbidity_detail = st.text_input("ระบุ:", key="pb_comorbidity_detail")
            child_history_data['โรคประจำตัว'] = f"มี ({comorbidity_detail})"
        else:
            child_history_data['โรคประจำตัว'] = "ไม่มี"

        st.write("4) เด็กรับประทานยาประจำ")

        # Define callback functions to handle the exclusive logic
        def med_none_callback():
            # If "None" is checked, uncheck all others
            if st.session_state.get("pb_med_none"):
                st.session_state.pb_med_regular = False
                st.session_state.pb_med_herbal = False
                st.session_state.pb_med_gwaad = False

        def med_others_callback():
            # If any other option is checked, uncheck "None"
            if st.session_state.get("pb_med_regular") or st.session_state.get("pb_med_herbal") or st.session_state.get("pb_med_gwaad"):
                st.session_state.pb_med_none = False
        
        # Using columns for a cleaner layout
        col_med1, col_med2 = st.columns(2)
        with col_med1:
            st.checkbox("ไม่ได้รับประทาน", key="pb_med_none", on_change=med_none_callback)
            st.checkbox("รับประทาน", key="pb_med_regular", on_change=med_others_callback)
        with col_med2:
            st.checkbox("รับประทานยาสมุนไพร", key="pb_med_herbal", on_change=med_others_callback)
            st.checkbox("ยากวาดลิ้น", key="pb_med_gwaad", on_change=med_others_callback)
        
        # Collect data based on the current state from session_state
        med_details_list = []
        
        # Use .get() to avoid errors if the key doesn't exist yet
        if st.session_state.get("pb_med_regular"):
            med_detail_regular = st.text_input("ระบุ (รับประทาน):", key="pb_med_detail_regular")
            med_details_list.append(f"รับประทาน ({med_detail_regular})" if med_detail_regular else "รับประทาน")

        if st.session_state.get("pb_med_herbal"):
            med_detail_herbal = st.text_input("ระบุ (รับประทานยาสมุนไพร):", key="pb_med_detail_herbal")
            med_details_list.append(f"รับประทานยาสมุนไพร ({med_detail_herbal})" if med_detail_herbal else "รับประทานยาสมุนไพร")
        
        if st.session_state.get("pb_med_gwaad"):
            med_details_list.append("ยากวาดลิ้น")

        # Final data assignment
        if st.session_state.get("pb_med_none"):
            child_history_data['ยาประจำ'] = "ไม่ได้รับประทาน"
        else:
            child_history_data['ยาประจำ'] = ", ".join(med_details_list) if med_details_list else ""

        child_history_data['อาบน้ำ'] = st.number_input("5) เด็กอาบน้ำวันละกี่ครั้ง", min_value=0, step=1, key="pb_bathing")
        child_history_data['ดื่มนม'] = st.radio("6) เด็กดื่มนมอะไร", ["นมแม่อย่างเดียว", "นมกระป๋อง/นมกล่องอย่างเดียว", "ทั้งนมแม่และนมกระป๋อง/นมกล่อง"], key="pb_milk")

        visit_workplace = st.radio("7) เด็กเคยไปบริเวณที่ทำงานเกี่ยวกับตะกั่วบ้างหรือไม่", ["ไม่ไป", "ไป"], key="pb_visit_work")
        child_history_data['เคยไปที่ทำงาน'] = visit_workplace
        
        if visit_workplace == "ไป":
            child_history_data['ความถี่ไปที่ทำงาน'] = st.radio("8) เด็กไปที่บริเวณงานเกี่ยวกับตะกั่วบ่อยแค่ไหน", ["นานๆ ไปครั้ง", "บ่อยมาก"], key="pb_visit_freq")
            child_history_data['ระยะเวลาที่ทำงาน'] = st.radio("9) ระยะเวลาเฉลี่ยในแต่ละวันที่เด็กอยู่บริเวณงานเกี่ยวกับตะกั่ว", ["น้อยกว่า 2 ชม.", "2 - 4 ชม.", "5 - 8 ชม.", "8 ชม. ขึ้นไป"], key="pb_visit_duration")

        form_data['ประวัติเด็ก'] = child_history_data


    # --- Section 2: Risk Factors ---
    with st.expander("ส่วนที่ 2: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่วของเด็ก", expanded=True):
        st.subheader("2.1 อาชีพผู้ปกครอง ผู้ดูแล หรือคนที่อยู่อาศัยบ้านเดียวกับเด็ก")
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)",
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]

        work_outside = st.radio("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน", ["ไม่ใช่", "ใช่"], key="pb_work_outside", horizontal=True)
        if work_outside == "ใช่":
            selected_jobs_outside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="pb_jobs_outside")
            other_job_outside = st.text_input("อื่นๆ:", key="pb_other_job_outside")
            if other_job_outside: selected_jobs_outside.append(other_job_outside)
            form_data['อาชีพนอกบ้าน'] = ", ".join(selected_jobs_outside)
            form_data['ความเกี่ยวข้อง_นอกบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="pb_rel_outside")

        work_inside = st.radio("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน", ["ไม่ใช่", "ใช่"], key="pb_work_inside", horizontal=True)
        if work_inside == "ใช่":
            selected_jobs_inside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="pb_jobs_inside")
            other_job_inside = st.text_input("อื่นๆ:", key="pb_other_job_inside")
            if other_job_inside: selected_jobs_inside.append(other_job_inside)
            form_data['อาชีพในบ้าน'] = ", ".join(selected_jobs_inside)
            form_data['ความเกี่ยวข้อง_ในบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="pb_rel_inside")

        store_nearby = st.radio("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย)", ["ไม่มี", "มี"], key="pb_store_nearby", horizontal=True)
        if store_nearby == "มี":
            selected_stores = st.multiselect("ระบุกิจการ:", risk_jobs_list, key="pb_stores_select")
            other_store = st.text_input("อื่นๆ:", key="pb_other_store_text")
            if other_store: selected_stores.append(other_store)
            form_data['ร้านค้าใกล้บ้าน'] = ", ".join(selected_stores)

        st.subheader("2.2 แผนผังลักษณะที่อยู่อาศัย")
        st.markdown("วาดแผนผังลักษณะที่อยู่อาศัย, บริเวณที่อยู่อาศัย, วัสดุ, บ้านเก่า, ทาสี, ลักษณะการเก็บข้าวของเครื่องใช้ในบ้าน และให้ใส่ **ดาว (⭐)** บริเวณที่ทำงานเกี่ยวกับตะกั่วในบ้าน, บริเวณที่นอน, ที่รับประทานอาหาร, สถานที่จัดเก็บอุปกรณ์ที่เกี่ยวข้องกับตะกั่ว (โดยการเดินสำรวจ)")
        form_data['แผนผังที่อยู่อาศัย'] = st.file_uploader("อัปโหลดรูปภาพแผนผัง", type=["png", "jpg", "jpeg"], key="pb_map_upload")
        
        st.subheader("2.3 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก")
        risk_factors_data = {}
        risk_factor_questions_by_category = {
            "**เกี่ยวกับที่พักอาศัย**": [
                ("1. บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา", "บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา", "pb_rf_paint"),
                ("2. โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น", "โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น", "pb_rf_floor"),
                ("3. มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน", "มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน", "pb_rf_tools"),
                ("4. สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)", "สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)", "pb_rf_clean"),
            ],
            "**เกี่ยวกับพฤติกรรมเสี่ยงของผู้ปกครอง/ผู้ดูแล**": [
                ("5. ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป", "ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป", "pb_rf_work_freq"),
                ("6. บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน", "บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน", "pb_rf_work_loc"),
                ("7. หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที", "หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที", "pb_rf_shower"),
                ("8. ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก", "ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก", "pb_rf_contamination"),
                ("9. ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว", "ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว", "pb_rf_feed"),
                ("10. อุ้มหรือกอดเด็กระหว่างทำงาน", "อุ้มหรือกอดเด็กระหว่างทำงาน", "pb_rf_hold"),
            ],
            "**พฤติกรรมของเด็ก**": [
                ("11. เด็กชอบอมหรือดูดนิ้วหรือไม่", "เด็กชอบอมหรือดูดนิ้วหรือไม่", "pb_rf_suck"),
                ("12. เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่", "เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่", "pb_rf_mouth"),
                ("13. ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร", "ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร", "pb_rf_handwash"),
                ("14. เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว", "เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว", "pb_rf_sleep"),
                ("15. บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว", "บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว", "pb_rf_play"),
                ("16. ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก", "ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก", "pb_rf_toys"),
            ]
        }

        for category, questions in risk_factor_questions_by_category.items():
            st.markdown(category)
            for q_label, q_dict_key, st_key in questions:
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.write(q_label)
                with col2:
                    risk_factors_data[q_dict_key] = st.radio(
                        q_label,
                        ["ใช่/มี", "ไม่ใช่/ไม่มี"],
                        horizontal=True,
                        key=st_key,
                        label_visibility="collapsed"
                    )
        
        form_data['ปัจจัยเกี่ยวข้อง'] = risk_factors_data

    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.markdown("##### ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        
        form_data['พื้น (Floors)'] = st.number_input(
            "พื้น (Floors) | ค่าอ้างอิง EPA: 10 µg/ft²", 
            min_value=0.0, 
            format="%.2f", 
            key="pb_wipe_floor"
        )
        form_data['ขอบหน้าต่าง'] = st.number_input(
            "ขอบหน้าต่าง (Window Sills) | ค่าอ้างอิง EPA: 100 µg/ft²", 
            min_value=0.0, 
            format="%.2f", 
            key="pb_wipe_sill"
        )
        form_data['รางหน้าต่าง'] = st.number_input(
            "รางหน้าต่าง (window troughs) | ค่าอ้างอิง EPA: 100 µg/ft²", 
            min_value=0.0, 
            format="%.2f", 
            key="pb_wipe_trough"
        )
        
        form_data['ข้อมูลเพิ่มเติม_สิ่งแวดล้อม'] = st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:", key="pb_env_other_info")
        form_data['ผู้สำรวจ'] = st.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):", key="pb_surveyor_name")
        form_data['เบอร์โทรผู้สำรวจ'] = st.text_input("เบอร์โทรหรือ ID Line:", key="pb_surveyor_contact")

    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา")
        symptoms_data_child = {}
        symptoms_list_child = [
            ("ปวดท้อง", "pb_symp_ปวดท้อง"),
            ("อาเจียน", "pb_symp_อาเจียน"),
            ("อ่อนเพลีย", "pb_symp_อ่อนเพลีย"),
            ("ท้องเสีย", "pb_symp_ท้องเสีย"),
            ("โลหิตจาง", "pb_symp_โลหิตจาง"),
            ("ชัก", "pb_symp_ชัก"),
            ("หมดสติ", "pb_symp_หมดสติ"),
            ("การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "pb_symp_การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์"),
            ("ระดับสติปัญญาต่ำกว่าเกณฑ์", "pb_symp_ระดับสติปัญญาต่ำกว่าเกณฑ์"),
            ("ท้องผูก", "pb_symp_ท้องผูก"),
            ("เบื่ออาหาร", "pb_symp_เบื่ออาหาร"),
            ("กระวนกระวาย/ไม่มีสมาธิ", "pb_symp_กระวนกระวายไม่มีสมาธิ"),
            ("หงุดหงิดง่าย", "pb_symp_หงุดหงิดง่าย")
        ]
        
        for symptom_label, symptom_key in symptoms_list_child:
            col1, col2 = st.columns([2, 3])
            with col1:
                st.write(symptom_label)
            with col2:
                symptoms_data_child[symptom_label] = st.radio(
                    symptom_label, 
                    ["เป็นประจำ/แทบทุกวัน", "นานๆครั้ง", "ไม่มี"], 
                    horizontal=True, 
                    key=symptom_key,
                    label_visibility="collapsed"
                )

        form_data['อาการเด็ก'] = symptoms_data_child

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        physical_exam_data = {}
        col1, col2, col3, col4 = st.columns(4)
        physical_exam_data['BP'] = col1.text_input("BP (mmHg):")
        physical_exam_data['PR'] = col2.number_input("PR (/min):", min_value=0, step=1)
        physical_exam_data['RR'] = col3.number_input("RR (/min):", min_value=0, step=1)
        physical_exam_data['BT'] = col4.number_input("BT (°C):", min_value=0.0, format="%.1f")
        
        exam_items = [
            ("General appearance", "exam_general"),
            ("HEENT: conjunctive", "exam_heent"),
            ("Lung", "exam_lung"),
            ("Abdomen", "exam_abdomen"),
            ("Skin", "exam_skin"),
            ("Hand writing", "exam_handwriting"),
            ("Gait", "exam_gait"),
            ("Sensation", "exam_sensation"),
            ("Cognition", "exam_cognition"),
            ("Mood", "exam_mood"),
            ("IQ หรือ Mentality", "exam_iq")
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

        for label, key in exam_items:
            create_exam_row(label, key)
        
        st.divider()
        st.write("7) Neuro sign: motor power grade")
        
        def create_motor_power_row(label, key_prefix):
            st.markdown(f"**{label}**")
            
            # Header Row
            h_col1, h_col2, h_col3, h_col4 = st.columns([2, 1, 2, 2])
            with h_col2:
                st.markdown("<p style='text-align: center;'><b>R</b></p>", unsafe_allow_html=True)
            with h_col3:
                st.markdown("<p style='text-align: center;'><b>L</b></p>", unsafe_allow_html=True)
        
            # Proximal Flexor
            cols = st.columns([1, 1, 2, 2])
            with cols[0]:
                st.markdown("**Proximal:**")
            with cols[1]:
                st.markdown("Flexor")
            with cols[2]:
                physical_exam_data[f'{key_prefix}_prox_flex_R'] = st.text_input(f"{key_prefix}_prox_flex_R", placeholder="/5", key=f"{key_prefix}_prox_flex_R", label_visibility="collapsed")
            with cols[3]:
                physical_exam_data[f'{key_prefix}_prox_flex_L'] = st.text_input(f"{key_prefix}_prox_flex_L", placeholder="/5", key=f"{key_prefix}_prox_flex_L", label_visibility="collapsed")
        
            # Proximal Extensor
            cols = st.columns([1, 1, 2, 2])
            with cols[1]:
                st.markdown("extensor")
            with cols[2]:
                physical_exam_data[f'{key_prefix}_prox_ext_R'] = st.text_input(f"{key_prefix}_prox_ext_R", placeholder="/5", key=f"{key_prefix}_prox_ext_R", label_visibility="collapsed")
            with cols[3]:
                physical_exam_data[f'{key_prefix}_prox_ext_L'] = st.text_input(f"{key_prefix}_prox_ext_L", placeholder="/5", key=f"{key_prefix}_prox_ext_L", label_visibility="collapsed")
                
            # Distal Flexor
            cols = st.columns([1, 1, 2, 2])
            with cols[0]:
                st.markdown("**Distal:**")
            with cols[1]:
                st.markdown("Flexor")
            with cols[2]:
                physical_exam_data[f'{key_prefix}_dist_flex_R'] = st.text_input(f"{key_prefix}_dist_flex_R", placeholder="/5", key=f"{key_prefix}_dist_flex_R", label_visibility="collapsed")
            with cols[3]:
                physical_exam_data[f'{key_prefix}_dist_flex_L'] = st.text_input(f"{key_prefix}_dist_flex_L", placeholder="/5", key=f"{key_prefix}_dist_flex_L", label_visibility="collapsed")
                
            # Distal Extensor
            cols = st.columns([1, 1, 2, 2])
            with cols[1]:
                st.markdown("extensor")
            with cols[2]:
                physical_exam_data[f'{key_prefix}_dist_ext_R'] = st.text_input(f"{key_prefix}_dist_ext_R", placeholder="/5", key=f"{key_prefix}_dist_ext_R", label_visibility="collapsed")
            with cols[3]:
                physical_exam_data[f'{key_prefix}_dist_ext_L'] = st.text_input(f"{key_prefix}_dist_ext_L", placeholder="/5", key=f"{key_prefix}_dist_ext_L", label_visibility="collapsed")
            
            st.divider()

        create_motor_power_row("(1) Upper extremities", "upper")
        create_motor_power_row("(2) Lower extremities", "lower")


        form_data['การตรวจร่างกาย'] = physical_exam_data

        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        lab_results_data = {}
        lab_results_data['ระดับตะกั่วในเลือด'] = st.number_input("ระดับตะกั่วในเลือด (µg/dL)", min_value=0.0, format="%.2f", key="lab_lead")

        other_lab_tests = ["CBC", "BUN/Cr", "SGPT/SGOT", "TB/DB", "Uric acid", "UA"]
        
        def create_lab_row(label, key):
            col1, col2 = st.columns([1,2])
            with col1:
                st.write(label)
            with col2:
                status = st.radio(label, ["ปกติ", "ผิดปกติ"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "ผิดปกติ":
                    detail = st.text_input("ระบุผล", key=f"{key}_detail", label_visibility="collapsed")
                lab_results_data[label] = f"{status}{f' ({detail})' if detail else ''}"

        for test in other_lab_tests:
            create_lab_row(test, f"lab_{test.lower()}")
            
        form_data['ผลทางห้องปฏิบัติการ'] = lab_results_data

        st.markdown("---")
        st.write("**ข้อมูลแพทย์ผู้ตรวจ**")
        col1, col2 = st.columns(2)
        form_data['แพทย์ผู้ตรวจ'] = col1.text_input("ชื่อ-นามสกุล แพทย์ผู้ตรวจร่างกาย", key="doc_name")
        form_data['เบอร์โทรแพทย์'] = col2.text_input("เบอร์โทรศัพท์", key="doc_phone")


    st.markdown("---")
    if st.button("บันทึกข้อมูล", use_container_width=True, type="primary", key="pb_submit_child_pb"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        # For debugging, you can uncomment the line below to see the collected data
        # st.write(form_data)

