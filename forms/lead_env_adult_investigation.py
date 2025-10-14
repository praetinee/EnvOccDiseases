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
        
        smoking_hist = st.radio("2.1 ประวัติการสูบบุหรี่:", ["ไม่สูบ", "เคยสูบแต่เลิกแล้ว", "สูบ/ปัจจุบันยังสูบ"])
        if smoking_hist == "เคยสูบแต่เลิกแล้ว":
            quit_years = st.number_input("เลิกมาแล้วกี่ปี:", min_value=0, step=1)
            form_data['ประวัติสูบบุหรี่'] = f"เคยสูบ (เลิกมาแล้ว {quit_years} ปี)"
        elif smoking_hist == "สูบ/ปัจจุบันยังสูบ":
            current_amount = st.number_input("วันละกี่มวน:", min_value=0, step=1)
            form_data['ประวัติสูบบุหรี่'] = f"ปัจจุบันยังสูบ ({current_amount} มวน/วัน)"
        else:
            form_data['ประวัติสูบบุหรี่'] = "ไม่สูบ"

        smoke_locs_opts = st.multiselect("2.2 สถานที่หรือบริเวณที่ท่านสูบบุหรี่:", ["ไม่สูบ", "บริเวณสถานที่ทำงาน/สูบพร้อมขณะทำงาน", "บริเวณที่จัดไว้เป็นสถานที่สูบบุหรี่", "บริเวณรับประทานอาหาร/โรงอาหาร", "อื่นๆ"])
        if "อื่นๆ" in smoke_locs_opts:
            smoke_loc_other = st.text_input("ระบุสถานที่สูบบุหรี่อื่นๆ:")
            form_data['สถานที่สูบบุหรี่'] = ", ".join(smoke_locs_opts) + f" ({smoke_loc_other})"
        else:
            form_data['สถานที่สูบบุหรี่'] = ", ".join(smoke_locs_opts)

        eating_loc_opts = st.multiselect("2.3 ท่านรับประทานอาหารในสถานที่ทำงานหรือไม่:", ["ไม่ได้รับประทาน", "รับประทานในโรงอาหาร", "รับประทานในบริเวณเดียวกับที่ปฏิบัติงาน", "อื่นๆ"])
        if "อื่นๆ" in eating_loc_opts:
            eating_loc_other = st.text_input("ระบุสถานที่รับประทานอาหารอื่นๆ:")
            form_data['สถานที่รับประทานอาหาร'] = ", ".join(eating_loc_opts) + f" ({eating_loc_other})"
        else:
            form_data['สถานที่รับประทานอาหาร'] = ", ".join(eating_loc_opts)
            
        food_source_opts = st.multiselect("2.4 แหล่งที่มาของอาหาร (ตอบได้มากกว่า 1 ข้อ):", ["ปรุง/ทำอาหารเอง", "ซื้อจากผู้ประกอบการเป็นหลัก", "อื่นๆ"])
        if "อื่นๆ" in food_source_opts:
            food_source_other = st.text_input("ระบุแหล่งที่มาของอาหารอื่นๆ:")
            form_data['แหล่งที่มาอาหาร'] = ", ".join(food_source_opts) + f" ({food_source_other})"
        else:
            form_data['แหล่งที่มาอาหาร'] = ", ".join(food_source_opts)

        water_use_opts = st.multiselect("2.5 แหล่งน้ำใช้:", ["น้ำประปา", "น้ำบาดาล", "แหล่งน้ำธรรมชาติ", "อื่นๆ"])
        processed_water_use = list(water_use_opts)
        if "แหล่งน้ำธรรมชาติ" in processed_water_use:
            coords = st.text_input("ระบุพิกัดของแหล่งน้ำธรรมชาติ:")
            if coords:
                idx = processed_water_use.index("แหล่งน้ำธรรมชาติ")
                processed_water_use[idx] = f"แหล่งน้ำธรรมชาติ (พิกัด: {coords})"
        if "อื่นๆ" in processed_water_use:
            other_text = st.text_input("ระบุแหล่งน้ำใช้อื่นๆ:")
            idx = processed_water_use.index("อื่นๆ")
            if other_text:
                processed_water_use[idx] = f"อื่นๆ ({other_text})"
            else:
                processed_water_use.pop(idx)
        form_data['แหล่งน้ำใช้'] = ", ".join(processed_water_use)

        water_drink_opts = st.multiselect("2.6 แหล่งน้ำดื่ม:", ["น้ำประปา", "น้ำซื้อ", "น้ำบาดาล", "อื่นๆ"])
        if "อื่นๆ" in water_drink_opts:
            water_drink_other = st.text_input("ระบุแหล่งน้ำดื่มอื่นๆ:")
            form_data['แหล่งน้ำดื่ม'] = ", ".join(water_drink_opts) + f" ({water_drink_other})"
        else:
            form_data['แหล่งน้ำดื่ม'] = ", ".join(water_drink_opts)

        disease_opts = st.multiselect("2.7 ประวัติโรคประจำตัว:", ["ความดันโลหิตสูง", "เบาหวาน", "โลหิตจาง", "อื่นๆ"])
        if "อื่นๆ" in disease_opts:
            disease_other = st.text_input("ระบุโรคประจำตัวอื่นๆ:")
            form_data['โรคประจำตัว'] = ", ".join(disease_opts) + f" ({disease_other})"
        else:
            form_data['โรคประจำตัว'] = ", ".join(disease_opts)

        other_history_opts = st.multiselect("2.8 ประวัติอื่นๆ:", ["ใช้ยาสมุนไพร", "การใช้แป้งทาหน้างิ้ว", "ประวัติการรับกระสุนปืน"])
        if "ใช้ยาสมุนไพร" in other_history_opts:
            herbal_med = st.text_input("ระบุยาสมุนไพร:")
            idx = other_history_opts.index("ใช้ยาสมุนไพร")
            other_history_opts[idx] = f"ใช้ยาสมุนไพร ({herbal_med})"
        form_data['ประวัติอื่นๆ'] = ", ".join(other_history_opts)

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

