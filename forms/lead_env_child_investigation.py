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
        # ... (Questions from PbC01 can be reused here if needed) ...
        st.info("ส่วนนี้สามารถนำข้อมูลจากแบบซักประวัติ (PbC01) มาใช้ได้")


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
            for factor in factors:
                form_data[factor] = st.radio(factor, ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, label_visibility="collapsed")


    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.write("ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        col1, col2 = st.columns(2)
        form_data['พื้น (Floors)'] = col1.number_input("พื้น (Floors) (µg/ft²)", min_value=0.0, format="%.2f")
        form_data['ขอบหน้าต่าง (Window Sills)'] = col2.number_input("ขอบหน้าต่าง (Window Sills) (µg/ft²)", min_value=0.0, format="%.2f")
        form_data['รางหน้าต่าง (window troughs)'] = col1.number_input("รางหน้าต่าง (window troughs) (µg/ft²)", min_value=0.0, format="%.2f")
        
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
            form_data[symptom] = st.radio(symptom, ["ไม่มี", "นานๆครั้ง", "เป็นประจำ/แทบทุกวัน"], horizontal=True)

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        # ... (Physical exam section can be added here, similar to lead_occupational_medical.py) ...
        st.info("ส่วนการตรวจร่างกายโดยแพทย์ สามารถใช้ข้อมูลจากแบบบันทึกตรวจร่างกาย (แพทย์) ได้")

        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        # ... (Lab results section can be added here, similar to lead_occupational_medical.py) ...
        st.info("ส่วนผลการตรวจทางห้องปฏิบัติการ สามารถใช้ข้อมูลจากแบบบันทึกตรวจร่างกาย (แพทย์) ได้")


    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

