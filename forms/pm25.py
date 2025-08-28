import streamlit as st

def render():
    """Renders the PM2.5 Individual Questionnaire (PM1)."""
    
    st.header("แบบสอบถามรายบุคคลสำหรับผู้ป่วยและกลุ่มเสี่ยง")
    st.caption("(แบบฟอร์ม PM1)")

    form_data = {}

    # --- General Information Section ---
    with st.expander("ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อ-สกุล'] = col1.text_input("1. ชื่อ - สกุล")
        form_data['เพศ'] = col2.radio("2. เพศ", ["ชาย", "หญิง"], horizontal=True)

        col1, col2, col3 = st.columns(3)
        form_data['อายุ'] = col1.number_input("3. อายุ (ปี)", min_value=0, step=1)
        form_data['น้ำหนัก'] = col2.number_input("4. น้ำหนักตัว (กิโลกรัม)", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง'] = col3.number_input("5. ส่วนสูง (เซนติเมตร)", min_value=0.0, format="%.2f")
        
        form_data['ที่อยู่'] = st.text_area("6. ที่อยู่", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด")

        diseases = st.multiselect("7. โรคประจำตัว", ["หืด", "ปอดอุดกั้นเรื้อรัง", "หัวใจขาดเลือด"])
        other_disease = st.text_input("โรคประจำตัวอื่นๆ:")
        if other_disease: diseases.append(other_disease)
        form_data['โรคประจำตัว'] = ", ".join(diseases) if diseases else "ไม่มี"

        col1, col2 = st.columns(2)
        form_data['ยาที่ใช้ประจำ'] = col1.text_input("8. ยาที่ใช้ประจำ")
        form_data['การรักษา'] = col2.radio("9. การรักษา", ["ต่อเนื่อง", "ไม่ต่อเนื่อง"])

        st.write("10. ระยะเวลาที่ท่านอาศัยในพื้นที่ปัจจุบัน")
        col1, col2 = st.columns(2)
        res_years = col1.number_input("ปี", min_value=0, step=1, key="pm25_res_years")
        res_months = col2.number_input("เดือน", min_value=0, max_value=11, step=1, key="pm25_res_months")
        form_data['ระยะเวลาอาศัย'] = f"{res_years} ปี {res_months} เดือน"

        st.write("11. สถานที่ และระยะเวลาในการสัมผัสพื้นที่สีแดง ก่อนเกิดอาการ 48 ชั่วโมง")
        form_data['สถานที่สัมผัส 1'] = st.text_input("สถานที่ 1", placeholder="สถานที่, ระยะเวลา (ปี/เดือน/วัน/ชม.)")
        form_data['สถานที่สัมผัส 2'] = st.text_input("สถานที่ 2", placeholder="สถานที่, ระยะเวลา (ปี/เดือน/วัน/ชม.)")
        form_data['สถานที่สัมผัส 3'] = st.text_input("สถานที่ 3", placeholder="สถานที่, ระยะเวลา (ปี/เดือน/วัน/ชม.)")

        occ_option = st.radio("12. อาชีพหลัก", ["ทำนา/ทำสวน/ทำไร่", "ว่างงาน/ไม่มีงานทำแน่นอน", "รับจ้างทั่วไป", "ค้าขายหรือธุรกิจส่วนตัว", "อื่นๆ"])
        occ_detail = st.text_input("ระบุรายละเอียดอาชีพ:", label_visibility="collapsed")
        form_data['อาชีพหลัก'] = f"{occ_option} ({occ_detail})" if occ_option in ["รับจ้างทั่วไป", "ค้าขายหรือธุรกิจส่วนตัว", "อื่นๆ"] else occ_option

        smoking_status = st.radio("13. ท่านสูบบุหรี่หรือไม่", ["ไม่สูบ", "สูบ"])
        if smoking_status == "สูบ":
            col1, col2 = st.columns(2)
            smoke_amount = col1.number_input("ปริมาณที่สูบ (ซอง/วัน)", min_value=0.0, format="%.1f")
            smoke_years = col2.number_input("สูบมากี่ปี", min_value=0, step=1)
            form_data['การสูบบุหรี่'] = f"สูบ (ปริมาณ: {smoke_amount} ซอง/วัน, ระยะเวลา: {smoke_years} ปี)"
        else:
            form_data['การสูบบุหรี่'] = "ไม่สูบ"

        form_data['คนในบ้านสูบบุหรี่'] = st.radio("14. คนในบ้านของท่านสูบบุหรี่หรือไม่", ["ไม่สูบ", "สูบ"])
        form_data['ลักษณะที่อยู่'] = st.radio("15. ลักษณะที่อยู่ของท่านเป็นอย่างไร", ["ห้องแถวหรือทาวน์เฮาส์", "อพาร์ทเมนท์หรือคอนโด", "บ้านเดี่ยว"])

        symptoms = st.multiselect("16. อาการป่วย (เลือกได้มากกว่า 1 ข้อ)", ["หายใจลำบาก", "หายใจมีเสียงหวีด", "ไอ", "ผื่นคัน", "แน่นหน้าอก"])
        symptom_other = st.text_input("อาการป่วยอื่นๆ:")
        if symptom_other: symptoms.append(symptom_other)
        form_data['อาการป่วย'] = ", ".join(symptoms) if symptoms else "ไม่มี"

        form_data['การรักษาตามอาการ'] = st.radio("17. ท่านได้รักษาตามอาการที่เกิดขึ้นในข้อ 16 หรือไม่", ["ไม่ได้รักษา", "ไปพบแพทย์", "ซื้อยากินเอง"])

    # --- Exposure Information Section ---
    with st.expander("ข้อมูลการสัมผัส", expanded=True):
        st.write("18. การสัมผัสฝุ่นละออง/ควัน/เขม่า/เถ้า ปลิวเข้ามาในบ้านหรือบริเวณบ้านของท่าน ในระยะเวลา 48 ชั่วโมงที่ผ่านมา")
        exposures = {
            "ควันจากการสูบบุหรี่ภายในบ้าน": st.checkbox("18.1 ควันจากการสูบบุหรี่ภายในบ้าน"),
            "ควันจากการประกอบอาหาร": st.checkbox("18.2 ควันจากการประกอบอาหาร"),
            "ควันจากธูป": st.checkbox("18.3 ควันจากธูป"),
            "ฝุ่น/เขม่าควันจากปั๊มน้ำมัน": st.checkbox("18.4 ฝุ่น/เขม่าควันจากปั๊มน้ำมัน"),
            "ฝุ่น/ควันรถ จากยานพาหนะ": st.checkbox("18.5 ฝุ่น/ควันรถ จากยานพาหนะ เช่น ฝุ่นจากถนน/รถบรรทุก"),
            "ฝุ่น/ควันจากการเผาฟางข้าว/ไร่/นา/อ้อย": st.checkbox("18.6 ฝุ่น/ควันจากการเผาฟางข้าว/ไร่/นา/อ้อย"),
            "ควันจากการเผาขยะหรือเศษใบไม้": st.checkbox("18.7 ควันจากการเผาขยะหรือเศษใบไม้"),
            "ฝุ่นจากการขุดเจาะหิน": st.checkbox("18.8 ฝุ่นจากการขุดเจาะหิน"),
            "ฝุ่นจากการก่อสร้าง": st.checkbox("18.9 ฝุ่นจากการก่อสร้าง"),
        }
        col1, col2 = st.columns([1,2])
        with col1:
            exposures['ฝุ่น/ควันจากโรงงานอุตสาหกรรม'] = st.checkbox("18.10 ฝุ่น/ควันจากโรงงานอุตสาหกรรม")
        with col2:
            factory_type = st.text_input("ระบุประเภทโรงงาน:", key="factory_type")
            if exposures['ฝุ่น/ควันจากโรงงานอุตสาหกรรม']: exposures['ฝุ่น/ควันจากโรงงานอุตสาหกรรม'] = f"ใช่ (ประเภท: {factory_type})"
        
        col1, col2 = st.columns([1,2])
        with col1:
            exposures['กิจกรรมอื่นๆ'] = st.checkbox("18.11 กิจกรรมอื่นๆ ที่เกิดฝุ่น/ควัน/เขม่า/เถ้า")
        with col2:
            other_activity = st.text_input("ระบุกิจกรรม:", key="other_activity")
            if exposures['กิจกรรมอื่นๆ']: exposures['กิจกรรมอื่นๆ'] = f"ใช่ (กิจกรรม: {other_activity})"
        
        form_data['การสัมผัส'] = ", ".join([key for key, value in exposures.items() if value and value is not True])


    # --- Protection Section ---
    with st.expander("การป้องกัน", expanded=True):
        protection_opt = st.radio("19. ท่านมีวิธีป้องกันตนเองจากฝุ่น/ควัน หรือไม่", 
                                  ["ไม่ได้ป้องกัน", "อยู่ในห้อง/อาคาร เพื่อหลีกเลี่ยงการสัมผัสฝุ่น/ควัน", "ใช้หน้ากากอนามัย", "อื่นๆ"])
        protection_other = st.text_input("วิธีป้องกันอื่นๆ:")
        form_data['การป้องกัน'] = f"อื่นๆ ({protection_other})" if protection_opt == "อื่นๆ" else protection_opt

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

