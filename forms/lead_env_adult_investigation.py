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
        col1, col2 = st.columns([3, 1])
        job_current = col1.text_input("3.1 อาชีพปัจจุบัน คือ")
        job_current_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_current_years")
        form_data['อาชีพปัจจุบัน'] = f"{job_current} ({job_current_years} ปี)"

        form_data['ลักษณะงานปัจจุบัน'] = st.text_input("3.2 ลักษณะงาน/ตำแหน่งงาน/แผนกที่ทำงานปัจจุบัน")

        st.write("3.3 ระยะเวลาที่ทำงานต่อวัน")
        col1, col2 = st.columns(2)
        work_hours = col1.number_input("ชั่วโมง/วัน", min_value=0, step=1, key="work_hours")
        work_days = col2.number_input("และกี่วันต่อสัปดาห์ (วัน/สัปดาห์)", min_value=0, step=1, key="work_days")
        form_data['ระยะเวลาทำงาน'] = f"{work_hours} ชม./วัน, {work_days} วัน/สัปดาห์"

        col1, col2 = st.columns([3, 1])
        job_previous = col1.text_input("3.4 อาชีพเดิมก่อนมาทำงานปัจจุบัน คือ")
        job_previous_years = col2.number_input("ทำมาแล้วกี่ปี", min_value=0, step=1, key="job_prev_years")
        form_data['อาชีพเดิม'] = f"{job_previous} ({job_previous_years} ปี)"

    # --- Section 4: Risk Factors ---
    with st.expander("ส่วนที่ 4: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่ว", expanded=True):
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)",
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ", "อื่นๆ"
        ]
        
        risk_jobs_household = st.multiselect("4.1 ปัจจุบันท่านหรือสมาชิกในบ้านมีผู้ใดประกอบอาชีพหรือทำงานในโรงงาน/สถานประกอบการ ต่อไปนี้หรือไม่ (ตอบได้มากกว่า 1 ข้อ):", risk_jobs_list)
        if "อื่นๆ" in risk_jobs_household:
            risk_jobs_household_other = st.text_input("ระบุอาชีพเสี่ยงอื่นๆ:")
            form_data['อาชีพเสี่ยงในครัวเรือน'] = ", ".join(risk_jobs_household) + f" ({risk_jobs_household_other})"
        else:
            form_data['อาชีพเสี่ยงในครัวเรือน'] = ", ".join(risk_jobs_household)

        risk_places_nearby = st.multiselect("4.2 โรงงาน/สถานประกอบการ/ร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย):", risk_jobs_list, key="risk_places")
        if "อื่นๆ" in risk_places_nearby:
            risk_places_nearby_other = st.text_input("ระบุสถานประกอบการเสี่ยงอื่นๆ:")
            form_data['สถานประกอบการเสี่ยงใกล้ที่พัก'] = ", ".join(risk_places_nearby) + f" ({risk_places_nearby_other})"
        else:
            form_data['สถานประกอบการเสี่ยงใกล้ที่พัก'] = ", ".join(risk_places_nearby)

        st.write("4.3 ท่านใช้อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลระหว่างการทำงานหรือไม่ เพื่อป้องกันอันตรายจากการทำงาน")
        
        ppe_items = [
            "ถุงมือยาง/หนัง", "หมวก/ผ้าคลุมผม", "หน้ากากป้องกันฝุ่น/ผ้าปิดจมูก",
            "แว่นตา", "รองเท้าบูธ/ผ้าใบ", "เสื้อแขนยาว", "กางเกงขายาว"
        ]
        ppe_options = ["ใช้ทุกครั้ง", "ใช้บางครั้ง", "ไม่ใช้"]

        for item in ppe_items:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(item)
            with col2:
                selection = st.radio(
                    item, 
                    options=ppe_options,
                    key=f"ppe_{item.replace('/', '_')}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                form_data[f"PPE: {item}"] = selection

        # Handle "Other" item separately
        col1, col2 = st.columns([1, 2])
        with col1:
             other_ppe_name = st.text_input("อื่นๆ:", placeholder="ระบุอุปกรณ์...")
        with col2:
            if other_ppe_name:
                other_ppe_selection = st.radio(
                    other_ppe_name,
                    options=ppe_options,
                    key="ppe_other_item_radio",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                form_data[f"PPE: {other_ppe_name}"] = other_ppe_selection
                
        ppe_source_opts = st.multiselect("4.4 อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลที่ท่านใช้ ได้มาจากอะไร (ตอบได้มากกว่า 1 ข้อ)", ["ซื้อเอง", "ได้รับจากโรงงาน/บริษัท", "แหล่งอื่นๆ"])
        if "แหล่งอื่นๆ" in ppe_source_opts:
            ppe_source_other = st.text_input("ระบุแหล่งอื่นๆ:")
            form_data['แหล่งที่มาอุปกรณ์'] = ", ".join(ppe_source_opts) + f" ({ppe_source_other})"
        else:
            form_data['แหล่งที่มาอุปกรณ์'] = ", ".join(ppe_source_opts)

        form_data['ที่เก็บอุปกรณ์'] = st.radio("4.5 ท่านเก็บอุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลไว้ที่ใด", ["บ้าน", "ที่ทำงาน"])
        
        storage_opts = st.multiselect("4.6 ท่านมีการจัดเก็บรักษาอุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคลหลังจาการใช้งานอย่างไร", ["ตามพื้น/ผนังห้องภายในบ้าน", "ล็อกเกอร์หรือตู้เก็บเฉพาะ", "อื่นๆ"])
        if "อื่นๆ" in storage_opts:
            storage_other = st.text_input("ระบุวิธีจัดเก็บอื่นๆ:")
            form_data['วิธีจัดเก็บอุปกรณ์'] = ", ".join(storage_opts) + f" ({storage_other})"
        else:
            form_data['วิธีจัดเก็บอุปกรณ์'] = ", ".join(storage_opts)

        st.write("4.7 พฤติกรรมด้านสุขลักษณะและความปลอดภัยในการทำงาน")
        hygiene_items = ["ล้างมือก่อนรับประทานอาหาร", "อาบน้ำก่อนออกจากสถานที่ทำงาน", "เปลี่ยนเสื้อผ้าก่อนออกจากที่ปฏิบัติงาน", "เปลี่ยนรองเท้าก่อนออกจากสถานที่ทำงาน", "นำหรือสวมเสื้อผ้าที่ปนเปื้อนกลับบ้าน"]
        hygiene_options = ["ทุกครั้ง/ประจำ", "บางครั้ง", "ไม่ได้ปฏิบัติ/ไม่ใช่"]
        
        for item in hygiene_items:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(item)
            with col2:
                selection = st.radio(
                    item,
                    options=hygiene_options,
                    key=f"hygiene_{item.replace('/', '_')}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                form_data[f"สุขลักษณะ: {item}"] = selection
    
    # --- Section 5: Symptoms ---
    with st.expander("ส่วนที่ 5: ลักษณะอาการที่ส่งผลกระทบทางสุขภาพ", expanded=True):
        st.write("ความถี่ของอาการดังกล่าว")
        symptoms = [
            "อ่อนเพลีย", "เบื่ออาหาร", "คลื่นไส้/อาเจียน", "ท้องผูก", 
            "ปวดท้องรุนแรงเป็นพัก ๆ", "ปวดตามข้อ กล้ามเนื้อ", 
            "อาการปวดเมื่อยตามร่างกาย", "ปวดศีรษะ", "ซีด", "ซึม", "ชัก",
            "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย", 
            "น้ำหนักลดโดยไม่ทราบสาเหตุ", "มือสั่น", "มือ เท้า อ่อนแรง", "ผื่น"
        ]
        symptom_options = ["เป็นประจำหรือแทบทุกวัน", "นาน ๆ ครั้ง", "ไม่มี"]

        for symptom in symptoms:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(symptom)
            with col2:
                value = st.radio(
                    symptom,
                    symptom_options,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"symptom_{symptom.replace(' ', '_').replace('/', '_')}"
                )
                form_data[f'อาการ: {symptom}'] = value

    # --- Section 6: Medical Info ---
    with st.expander("ส่วนที่ 6: ผลการตรวจร่างกายและการตรวจทางห้องปฏิบัติการ", expanded=True):
        st.subheader("การตรวจร่างกายตามระบบโดยแพทย์")
        
        # Vitals
        col1, col2, col3, col4 = st.columns(4)
        form_data['BP'] = col1.text_input("BP (mmHg)")
        form_data['PR'] = col2.text_input("PR (/min)")
        form_data['RR'] = col3.text_input("RR (/min)")
        form_data['BT'] = col4.text_input("BT (°C)")

        physical_exam_data = {}
        
        exam_items_part1 = {
            "1) General appearance": "exam_general",
            "2) HEENT: conjunctivae": "exam_heent",
            "3) Lung": "exam_lung",
            "4) Abdomen": "exam_abdomen",
            "5) Skin": "exam_skin",
            "6) Hand writing (เขียนชื่อ-สกุลในช่องด้านล่าง)": "exam_handwriting",
        }

        for item, key in exam_items_part1.items():
            col1, col2 = st.columns([2, 5])
            with col1:
                st.write(item)
            with col2:
                sub_col1, sub_col2 = st.columns([1, 2])
                with sub_col1:
                    status = st.radio(item, ["Normal", "Abnormal"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "Abnormal":
                    with sub_col2:
                        detail = st.text_input("โปรดระบุความผิดปกติที่ตรวจพบ", key=f"{key}_detail", label_visibility="collapsed")
                physical_exam_data[item] = f"{status}{f' ({detail})' if detail else ''}"
        
        st.text_input(" ", key="handwriting_input", label_visibility="collapsed")

        st.write("7) Neuro sign: motor power grade")

        def create_motor_power_row(label, key_prefix):
            st.markdown(f"**{label}**")
            h_spacer, h_r, h_l = st.columns([2, 2, 2])
            with h_r: st.markdown("<p style='text-align: center;'><b>R</b></p>", unsafe_allow_html=True)
            with h_l: st.markdown("<p style='text-align: center;'><b>L</b></p>", unsafe_allow_html=True)
            
            for part in ["Proximal", "Distal"]:
                for muscle_type in ["Flexor", "extensor"]:
                    cols = st.columns([1, 1, 2, 2])
                    with cols[0]: st.markdown(part if muscle_type=="Flexor" else "")
                    with cols[1]: st.markdown(muscle_type)
                    for i, side in enumerate(["R", "L"]):
                        with cols[i+2]:
                            input_col, text_col = st.columns([4, 1])
                            with input_col:
                                key = f"{key_prefix}_{part}_{muscle_type}_{side}"
                                physical_exam_data[key] = st.text_input(key, key=key, label_visibility="collapsed")
                            with text_col:
                                st.markdown("<div style='padding-top: 8px;'>/5</div>", unsafe_allow_html=True)
        
        create_motor_power_row("(1) Upper extremities", "upper")
        create_motor_power_row("(2) Lower extremities", "lower")
        
        exam_items_part2 = {
            "8) Gait": "exam_gait",
            "9) Sensation": "exam_sensation",
            "10) Cognition": "exam_cognition",
            "11) Mood": "exam_mood",
            "12) IQ หรือ Mentality": "exam_iq",
        }

        for item, key in exam_items_part2.items():
            col1, col2 = st.columns([2, 5])
            with col1:
                st.write(item)
            with col2:
                sub_col1, sub_col2 = st.columns([1, 2])
                with sub_col1:
                    status = st.radio(item, ["Normal", "Abnormal"], key=f"{key}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "Abnormal":
                    with sub_col2:
                        detail = st.text_input("โปรดระบุความผิดปกติที่ตรวจพบ", key=f"{key}_detail", label_visibility="collapsed")
                physical_exam_data[item] = f"{status}{f' ({detail})' if detail else ''}"

        form_data['การตรวจร่างกาย'] = physical_exam_data

        st.subheader("ข้อมูลผลการตรวจทางห้องปฏิบัติการ")
        lab_results_data = {}

        st.write("**การตรวจสารบ่งชี้ทางชีวภาพ**")
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.write("ระดับตะกั่วในเลือด")
        with col2:
            input_col, unit_col = st.columns([3, 2])
            with input_col:
                lab_results_data['ระดับตะกั่วในเลือด'] = st.text_input("ผลการตรวจ", key="lab_lead_level", label_visibility="collapsed")
            with unit_col:
                st.markdown("<div style='padding-top: 8px;'>µg/dL</div>", unsafe_allow_html=True)
        with col3:
            lab_results_data['วันที่ตรวจ_ระดับตะกั่วในเลือด'] = st.date_input("วันที่ตรวจ", key="lab_lead_date", label_visibility="collapsed")

        st.write("**การตรวจทางห้องปฏิบัติการอื่นๆ**")
        
        other_lab_tests = ["CBC", "BUN/Cr", "SGPT/SGOT", "TB/DB", "Uric acid", "UA"]
        
        # Header
        col_h1, col_h2, col_h3 = st.columns([1,2,1])
        with col_h1: st.markdown("**รายการตรวจ**")
        with col_h2: st.markdown("**ผลการตรวจ**")
        with col_h3: st.markdown("**วันที่ตรวจ**")

        for test in other_lab_tests:
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                st.write(test)
            with col2:
                status = st.radio(test, ["ปกติ", "ผิดปกติ"], key=f"lab_{test}_status", horizontal=True, label_visibility="collapsed")
                detail = ""
                if status == "ผิดปกติ":
                    detail = st.text_input("ระบุ", key=f"lab_{test}_detail", label_visibility="collapsed")
                lab_results_data[test] = f"{status}{f' ({detail})' if detail else ''}"
            with col3:
                lab_results_data[f"วันที่ตรวจ_{test}"] = st.date_input("date", key=f"lab_{test}_date", label_visibility="collapsed")
        
        form_data['ผลทางห้องปฏิบัติการ'] = lab_results_data

    # --- Section 7 & 8: Diagnosis and Recommendations ---
    with st.expander("ส่วนที่ 7 และ 8: การวินิจฉัยและการรักษา", expanded=True):
        st.subheader("ส่วนที่ 7: การวินิจฉัยโรค")
        diagnosis_options = st.multiselect(
            "การวินิจฉัย:",
            ["สงสัยโรคจากตะกั่ว", "โรคจากตะกั่ว", "โรคอื่นๆ"]
        )
        if "โรคอื่นๆ" in diagnosis_options:
            other_diagnosis = st.text_input("ระบุโรคอื่นๆ:")
            form_data['การวินิจฉัย'] = ", ".join(diagnosis_options) + f" ({other_diagnosis})"
        else:
            form_data['การวินิจฉัย'] = ", ".join(diagnosis_options)

        st.subheader("ส่วนที่ 8: การรักษาพยาบาล หรือข้อเสนอแนะอื่นๆ")
        form_data['การรักษาและข้อเสนอแนะ'] = st.text_area("รายละเอียด:", height=200)

        st.subheader("ข้อมูลแพทย์ผู้ตรวจ")
        form_data['แพทย์ผู้ตรวจ'] = st.text_input("ชื่อ - นามสกุล แพทย์ผู้ตรวจร่างกาย", key="doc_name")
        form_data['เบอร์โทรแพทย์'] = st.text_input("เบอร์โทร", key="doc_phone")
        form_data['ID Line แพทย์'] = st.text_input("ID Line", key="doc_line")
        form_data['วันที่ตรวจ'] = st.date_input("วัน/เดือน/ปี", key="doc_date")

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

