import streamlit as st
import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd

def render():
    """Renders the Lead Environmental Child Investigation Form (Pb)"""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของเด็กในบ้านพักอาศัย และในชุมชน")
    st.caption("(แบบสอบสวน Pb)")

    form_data = {}

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อเด็ก'] = col1.text_input("ชื่อ ด.ช./ด.ญ.:", key="pb_child_name")
        form_data['เลขบัตรประชาชนเด็ก'] = col2.text_input("เลขบัตรประชาชน:", key="pb_child_id")
        
        col1, col2, col3 = st.columns(3)
        form_data['วันเกิด'] = col1.date_input("วัน/เดือน/ปีเกิด:", key="pb_child_dob")
        form_data['น้ำหนัก (กก.)'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f", key="pb_child_weight")
        form_data['ส่วนสูง (ซม.)'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f", key="pb_child_height")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("ชื่อผู้ปกครอง:", key="pb_parent_name")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, เบอร์โทร", key="pb_address")
        
        st.write("จำนวนสมาชิกในครอบครัว:")
        col1, col2 = st.columns(2)
        fam_total = col1.number_input("รวม (คน)", min_value=0, step=1, key="pb_fam_total")
        fam_children = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1, key="pb_fam_children")
        form_data['จำนวนสมาชิกในครอบครัว'] = f"รวม: {fam_total} คน, เด็ก < 7 ปี: {fam_children} คน"

        st.subheader("ประวัติเด็ก")
        # ... (Same as lead_env_child_history.py Section 2) ...

    # --- Section 2: Risk Factors ---
    with st.expander("ส่วนที่ 2: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่วของเด็ก", expanded=True):
        st.subheader("2.1 อาชีพผู้ปกครอง ผู้ดูแล หรือคนที่อยู่อาศัยบ้านเดียวกับเด็ก")
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)",
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]

        work_outside = st.checkbox("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน")
        if work_outside:
            work_outside_types = st.multiselect("ระบุอาชีพ (นอกบ้าน):", risk_jobs_list, key="work_outside_types")
            work_outside_other = st.text_input("อาชีพอื่นๆ (นอกบ้าน):", key="work_outside_other")
            if work_outside_other: work_outside_types.append(work_outside_other)
            work_outside_relation = st.multiselect("ความเกี่ยวข้องกับเด็ก (นอกบ้าน):", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="work_outside_relation")
            form_data['ทำงานนอกบ้าน'] = f"ใช่ (อาชีพ: {', '.join(work_outside_types)}, เกี่ยวข้องเป็น: {', '.join(work_outside_relation)})"
        
        work_inside = st.checkbox("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน")
        if work_inside:
            # ... (similar structure as work_outside) ...
            pass

        store_nearby = st.checkbox("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากบริเวณที่อยู่อาศัย)")
        if store_nearby:
            # ... (similar structure as work_outside) ...
            pass
        
        st.subheader("แผนผังลักษณะที่อยู่อาศัย")
        st.info("คุณสามารถอัปโหลดรูปภาพแผนผังที่วาดไว้ หรือวาดแผนผังเบื้องต้นได้ที่นี่")
        
        uploaded_files = st.file_uploader(
            "อัปโหลดรูปภาพแผนผัง (สูงสุด 5 รูป):", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True
        )
        if uploaded_files:
            st.image(uploaded_files, width=150)

        st.write("2.3 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก:")
        factors = {
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
        for category, items in factors.items():
            st.markdown(f"**{category}**")
            for item in items:
                form_data[f'ปัจจัย: {item}'] = st.radio(item, ["ไม่ใช่/ไม่มี", "ใช่/มี"], horizontal=True, key=f"factor_{item}")

    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.info("ผลการตรวจวัดสภาพแวดล้อม ระดับฝุ่นตะกั่วในบ้าน หรือสถานที่เกี่ยวข้อง (เก็บด้วย Wipe technique กรณีพบความเสี่ยงปานกลาง หรือสูง)")
        col1, col2, col3 = st.columns(3)
        col1.markdown("**จุดเก็บตัวอย่าง**")
        col2.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
        col3.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")
        
        col1.write("พื้น (Floors)")
        form_data['วัดค่าพื้น'] = col2.number_input("Floors", label_visibility="collapsed", key="wipe_floor")
        col3.metric(label="Ref.", value="5")

        col1.write("ขอบหน้าต่าง (Window Sills)")
        form_data['วัดค่าขอบหน้าต่าง'] = col2.number_input("Window Sills", label_visibility="collapsed", key="wipe_sill")
        col3.metric(label="Ref.", value="40")

        col1.write("รางหน้าต่าง (window troughs)")
        form_data['วัดค่ารางหน้าต่าง'] = col2.number_input("Window Troughs", label_visibility="collapsed", key="wipe_trough")
        col3.metric(label="Ref.", value="100")
        
        form_data['ข้อมูลเพิ่มเติม (สิ่งแวดล้อม)'] = st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:")
        col1, col2 = st.columns(2)
        form_data['ผู้สำรวจ'] = col1.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):")
        form_data['เบอร์โทรผู้สำรวจ'] = col2.text_input("เบอร์โทรหรือ ID Line:")

    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา:")
        symptoms = [
            "ปวดท้อง", "อาเจียน", "อ่อนเพลีย", "ท้องเสีย", "โลหิตจาง", "ชัก", "หมดสติ",
            "การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "ระดับสติปัญญาต่ำกว่าเกณฑ์",
            "ท้องผูก", "เบื่ออาหาร", "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย"
        ]
        symptom_options = ["ไม่มี", "นานๆครั้ง", "เป็นประจำ/แทบทุกวัน"]
        for symptom in symptoms:
            form_data[f'อาการเด็ก: {symptom}'] = st.radio(symptom, symptom_options, horizontal=True, key=f"child_symptom_{symptom}")

        st.subheader("4.2 การตรวจร่างกายตามระบบ:")
        # ... (Physical exam section from lead_occupational_medical can be copied here) ...

        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ:")
        # ... (Lab results section from lead_occupational_medical can be copied here) ...
        
    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)
