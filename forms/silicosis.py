# -*- coding: utf-8 -*-
import streamlit as st
import datetime
import pandas as pd

def render():
    """Renders the Silicosis and Asbestosis Investigation Form."""
    
    st.header("แบบสอบสวนโรคซิลิโคสิสและโรคจากแอสเบสตอส")
    st.caption("โปรดทำเครื่องหมาย ☑ ลงในช่อง ☐ และเติมข้อความลงในช่องว่าง")

    form_data = {}

    # --- Section 1: General Information ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อ-สกุล'] = col1.text_input("ชื่อ - สกุล")
        form_data['เลขบัตรประชาชน'] = col2.text_input("เลขบัตรประชาชน")
        
        col1, col2, col3, col4 = st.columns(4)
        form_data['HN'] = col1.text_input("H.N.")
        form_data['เพศ'] = col2.radio("เพศ", ["ชาย", "หญิง"], horizontal=True)
        form_data['สัญชาติ'] = col3.text_input("สัญชาติ")
        form_data['อายุ'] = col4.number_input("อายุ (ปี)", min_value=0, step=1)

        form_data['ที่อยู่ขณะป่วย'] = st.text_input("ที่อยู่ขณะป่วย", placeholder="บ้านเลขที่ หมู่ที่ ตำบล อำเภอ จังหวัด")

        diseases = st.multiselect(
            "ท่านมีโรคประจำตัวหรือไม่",
            ["ไม่มี", "ปอดอุดกั้นเรื้อรัง", "หอบหืด", "วัณโรค", "อื่นๆ"]
        )
        
        other_disease_text = ""
        if "อื่นๆ" in diseases:
            other_disease_text = st.text_input("โรคประจำตัวอื่นๆ (โปรดระบุ):")
        
        # Combine selected diseases and the "other" text input
        final_diseases = []
        for disease in diseases:
            if disease != "อื่นๆ":
                final_diseases.append(disease)
        if other_disease_text:
            final_diseases.append(other_disease_text)

        form_data['โรคประจำตัว'] = ", ".join(final_diseases)


        form_data['ยาที่ใช้ประจำ'] = st.text_input("ยาที่ใช้ประจำ")
        
        treatment_status = st.radio("การรักษาโรคประจำตัว", ["ไม่ต่อเนื่อง", "ต่อเนื่อง (พบแพทย์ตามนัด)"])
        if treatment_status == "ต่อเนื่อง (พบแพทย์ตามนัด)":
            hospital = st.text_input("ปัจจุบันรักษาที่โรงพยาบาล:")
            form_data['การรักษาโรคประจำตัว'] = f"ต่อเนื่อง (รพ.: {hospital})"
        else:
            form_data['การรักษาโรคประจำตัว'] = "ไม่ต่อเนื่อง"

        smoking_status = st.radio("ท่านสูบบุหรี่หรือยาเส้นหรือไม่", ["ไม่สูบ", "สูบ", "เคยสูบแต่เลิกแล้ว"])
        if smoking_status == "สูบ":
            col1, col2 = st.columns(2)
            amount = col1.number_input("สูบวันละ (มวน)", min_value=0, step=1)
            years = col2.number_input("สูบมา (ปี)", min_value=0, step=1)
            form_data['การสูบบุหรี่'] = f"สูบ ({amount} มวน/วัน, {years} ปี)"
        elif smoking_status == "เคยสูบแต่เลิกแล้ว":
            col1, col2 = st.columns(2)
            amount = col1.number_input("เคยสูบวันละ (มวน)", min_value=0, step=1)
            years = col2.number_input("เลิกมา (ปี)", min_value=0, step=1)
            form_data['การสูบบุหรี่'] = f"เคยสูบ ({amount} มวน/วัน, เลิกมา {years} ปี)"
        else:
            form_data['การสูบบุหรี่'] = "ไม่สูบ"
        
        form_data['เคยตรวจสุขภาพประจำปี'] = st.radio("ท่านเคยตรวจสุขภาพประจำปีหรือไม่", ["ไม่เคย", "เคย"])
        
        xray_status = st.radio("ท่านเคยถ่ายภาพรังสีทรวงอกหรือไม่", ["ไม่เคย", "ไม่แน่ใจ", "เคย"])
        if xray_status == "เคย":
            xray_result = st.radio("ผลตรวจ X-ray", ["ปกติ", "ผิดปกติ"])
            xray_detail = st.text_input("ระบุผล X-ray:")
            form_data['ผลถ่ายภาพรังสีทรวงอก'] = f"เคย (ผล: {xray_result} - {xray_detail})"
        
        pft_status = st.radio("ท่านเคยตรวจสมรรถภาพปอดหรือไม่", ["ไม่เคย", "ไม่แน่ใจ", "เคย"])
        if pft_status == "เคย":
            pft_result = st.radio("ผลตรวจสมรรถภาพปอด", ["ปกติ", "ผิดปกติ"])
            pft_detail = st.text_input("ระบุผลตรวจสมรรถภาพปอด:")
            form_data['ผลตรวจสมรรถภาพปอด'] = f"เคย (ผล: {pft_result} - {pft_detail})"

    # --- Section 2: Work Information ---
    with st.expander("ส่วนที่ 2: ข้อมูลเกี่ยวกับการทำงาน", expanded=True):
        col1, col2 = st.columns(2)
        form_data['อาชีพปัจจุบัน'] = col1.text_input("อาชีพปัจจุบัน")
        form_data['ลักษณะงานปัจจุบัน'] = col2.text_input("ลักษณะงานที่ท่านทำ")
        form_data['สถานที่ทำงานปัจจุบัน'] = col1.text_input("ชื่อสถานที่ทำงาน")
        form_data['ที่ตั้งสถานที่ทำงาน'] = col2.text_input("ที่ตั้ง")
        form_data['ระยะเวลาทำงานปัจจุบัน (ปี)'] = col1.number_input("ระยะเวลาทำงาน (ปี)", min_value=0, step=1)
        form_data['การสัมผัสฝุ่น/แร่ใยหินปัจจุบัน'] = col2.radio("สัมผัสฝุ่น/แร่ใยหินหรือไม่", ["ไม่สัมผัส", "สัมผัส"])

        st.write("ประวัติการทำงานในอดีต (โปรดระบุทุกงานที่เคยทำ)")
        
        # Create an editable table for work history
        if 'work_history' not in st.session_state:
            st.session_state.work_history = pd.DataFrame([
                {"ชื่อและที่ตั้งสถานที่ทำงาน": "", "ประเภทการผลิต": "", "ลักษณะงานที่ทำ": "", "ระยะเวลา (ปี)": 0, "สัมผัสฝุ่น/แร่ใยหิน": False},
            ])
        
        edited_df = st.data_editor(st.session_state.work_history, num_rows="dynamic")
        form_data['ประวัติการทำงาน'] = edited_df.to_dict('records')

        use_ppe = st.radio("ขณะปฏิบัติงานท่านมีการใช้อุปกรณ์ป้องกันอันตรายส่วนบุคคลหรือไม่", ["ไม่ใช้", "ใช้"])
        if use_ppe == "ใช้":
            mask_types = st.multiselect(
                "กรณีใช้หน้ากาก ใช้หน้ากากชนิดใด",
                ["หน้ากาก N95", "หน้ากากผ้า", "หน้ากากอนามัย", "หน้ากากชนิดมีไส้กรอง (canister)"]
            )
            mask_other = st.text_input("หน้ากากอื่นๆ:")
            if mask_other: mask_types.append(mask_other)
            form_data['ชนิดหน้ากาก'] = ", ".join(mask_types)

            form_data['การสวมหน้ากาก'] = st.radio("ใช้ครอบทั้งปากและจมูกหรือไม่", ["ไม่ครอบ", "ครอบ"])
            
            mask_duration_opt = st.radio("ระยะเวลาในการใส่หน้ากาก", ["ไม่ใส่", "ใส่ตลอดระยะเวลาการทำงาน", "ใส่บางครั้ง"])
            if mask_duration_opt == "ใส่บางครั้ง":
                duration = st.number_input("ระบุชั่วโมง/วัน", min_value=0)
                form_data['ระยะเวลาใส่หน้ากาก'] = f"ใส่บางครั้ง ({duration} ชั่วโมง/วัน)"
            else:
                form_data['ระยะเวลาใส่หน้ากาก'] = mask_duration_opt
        else:
            form_data['การใช้อุปกรณ์ป้องกัน'] = "ไม่ใช้"

    # --- Section 3: Illness and Treatment ---
    with st.expander("ส่วนที่ 3: การป่วยและการรักษา", expanded=True):
        symptoms = st.multiselect(
            "16. ในระยะเวลา 3 เดือนที่ผ่านมา ท่านมีอาการผิดปกติเหล่านี้หรือไม่",
            ["หอบเหนื่อย", "หายใจมีเสียงหวีด", "เจ็บหน้าอก", "ไข้", "อ่อนเพลีย", "ไอเรื้อรัง (ตั้งแต่ 8 สัปดาห์ขึ้นไป)", "มีเสมหะ", "ไอปนเลือด"]
        )
        symptom_other = st.text_input("อาการอื่นๆ:")
        if symptom_other: symptoms.append(symptom_other)
        form_data['อาการผิดปกติ'] = ", ".join(symptoms)

        st.write("17. ผลการตรวจร่างกายโดยแพทย์")
        form_data['ผลตรวจระบบทางเดินหายใจ'] = st.text_area("ระบบทางเดินหายใจ:")
        form_data['ผลตรวจระบบอื่นๆ'] = st.text_area("ระบบอื่นๆ:")

        st.write("18. ผลการตรวจทางห้องปฏิบัติการ")
        col1, col2 = st.columns(2)
        xray_date = col1.date_input("18.1 ภาพถ่ายรังสีทรวงอก เมื่อวันที่:")
        xray_result = col2.text_area("ผลการตรวจ:", key="xray_result_detail")
        form_data['ผลภาพถ่ายรังสีทรวงอก'] = f"วันที่ {xray_date}: {xray_result}"
        
        ct_date = col1.date_input("18.2 ภาพถ่ายรังสีคอมพิวเตอร์ทรวงอก (CT scan) เมื่อวันที่:")
        ct_result = col2.text_area("ผลการตรวจ:", key="ct_result_detail")
        form_data['ผล CT scan'] = f"วันที่ {ct_date}: {ct_result}"
        
        pft_date = col1.date_input("18.3 การตรวจสมรรถภาพปอด เมื่อวันที่:")
        pft_result = col2.text_area("ผลการตรวจ:", key="pft_result_detail")
        form_data['ผลตรวจสมรรถภาพปอด (ละเอียด)'] = f"วันที่ {pft_date}: {pft_result}"

        form_data['การตรวจอื่นๆ'] = st.text_area("18.4 การตรวจอื่นๆ (ระบุชนิดและผลการตรวจ):")
        
        col1, col2 = st.columns(2)
        form_data['ผลการวินิจฉัย'] = col1.text_input("19. ผลการวินิจฉัยโดยแพทย์")
        form_data['การรักษา'] = col2.text_input("20. การรักษา")
        form_data['ผลการรักษา'] = st.radio("21. ผลการรักษา", ["ดีขึ้น/พักที่บ้าน", "นอนโรงพยาบาล", "ส่งต่อ", "เสียชีวิต", "อื่นๆ"])

    # --- Recorder Information ---
    with st.expander("ผู้บันทึกข้อมูล", expanded=True):
        col1, col2, col3 = st.columns(3)
        form_data['ผู้บันทึก'] = col1.text_input("ชื่อ - สกุล ผู้บันทึก")
        form_data['เบอร์โทรผู้บันทึก'] = col2.text_input("เบอร์ติดต่อ")
        form_data['วันที่บันทึก'] = col3.date_input("วันที่บันทึก", datetime.date.today())

    st.markdown("---")
    if st.button("ส่งข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกส่งเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)
