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
        form_data['สมาชิกทั้งหมด'] = col1.number_input("รวม (คน)", min_value=0, step=1, key="child_total_fam")
        form_data['สมาชิกเด็ก<7ปี'] = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1, key="child_u7_fam")

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

        work_outside = st.radio("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน", ["ไม่ใช่", "ใช่"], key="work_outside_radio")
        if work_outside == "ใช่":
            selected_jobs_outside = st.multiselect("ระบุอาชีพ (นอกบ้าน):", risk_jobs_list, key="jobs_outside_select")
            other_job_outside = st.text_input("อื่นๆ (นอกบ้าน):", key="other_job_outside_text")
            if other_job_outside: selected_jobs_outside.append(other_job_outside)
            form_data['อาชีพนอกบ้าน'] = ", ".join(selected_jobs_outside)
            
            form_data['ความเกี่ยวข้อง_นอกบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="rel_outside_select")

        work_inside = st.radio("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน", ["ไม่ใช่", "ใช่"], key="work_inside_radio")
        if work_inside == "ใช่":
            selected_jobs_inside = st.multiselect("ระบุอาชีพ (ในบ้าน):", risk_jobs_list, key="jobs_inside_select")
            other_job_inside = st.text_input("อื่นๆ (ในบ้าน):", key="other_job_inside_text")
            if other_job_inside: selected_jobs_inside.append(other_job_inside)
            form_data['อาชีพในบ้าน'] = ", ".join(selected_jobs_inside)
            
            form_data['ความเกี่ยวข้อง_ในบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก (ในบ้าน):", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="rel_inside_select")

        store_nearby = st.radio("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย)", ["ไม่มี", "มี"], key="store_nearby_radio")
        if store_nearby == "มี":
            selected_stores = st.multiselect("ระบุกิจการ:", risk_jobs_list, key="stores_select")
            other_store = st.text_input("อื่นๆ (ร้านค้า):", key="other_store_text")
            if other_store: selected_stores.append(other_store)
            form_data['ร้านค้าใกล้บ้าน'] = ", ".join(selected_stores)

        st.subheader("2.2 แผนผังลักษณะที่อยู่อาศัย")
        st.markdown("""
        วาดแผนผังลักษณะที่อยู่อาศัย, บริเวณที่อยู่อาศัย, วัสดุ, บ้านเก่า, ทาสี, ลักษณะการเก็บข้าวของเครื่องใช้ในบ้าน 
        และให้ใส่ **ดาว (⭐)** บริเวณที่ทำงานเกี่ยวกับตะกั่วในบ้าน, บริเวณที่นอน, ที่รับประทานอาหาร, สถานที่จัดเก็บอุปกรณ์ที่เกี่ยวข้องกับตะกั่ว (โดยการเดินสำรวจ)
        """)
        form_data['แผนผังที่อยู่อาศัย'] = st.file_uploader("อัปโหลดรูปภาพแผนผัง", type=["png", "jpg", "jpeg"])

        st.subheader("2.3 ประวัติเด็ก")
        child_history_data = {}
        
        education_status = st.radio("1) การศึกษาของเด็ก", ["ยังไม่ได้เข้าเรียน", "เข้าเรียน"], horizontal=True)
        if education_status == "เข้าเรียน":
            education_level = st.radio("ระดับ", ["ก่อนอนุบาล", "อนุบาล", "ประถม"], horizontal=True)
            st.write("เด็กเรียนอยู่ในโรงเรียนปัจจุบันเป็นระยะเวลา:")
            col1, col2 = st.columns(2)
            edu_years = col1.number_input("ปี", min_value=0, step=1, key="edu_years_pb_invest")
            edu_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="edu_months_pb_invest")
            child_history_data['การศึกษา'] = f"เข้าเรียน ระดับ {education_level} (ระยะเวลา {edu_years} ปี {edu_months} เดือน)"
        else:
            child_history_data['การศึกษา'] = "ยังไม่ได้เข้าเรียน"

        st.write("2) เด็กอาศัยอยู่ในที่อยู่ปัจจุบันมาประมาณ")
        col1, col2 = st.columns(2)
        res_years_child = col1.number_input("ปี", min_value=0, step=1, key="res_years_child_pb_invest")
        res_months_child = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="res_months_child_pb_invest")
        child_history_data['ระยะเวลาอาศัย'] = f"{res_years_child} ปี {res_months_child} เดือน"

        chronic_disease_status = st.radio("3) เด็กมีโรคประจำตัวหรือไม่", ["ไม่มี", "มี"], horizontal=True)
        if chronic_disease_status == "มี":
            chronic_disease_detail = st.text_input("ระบุ:", key="chronic_disease_detail_pb_invest")
            child_history_data['โรคประจำตัว'] = f"มี ({chronic_disease_detail})"
        else:
            child_history_data['โรคประจำตัว'] = "ไม่มี"
        
        medication_status = st.radio("4) เด็กรัปประทานยาประจำ", ["ไม่ได้รับประทาน", "รับประทานสมุนไพร", "ยากวาดลิ้น"], horizontal=True)
        if medication_status == "ไม่ได้รับประทาน":
             child_history_data['ยาประจำ'] = "ไม่ได้รับประทาน"
        else:
             child_history_data['ยาประจำ'] = medication_status

        child_history_data['จำนวนอาบน้ำ'] = st.number_input("5) เด็กอาบน้ำวันละกี่ครั้ง", min_value=0, step=1)
        
        child_history_data['การดื่มนม'] = st.radio("6) เด็กดื่มนมอะไร", ["นมแม่อย่างเดียว", "นมกระป๋อง/นมกล่องอย่างเดียว", "ทั้งนมแม่และนมกระป๋อง/นมกล่อง"])

        visit_workplace = st.radio("7) เด็กเคยไปบริเวณที่ทำงานเกี่ยวกับตะกั่วบ้างหรือไม่", ["ไม่ไป", "ไป"], horizontal=True)
        child_history_data['เคยไปที่ทำงาน'] = visit_workplace
        if visit_workplace == "ไป":
            child_history_data['ความถี่ไปที่ทำงาน'] = st.radio("8) เด็กไปที่บริเวณงานเกี่ยวกับตะกั่วบ่อยแค่ไหน", ["นานๆ ไปครั้ง", "บ่อยมาก"], horizontal=True)
            child_history_data['ระยะเวลาอยู่ทีทำงาน'] = st.radio("9) ระยะเวลาเฉลี่ยในแต่ละวันที่เด็กอยู่บริเวณงานเกี่ยวกับตะกั่ว", ["น้อยกว่า 2 ชม.", "2 - 4 ชม.", "5 - 8 ชม.", "8 ชม. ขึ้นไป"], horizontal=True)

        form_data['ประวัติเด็ก'] = child_history_data

        st.subheader("2.4 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก")
        risk_factors_data = {}
        
        st.markdown("**เกี่ยวกับที่พักอาศัย**")
        risk_factors_data['บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา'] = st.radio("บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_paint")
        risk_factors_data['โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น'] = st.radio("โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_floor")
        risk_factors_data['มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน'] = st.radio("มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_tools")
        risk_factors_data['สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)'] = st.radio("สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_clean")

        st.markdown("**เกี่ยวกับพฤติกรรมเสี่ยงของผู้ปกครอง/ผู้ดูแล**")
        risk_factors_data['ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป'] = st.radio("ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_work_freq")
        risk_factors_data['บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน'] = st.radio("บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_work_loc")
        risk_factors_data['หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที'] = st.radio("หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_shower")
        risk_factors_data['ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก'] = st.radio("ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_contamination")
        risk_factors_data['ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว'] = st.radio("ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_feed")
        risk_factors_data['อุ้มหรือกอดเด็กระหว่างทำงาน'] = st.radio("อุ้มหรือกอดเด็กระหว่างทำงาน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_hold")

        st.markdown("**พฤติกรรมของเด็ก**")
        risk_factors_data['เด็กชอบอมหรือดูดนิ้วหรือไม่'] = st.radio("เด็กชอบอมหรือดูดนิ้วหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_suck")
        risk_factors_data['เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่'] = st.radio("เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_mouth")
        risk_factors_data['ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร'] = st.radio("ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_handwash")
        risk_factors_data['เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว'] = st.radio("เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_sleep")
        risk_factors_data['บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว'] = st.radio("บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_play")
        risk_factors_data['ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก'] = st.radio("ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_toys")
        
        form_data['ปัจจัยเกี่ยวข้อง'] = risk_factors_data


    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.markdown("##### ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        
        col1, col2, col3 = st.columns([2,2,1])
        col1.markdown("**จุดเก็บตัวอย่าง**")
        col2.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
        col3.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")

        with col1:
            st.markdown("พื้น (Floors)")
        with col2:
            form_data['พื้น (Floors)'] = st.number_input("พื้น (Floors)", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_floor")
        with col3:
            st.markdown("5")

        with col1:
            st.markdown("ขอบหน้าต่าง (Window Sills)")
        with col2:
            form_data['ขอบหน้าต่าง (Window Sills)'] = st.number_input("ขอบหน้าต่าง (Window Sills)", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_sill")
        with col3:
            st.markdown("40")

        with col1:
            st.markdown("รางหน้าต่าง (window troughs)")
        with col2:
            form_data['รางหน้าต่าง (window troughs)'] = st.number_input("รางหน้าต่าง (window troughs)", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_trough")
        with col3:
            st.markdown("100")
        
        st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:", key="env_other_info")
        form_data['ผู้สำรวจ'] = st.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):", key="surveyor_name")
        form_data['เบอร์โทรผู้สำรวจ'] = st.text_input("เบอร์โทรหรือ ID Line:", key="surveyor_contact")


    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา")
        symptoms_data_child = {}
        symptoms_list_child = [
            "ปวดท้อง", "อาเจียน", "อ่อนเพลีย", "ท้องเสีย", "โลหิตจาง", "ชัก", "หมดสติ",
            "การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "ระดับสติปัญญาต่ำกว่าเกณฑ์",
            "ท้องผูก", "เบื่ออาหาร", "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย"
        ]
        for symptom in symptoms_list_child:
            symptoms_data_child[symptom] = st.radio(symptom, ["เป็นประจำหรือแทบทุกวัน", "นาน ๆ ครั้ง", "ไม่มี"], horizontal=True, key=f"symp_child_{symptom}")
        form_data['อาการเด็ก'] = symptoms_data_child

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        # Reuse structure from lead_occupational_medical form
        # This part can be refactored into a shared function if needed
        st.info("ส่วนการตรวจร่างกายโดยแพทย์ สามารถใช้ข้อมูลจากแบบบันทึกตรวจร่างกาย (แพทย์) ได้")
        
        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        st.info("ส่วนผลการตรวจทางห้องปฏิบัติการ สามารถใช้ข้อมูลจากแบบบันทึกตรวจร่างกาย (แพทย์) ได้")

    st.markdown("---")
    if st.button("บันทึกข้อมูล", use_container_width=True, type="primary", key="submit_child_pb"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

