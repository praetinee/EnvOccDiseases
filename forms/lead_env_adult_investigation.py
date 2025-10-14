import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Adult Investigation Form (Pb-1)"""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของผู้ใหญ่/หญิงตั้งครรภ์ในบ้านพักอาศัยและในชุมชน")
    st.caption("(แบบสอบสวน Pb-1)")
    st.info("คำชี้แจง: แบบสอบสวนโรคฉบับนี้ใช้ในการสัมภาษณ์ผู้ที่มีความเสี่ยงหรือสงสัยว่าป่วยด้วยโรคจากตะกั่วหรือสารประกอบของตะกั่ว ประกอบด้วย ข้อมูลทั้งจากการสัมภาษณ์ การสังเกต และบันทึกข้อมูลภาคสนาม")

    form_data = {}

    with st.container(border=True):
        col1, col2 = st.columns(2)
        form_data['วันที่สอบสวน'] = col1.date_input("วัน/เดือน/ปี ที่ดำเนินการสอบสวน:")
        form_data['ชื่อสถานประกอบการ'] = col2.text_input("ชื่อโรงงาน/สถานประกอบการ/สถานที่เกิดเหตุ:")
        form_data['ประเภทกิจการ'] = st.text_input("ประเภทสถานประกอบกิจการ:")

    # --- Section 1: Personal Information ---
    with st.expander("ส่วนที่ 1: ข้อมูลส่วนบุคคล", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อ-นามสกุล'] = col1.text_input("1.1 ชื่อ - นามสกุล")
        form_data['เลขบัตรประชาชน'] = col2.text_input("เลขบัตรประชาชน")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("1.2 ที่อยู่ปัจจุบัน", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด")
        form_data['เบอร์โทร'] = st.text_input("เบอร์โทร")

        st.write("1.3 อาศัยอยู่ในพื้นที่มาแล้ว:")
        col1, col2 = st.columns(2)
        res_years = col1.number_input("ปี", min_value=0, step=1, key="pb1_res_years")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="pb1_res_months")
        form_data['ระยะเวลาอาศัย'] = f"{res_years} ปี {res_months} เดือน"

        col1, col2 = st.columns(2)
        form_data['อายุ'] = col1.number_input("1.4 อายุ (ปี)", min_value=0, step=1)
        form_data['เพศ'] = col2.radio("1.5 เพศ", ["ชาย", "หญิง"], horizontal=True)
        
        col1, col2 = st.columns(2)
        marital_status = col1.selectbox("1.6 สถานภาพสมรส", ["โสด", "คู่", "หย่าร้าง/แยกกันอยู่/หม้าย", "อื่นๆ"])
        if marital_status == "อื่นๆ":
            other_marital_status = col1.text_input("ระบุ:", key="pb1_marital_other", label_visibility="collapsed")
            form_data['สถานภาพสมรส'] = other_marital_status
        else:
            form_data['สถานภาพสมรส'] = marital_status
        form_data['ระดับการศึกษา'] = col2.selectbox("1.7 ระดับการศึกษาสูงสุด", ["ไม่ได้ศึกษา", "ประถมศึกษา", "มัธยมศึกษา/ปวช.", "อนุปริญญา/ปวส.", "ปริญญาตรี", "สูงกว่าปริญญาตรี"])

        col1, col2 = st.columns(2)
        form_data['จำนวนสมาชิกในครอบครัว'] = col1.number_input("1.8 จํานวนสมาชิกในครอบครัว (คน)", min_value=0, step=1)
        form_data['จำนวนเด็ก < 7 ปี'] = col2.number_input("จำนวนเด็กอายุน้อยกว่า 7 ปี (คน)", min_value=0, step=1)

        st.subheader("กรณีเป็นหญิงตั้งครรภ์ (สอบถามเพิ่มเติม)")
        col1, col2 = st.columns(2)
        form_data['อายุครรภ์'] = col1.number_input("9. อายุครรภ์ (สัปดาห์)", min_value=0, step=1)
        form_data['ท้องคนที่'] = col2.number_input("10. ท้องคนที่", min_value=1, step=1)
        form_data['ฝากครรภ์'] = col1.text_input("11. ฝากครรภ์หรือไม่")
        form_data['ประวัติการแท้ง'] = col2.number_input("12. ประวัติการแท้ง (ครั้ง)", min_value=0, step=1)
        form_data['บุตรน้ำหนักต่ำกว่าเกณฑ์'] = st.number_input("13. บุตรน้ำหนักต่ำกว่าเกณฑ์ (คน)", min_value=0, step=1)

    # --- Section 2 & 3 (Combined for flow) ---
    with st.expander("ส่วนที่ 2 และ 3: ข้อมูลพฤติกรรมและอาชีพ", expanded=True):
        st.subheader("ส่วนที่ 2: ข้อมูลสุขภาวะและพฤติกรรมสุขภาพ")
        # This section is identical to PbC04, so it can be copied or refactored into a shared function later.
        st.info("ส่วนนี้เหมือนกับฟอร์ม PbC04 (ซักประวัติผู้ใหญ่)")
        # ... (You can copy the code from lead_env_adult_history.py Section 2 here) ...

        st.subheader("ส่วนที่ 3: ลักษณะงานและการประกอบอาชีพ")
        # ... (You can copy the code from lead_occupational.py Section 3 here) ...
        st.info("ส่วนนี้เหมือนกับฟอร์มโรคจากตะกั่ว (อาชีพ)")

    # --- Section 4: Risk Factors ---
    with st.expander("ส่วนที่ 4: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่ว", expanded=True):
        # This section is identical to lead_occupational.py Section 4
        st.info("ส่วนนี้เหมือนกับฟอร์มโรคจากตะกั่ว (อาชีพ)")
        # ... (You can copy the code from lead_occupational.py Section 4 here) ...
    
    # --- Section 5: Symptoms ---
    with st.expander("ส่วนที่ 5: ลักษณะอาการที่ส่งผลกระทบทางสุขภาพ", expanded=True):
        # This section is identical to lead_occupational.py Section 5
        st.info("ส่วนนี้เหมือนกับฟอร์มโรคจากตะกั่ว (อาชีพ)")
        # ... (You can copy the code from lead_occupational.py Section 5 here) ...

    # --- Section 6, 7, 8: Medical Info ---
    with st.expander("ส่วนที่ 6, 7, 8: ผลการตรวจ, การวินิจฉัย และการรักษา", expanded=True):
        # These sections are identical to the medical form (lead_occupational_medical.py)
        st.info("ส่วนนี้เหมือนกับแบบบันทึกการตรวจร่างกายโดยแพทย์")
        # ... (You can copy the code from lead_occupational_medical.py here) ...

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)
