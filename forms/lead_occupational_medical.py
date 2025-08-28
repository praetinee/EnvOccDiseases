import streamlit as st
import datetime

def render():
    """Renders the Lead Occupational Medical Examination Form."""
    
    st.header("แบบบันทึกการตรวจร่างกายโดยแพทย์")
    st.caption("สำหรับโรคจากตะกั่วหรือสารประกอบของตะกั่ว (อ้างอิงเอกสารแนบที่ 3)")

    # --- Data Collection Dictionary ---
    form_data = {}

    with st.container(border=True):
        st.subheader("Vitals")
        col1, col2, col3, col4 = st.columns(4)
        form_data['BP (mmHg)'] = col1.text_input("BP (mmHg):")
        form_data['PR (/min)'] = col2.number_input("PR (/min):", min_value=0, step=1)
        form_data['RR (/min)'] = col3.number_input("RR (/min):", min_value=0, step=1)
        form_data['BT (°C)'] = col4.number_input("BT (°C):", min_value=0.0, format="%.1f")

    with st.container(border=True):
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

    with st.container(border=True):
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
        
    with st.container(border=True):
        st.subheader("ข้อมูลแพทย์ผู้ตรวจ")
        col1, col2 = st.columns(2)
        form_data['แพทย์ผู้ตรวจ'] = col1.text_input("ชื่อ - นามสกุล แพทย์ผู้ตรวจร่างกาย:")
        form_data['เบอร์โทรแพทย์'] = col2.text_input("เบอร์โทรศัพท์:")

    st.markdown("---")
    if st.button("ประเมินผล", use_container_width=True, type="primary"):
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
