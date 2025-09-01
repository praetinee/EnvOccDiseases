# -*- coding: utf-8 -*-
import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Child Investigation Form (Pb)"""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของเด็กในบ้านพักอาศัย และในชุมชน")
    st.caption("(แบบสอบสวน Pb)")

    form_data = {}

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อเด็ก'] = col1.text_input("ชื่อ ด.ช./ด.ญ.:")
        form_data['เลขบัตรประชาชน'] = col2.text_input("เลขบัตรประชาชน:")
        
        col1, col2, col3 = st.columns(3)
        form_data['วันเกิด'] = col1.date_input("วัน/เดือน/ปีเกิด:")
        form_data['น้ำหนัก'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("ชื่อผู้ปกครอง:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, เบอร์โทร")
        
        st.write("จำนวนสมาชิกในครอบครัว:")
        col1, col2 = st.columns(2)
        form_data['สมาชิกทั้งหมด'] = col1.number_input("รวม (คน)", min_value=0, step=1)
        form_data['สมาชิกเด็ก<7ปี'] = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1)

        st.subheader("ประวัติเด็ก")
        
        # 1. การศึกษาของเด็ก
        education_status = st.radio("1) การศึกษาของเด็ก:", ["ยังไม่ได้เข้าเรียน", "เข้าเรียน"])
        if education_status == "เข้าเรียน":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("ระดับ:")
                education_level = st.radio("ระดับชั้น:", ["ก่อนอนุบาล", "อนุบาล", "ประถม"], label_visibility="collapsed")
            with col2:
                st.write("ระยะเวลาที่เรียน (ปี):")
                edu_years = st.number_input("ปี", min_value=0, step=1, key="edu_years", label_visibility="collapsed")
            with col3:
                st.write("ระยะเวลาที่เรียน (เดือน):")
                edu_months = st.number_input("เดือน", min_value=0, max_value=11, step=1, key="edu_months", label_visibility="collapsed")
            form_data['การศึกษา'] = f"เข้าเรียน ระดับ {education_level} (ระยะเวลา {edu_years} ปี {edu_months} เดือน)"
        else:
            form_data['การศึกษา'] = "ยังไม่ได้เข้าเรียน"

        # 2. ระยะเวลาอาศัย
        st.write("2) เด็กอาศัยอยู่ในที่อยู่ปัจจุบันมาประมาณ:")
        col1, col2 = st.columns(2)
        res_years = col1.number_input("ปี", min_value=0, step=1, key="res_years_child")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="res_months_child")
        form_data['ระยะเวลาอาศัย'] = f"{res_years} ปี {res_months} เดือน"

        # 3. โรคประจำตัว
        comorbidity_status = st.radio("3) เด็กมีโรคประจำตัวหรือไม่:", ["ไม่มี", "มี"])
        if comorbidity_status == "มี":
            comorbidity_detail = st.text_input("ระบุโรคประจำตัว:", key="comorbidity_detail")
            form_data['โรคประจำตัว'] = f"มี ({comorbidity_detail})"
        else:
            form_data['โรคประจำตัว'] = "ไม่มี"

        # 4. ยาประจำ
        medication_opts = st.multiselect("4) เด็กรับประทานยาประจำ:", 
                                         ["ไม่ได้รับประทาน", "รับประทาน (ระบุ)", "รับประทานยาสมุนไพร (ระบุ)", "ยากวาดลิ้น"])
        
        med_details = []
        if "รับประทาน (ระบุ)" in medication_opts:
            med_regular = st.text_input("ระบุยาที่รับประทานประจำ")
            if med_regular: med_details.append(f"รับประทาน ({med_regular})")
        if "รับประทานยาสมุนไพร (ระบุ)" in medication_opts:
            med_herbal = st.text_input("ระบุยาสมุนไพร")
            if med_herbal: med_details.append(f"ยาสมุนไพร ({med_herbal})")
        if "ยากวาดลิ้น" in medication_opts:
            med_details.append("ยากวาดลิ้น")
        if "ไม่ได้รับประทาน" in medication_opts:
             med_details.append("ไม่ได้รับประทาน")
        form_data['ยาประจำ'] = ", ".join(med_details)


        # 5. อาบน้ำ
        form_data['จำนวนอาบน้ำ'] = st.number_input("5) เด็กอาบน้ำวันละกี่ครั้ง:", min_value=0, step=1)

        # 6. ดื่มนม
        form_data['การดื่มนม'] = st.radio("6) เด็กดื่มนมอะไร:", ["นมแม่อย่างเดียว", "นมกระป๋อง/นมกล่องอย่างเดียว", "ทั้งนมแม่และนมกระป๋อง/นมกล่อง"])
        
        # 7-9. การไปในที่ทำงานเกี่ยวกับตะกั่ว
        visit_workplace = st.radio("7) เด็กเคยไปบริเวณที่ทำงานเกี่ยวกับตะกั่วบ้างหรือไม่:", ["ไม่ไป", "ไป"])
        if visit_workplace == "ไป":
            form_data['ความถี่ในการไป'] = st.radio("8) เด็กไปที่บริเวณงานเกี่ยวกับตะกั่วบ่อยแค่ไหน:", ["นานๆ ไปครั้ง", "บ่อยมาก"])
            form_data['ระยะเวลาที่อยู่'] = st.radio("9) ระยะเวลาเฉลี่ยในแต่ละวันที่เด็กอยู่บริเวณงานเกี่ยวกับตะกั่ว:", ["น้อยกว่า 2 ชม.", "2 - 4 ชม.", "5 - 8 ชม.", "8 ชม. ขึ้นไป"])
        else:
            form_data['ความถี่ในการไป'] = "ไม่ไป"
            form_data['ระยะเวลาที่อยู่'] = "ไม่ไป"


    # --- Section 2: Risk Factors ---
    with st.expander("ส่วนที่ 2: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่วของเด็ก", expanded=True):
        st.subheader("2.1 อาชีพผู้ปกครอง ผู้ดูแล หรือคนที่อยู่อาศัยบ้านเดียวกับเด็ก")
        
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", 
            "หลอมตะกั่ว/กระสุน", "ทาหรือพ่นสี", "ซ่อมยานยนต์", 
            "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)", 
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]

        work_outside = st.radio("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน", ["ไม่ใช่", "ใช่"])
        if work_outside == "ใช่":
            form_data['อาชีพนอกบ้าน'] = st.multiselect("ระบุอาชีพ (นอกบ้าน):", risk_jobs_list + ["อื่นๆ"])
            form_data['ความเกี่ยวข้อง_นอกบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"])

        work_inside = st.radio("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน", ["ไม่ใช่", "ใช่"])
        if work_inside == "ใช่":
            form_data['อาชีพในบ้าน'] = st.multiselect("ระบุอาชีพ (ในบ้าน):", risk_jobs_list + ["อื่นๆ"])
            form_data['ความเกี่ยวข้อง_ในบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก (ในบ้าน):", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"])

        store_nearby = st.radio("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย)", ["ไม่มี", "มี"])
        if store_nearby == "มี":
            form_data['ร้านค้าใกล้บ้าน'] = st.multiselect("ระบุกิจการ:", risk_jobs_list + ["อื่นๆ"])

        st.subheader("2.2 แผนผังลักษณะที่อยู่อาศัย")
        st.markdown("""
        **แนวทางการวาดแผนผัง:**
        - แผนผังลักษณะที่อยู่อาศัย บริเวณที่อยู่อาศัย
        - รวมทั้งวัสดุ บ้านเก่า ทาสี ลักษณะการเก็บข้าวของเครื่องใช้ในบ้าน
        - **ให้ใส่ดาว (⭐) บริเวณที่ทำงานเกี่ยวกับตะกั่วในบ้าน**
        - ระบุบริเวณที่นอน, ที่รับประทานอาหาร
        - ระบุสถานที่จัดเก็บอุปกรณ์ที่เกี่ยวข้องกับตะกั่ว (โดยการเดินสำรวจ)
        """)
        st.warning("กรุณาวาดแผนผังในโปรแกรมอื่น แล้วอัปโหลดเป็นไฟล์รูปภาพ")
        form_data['แผนผังที่อยู่อาศัย'] = st.file_uploader("อัปโหลดรูปภาพแผนผัง", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        st.subheader("2.3 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก")
        risk_factors = {
            "เกี่ยวกับที่พักอาศัย": [
                "บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา",
                "โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น",
                "มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน",
                "สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)"
            ],
            "เกี่ยวกับพฤติกรรมเสี่ยงของผู้ปกครอง/ผู้ดูแล": [
                "ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป",
                "บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน",
                "หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที",
                "ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก",
                "ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว",
                "อุ้มหรือกอดเด็กระหว่างทำงาน"
            ],
            "พฤติกรรมของเด็ก": [
                "เด็กชอบอมหรือดูดนิ้วหรือไม่",
                "เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่",
                "ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร",
                "เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว",
                "บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว",
                "ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก"
            ]
        }
        for category, factors in risk_factors.items():
            st.markdown(f"**{category}**")
            for i, factor in enumerate(factors):
                cols = st.columns([3, 2])
                cols[0].write(factor)
                form_data[factor] = cols[1].radio(f"select_{category}_{i}", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, label_visibility="collapsed")


    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.markdown("##### ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        
        col1, col2, col3 = st.columns([2,2,1])
        col1.markdown("**จุดเก็บตัวอย่าง**")
        col2.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
        col3.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")

        with col1:
            st.markdown("<div style='height: 38px; display: flex; align-items: center;'>พื้น (Floors)</div>", unsafe_allow_html=True)
        with col2:
            form_data['พื้น (Floors)'] = st.number_input("พื้น (Floors)", min_value=0.0, format="%.2f", label_visibility="collapsed")
        with col3:
            st.markdown("<div style='height: 38px; display: flex; align-items: center; justify-content: center;'>5</div>", unsafe_allow_html=True)

        with col1:
            st.markdown("<div style='height: 38px; display: flex; align-items: center;'>ขอบหน้าต่าง (Window Sills)</div>", unsafe_allow_html=True)
        with col2:
            form_data['ขอบหน้าต่าง (Window Sills)'] = st.number_input("ขอบหน้าต่าง (Window Sills)", min_value=0.0, format="%.2f", label_visibility="collapsed")
        with col3:
            st.markdown("<div style='height: 38px; display: flex; align-items: center; justify-content: center;'>40</div>", unsafe_allow_html=True)

        with col1:
            st.markdown("<div style='height: 38px; display: flex; align-items: center;'>รางหน้าต่าง (window troughs)</div>", unsafe_allow_html=True)
        with col2:
            form_data['รางหน้าต่าง (window troughs)'] = st.number_input("รางหน้าต่าง (window troughs)", min_value=0.0, format="%.2f", label_visibility="collapsed")
        with col3:
            st.markdown("<div style='height: 38px; display: flex; align-items: center; justify-content: center;'>100</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        form_data['ข้อมูลเพิ่มเติม_สิ่งแวดล้อม'] = st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:")
        form_data['ผู้สำรวจ'] = st.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):")
        form_data['เบอร์โทรผู้สำรวจ'] = st.text_input("เบอร์โทรหรือ ID Line:")


    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา")
        symptoms = [
            "ปวดท้อง", "อาเจียน", "อ่อนเพลีย", "ท้องเสีย", "โลหิตจาง", "ชัก", "หมดสติ",
            "การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "ระดับสติปัญญาต่ำกว่าเกณฑ์",
            "ท้องผูก", "เบื่ออาหาร", "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย"
        ]
        for symptom in symptoms:
            cols = st.columns([2, 3])
            cols[0].write(symptom)
            form_data[symptom] = cols[1].radio(symptom, ["ไม่มี", "นานๆครั้ง", "เป็นประจำ/แทบทุกวัน"], horizontal=True, label_visibility="collapsed")

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        col1, col2, col3, col4 = st.columns(4)
        form_data['BP'] = col1.text_input("BP (mmHg)")
        form_data['PR'] = col2.text_input("PR (/min)")
        form_data['RR'] = col3.text_input("RR (/min)")
        form_data['BT'] = col4.text_input("BT (°C)")

        exam_items_normal_abnormal = {
            "1) General appearance": "exam_general",
            "2) HEENT: conjunctivae": "exam_heent",
            "3) Lung": "exam_lung",
            "4) Abdomen": "exam_abdomen",
            "5) Skin": "exam_skin",
            "6) Hand writing": "exam_handwriting",
            "8) Gait": "exam_gait",
            "9) Sensation": "exam_sensation",
            "10) Cognition": "exam_cognition",
            "11) Mood": "exam_mood",
            "12) IQ หรือ Mentality": "exam_iq"
        }

        for item, key in exam_items_normal_abnormal.items():
            status = st.radio(item, ["Normal", "Abnormal"], key=f"{key}_status", horizontal=True)
            if status == "Abnormal":
                detail = st.text_input("ระบุความผิดปกติ", key=f"{key}_detail")
                form_data[item] = f"Abnormal: {detail}"
            else:
                form_data[item] = "Normal"
        
        st.markdown("**7) Neuro sign: motor power grade**")
        
        def render_motor_power(extremity_name, key_prefix):
            st.markdown(f"**({extremity_name})**")
            # Proximal
            st.markdown("Proximal:")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.write("Flexor")
            with col2: form_data[f'{key_prefix}_prox_flex_r'] = st.text_input("R", key=f"{key_prefix}_pfr") + "/5"
            with col3: form_data[f'{key_prefix}_prox_flex_l'] = st.text_input("L", key=f"{key_prefix}_pfl") + "/5"
            with col1: st.write("Extensor")
            with col2: form_data[f'{key_prefix}_prox_ext_r'] = st.text_input("R", key=f"{key_prefix}_per") + "/5"
            with col3: form_data[f'{key_prefix}_prox_ext_l'] = st.text_input("L", key=f"{key_prefix}_pel") + "/5"
            # Distal
            st.markdown("Distal:")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.write("Flexor")
            with col2: form_data[f'{key_prefix}_dist_flex_r'] = st.text_input("R", key=f"{key_prefix}_dfr") + "/5"
            with col3: form_data[f'{key_prefix}_dist_flex_l'] = st.text_input("L", key=f"{key_prefix}_dfl") + "/5"
            with col1: st.write("Extensor")
            with col2: form_data[f'{key_prefix}_dist_ext_r'] = st.text_input("R", key=f"{key_prefix}_der") + "/5"
            with col3: form_data[f'{key_prefix}_dist_ext_l'] = st.text_input("L", key=f"{key_prefix}_del") + "/5"
            
        render_motor_power("1 Upper extremities", "upper")
        render_motor_power("2 Lower extremities", "lower")


        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        st.markdown("**การตรวจสารบ่งชี้ทางชีวภาพ**")
        col1, col2, col3 = st.columns([2,2,2])
        col1.markdown("ระดับตะกั่วในเลือด")
        form_data['BLL_result'] = col2.text_input("ผลการตรวจ (µg/dL)", key="bll_res")
        form_data['BLL_date'] = col3.date_input("วันที่ตรวจ", key="bll_date")

        st.markdown("**การตรวจทางห้องปฏิบัติการอื่นๆ**")
        lab_tests = ["CBC", "BUN/Cr", "SGPT/SGOT", "TB/DB", "Uric acid", "UA"]
        for test in lab_tests:
            col1, col2, col3 = st.columns([2,2,2])
            col1.markdown(test)
            form_data[f'{test}_result'] = col2.text_input("ผลการตรวจ", key=f"{test}_res")
            form_data[f'{test}_date'] = col3.date_input("วันที่ตรวจ", key=f"{test}_date")
        
        st.subheader("ข้อมูลแพทย์ผู้ตรวจ")
        form_data['แพทย์ผู้ตรวจ'] = st.text_input("ชื่อ-นามสกุล แพทย์ผู้ตรวจร่างกาย")
        form_data['เบอร์โทรแพทย์'] = st.text_input("เบอร์โทรติดต่อ")
        form_data['ID line แพทย์'] = st.text_input("ID line")
        form_data['วันที่ตรวจ'] = st.date_input("วันที่ตรวจร่างกาย")


    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

