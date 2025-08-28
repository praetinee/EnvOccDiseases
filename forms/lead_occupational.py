import streamlit as st
import datetime

def render():
    """Renders the Lead Occupational Investigation Form using Streamlit widgets."""
    
    st.header("แบบสอบสวนโรคจากตะกั่ว (จากการประกอบอาชีพ)")
    st.caption("สำหรับกลุ่มงานอาชีวเวชกรรม (อ้างอิงเอกสารแนบที่ 1 หน้า 30-33)")

    with st.form("lead_occupational_form"):
        # --- General Information Section ---
        with st.expander("ข้อมูลทั่วไป", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("วัน/เดือน/ปี ที่ดำเนินการสอบสวน:", datetime.date.today(), key="occ_date")
                st.text_input("ชื่อโรงงาน/สถานประกอบการ/สถานที่เกิดเหตุ:", key="occ_company_name")
            with col2:
                st.text_input("ประเภทสถานประกอบกิจการ:", key="occ_company_type")

        # --- Section 1: Personal Information ---
        with st.expander("ส่วนที่ 1: ข้อมูลส่วนบุคคล", expanded=True):
            st.text_input("1.1 ชื่อ - นามสกุล:", key="occ_fullname")
            st.text_area("1.2 ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด", key="occ_address")
            
            st.write("1.3 อาศัยอยู่ในพื้นที่มาแล้ว:")
            col1, col2 = st.columns(2)
            col1.number_input("ปี", min_value=0, step=1, key="occ_residence_years")
            col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="occ_residence_months")

            col1, col2 = st.columns(2)
            col1.number_input("1.4 อายุ (ปี):", min_value=0, step=1, key="occ_age")
            col2.radio("1.5 เพศ:", ["ชาย", "หญิง"], key="occ_gender", horizontal=True)

            col1, col2 = st.columns(2)
            with col1:
                st.radio("1.6 สถานภาพสมรส:", 
                         ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"], 
                         key="occ_marital_status")
                st.text_input("อื่นๆ (โปรดระบุ):", key="occ_marital_status_other")
            with col2:
                st.selectbox("1.7 ระดับการศึกษาสูงสุด:",
                             ["-- เลือก --", "ไม่ได้ศึกษา", "ประถมศึกษา", "มัธยมศึกษา/ปวช.", 
                              "อนุปริญญา/ปวส.", "ปริญญาตรี", "สูงกว่าปริญญาตรี"], 
                             key="occ_education")

            st.write("1.8 จํานวนสมาชิกในครอบครัว:")
            col1, col2 = st.columns(2)
            col1.number_input("รวมทั้งหมด (คน)", min_value=0, step=1, key="occ_family_total")
            col2.number_input("เด็กอายุ < 7 ปี (คน)", min_value=0, step=1, key="occ_family_children")

        # --- Section 2: Health and Behavior ---
        with st.expander("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ", expanded=True):
            st.radio("2.1 ประวัติการสูบบุหรี่:",
                     ["ไม่สูบ", "เคยสูบแต่เลิกแล้ว", "ปัจจุบันยังสูบ"],
                     key="occ_smoking_history")
            col1, col2 = st.columns([1,2])
            with col1:
                st.number_input("เลิกมาแล้ว (ปี)", min_value=0, step=1, key="occ_smoking_quit_years")
            with col2:
                st.number_input("ปัจจุบันยังสูบ (มวน/วัน)", min_value=0, step=1, key="occ_smoking_current_amount")
            
            st.multiselect("2.2 สถานที่หรือบริเวณที่ท่านสูบบุหรี่:",
                           ["ไม่สูบ", "บริเวณสถานที่ทำงาน/สูบพร้อมขณะทำงาน", "บริเวณที่จัดไว้", 
                            "บริเวณรับประทานอาหาร/โรงอาหาร", "อื่นๆ"],
                           key="occ_smoking_place")
            st.text_input("อื่นๆ (โปรดระบุ):", key="occ_smoking_place_other")

            st.radio("2.3 ท่านรับประทานอาหารในสถานที่ทํางานหรือไม่:",
                     ["ไม่ได้รับประทาน", "รับประทานในบริเวณเดียวกับที่ปฏิบัติงาน", "รับประทานในโรงอาหาร", "อื่นๆ"],
                     key="occ_eating_place")
            st.text_input("อื่นๆ (โปรดระบุ):", key="occ_eating_place_other")

            st.multiselect("2.4 แหล่งที่มาของอาหาร (ตอบได้มากกว่า 1 ข้อ):",
                           ["ปรุง/ทำอาหารเอง", "ซื้อจากผู้ประกอบการเป็นหลัก", "อื่นๆ"],
                           key="occ_food_source")
            st.text_input("อื่นๆ (โปรดระบุ):", key="occ_food_source_other")

            st.radio("2.5 แหล่งน้ำดื่ม:",
                     ["น้ำประปา", "น้ำซื้อ", "นายจ้างจัดให้", "อื่นๆ"],
                     key="occ_water_source")
            st.text_input("อื่นๆ (โปรดระบุ):", key="occ_water_source_other")

            st.multiselect("2.6 ประวัติโรคประจําตัว:",
                           ["ไม่มี", "ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง", "อื่นๆ"],
                           key="occ_chronic_disease")
            st.text_input("อื่นๆ (โปรดระบุ):", key="occ_chronic_disease_other")

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
                st.radio(symptom, symptom_options, key=f"occ_symptom_{symptom.replace(' ', '_')}", horizontal=True)

        # --- Submitter Information ---
        with st.expander("ข้อมูลผู้บันทึก", expanded=True):
            col1, col2 = st.columns(2)
            col1.text_input("ผู้บันทึกข้อมูล ชื่อ:", key="occ_recorder_name")
            col2.text_input("เบอร์ติดต่อ:", key="occ_recorder_phone")

        # --- Form Submission ---
        submitted = st.form_submit_button("บันทึกข้อมูล")
        if submitted:
            # In a real app, you would process the data from st.session_state here
            st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว!")
            st.balloons()
