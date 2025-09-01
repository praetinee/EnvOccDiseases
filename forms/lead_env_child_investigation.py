# -*- coding: utf-8 -*-
import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Child Investigation Form (Pb), correctly structured as per the source document."""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของเด็กในบ้านพักอาศัย และในชุมชน")
    st.caption("(แบบสอบสวน Pb)")

    form_data = {}

    # --- Section 1: General Info & Child History ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไปและประวัติเด็ก", expanded=True):
        st.subheader("1.1 ข้อมูลทั่วไป")
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
        form_data['สมาชิกทั้งหมด'] = col1.number_input("รวม (คน)", min_value=0, step=1, key="child_total_fam_v2")
        form_data['สมาชิกเด็ก<7ปี'] = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1, key="child_u7_fam_v2")

        st.divider()
        st.subheader("1.2 ประวัติเด็ก")
        child_history_data = {}
        child_history_data['ประวัติการเจ็บป่วย_อดีต'] = st.text_input("ประวัติการเจ็บป่วยในอดีต (โรคประจำตัว):")
        
        st.markdown("**ประวัติการคลอด**")
        col1, col2, col3, col4 = st.columns(4)
        child_history_data['การคลอด'] = col1.radio("การคลอด:", ["ครบกำหนด", "ก่อนกำหนด"], key="birth_term")
        child_history_data['น้ำหนักแรกคลอด'] = col2.number_input("น้ำหนักแรกคลอด (กรัม):", min_value=0, key="birth_weight")
        child_history_data['วิธีคลอด'] = col3.radio("วิธีคลอด:", ["ปกติ", "ผ่าตัด"], key="birth_method")
        child_history_data['ภาวะแทรกซ้อน'] = col4.radio("ภาวะแทรกซ้อน:", ["ไม่มี", "มี"], key="birth_complication")
        
        st.markdown("**ประวัติพัฒนาการ** (อายุที่เริ่มทำได้)")
        dev_col1, dev_col2, dev_col3, dev_col4 = st.columns(4)
        child_history_data['ชันคอ'] = dev_col1.text_input("ชันคอ:", key="dev_neck")
        child_history_data['นั่ง'] = dev_col2.text_input("นั่ง:", key="dev_sit")
        child_history_data['คลาน'] = dev_col3.text_input("คลาน:", key="dev_crawl")
        child_history_data['ยืน'] = dev_col4.text_input("ยืน:", key="dev_stand")
        child_history_data['เดิน'] = dev_col1.text_input("เดิน:", key="dev_walk")
        child_history_data['พูดคำแรก'] = dev_col2.text_input("พูดคำแรก:", key="dev_word")
        child_history_data['พูดเป็นประโยค'] = dev_col3.text_input("พูดเป็นประโยค:", key="dev_sentence")
        
        child_history_data['ประวัติวัคซีน'] = st.radio("ประวัติการได้รับวัคซีน:", ["ครบตามเกณฑ์", "ไม่ครบ/ไม่แน่ใจ"], key="vaccine_hist")
        
        st.markdown("**พฤติกรรมของเด็ก**")
        behavior_cols = st.columns(2)
        child_history_data['ดูดนิ้ว'] = behavior_cols[0].checkbox("ดูดนิ้ว", key="behav_suck")
        child_history_data['เอาของเข้าปาก'] = behavior_cols[1].checkbox("เอาของเล่น/สิ่งแปลกปลอมเข้าปาก", key="behav_mouth")
        child_history_data['ไม่ล้างมือก่อนกินข้าว'] = behavior_cols[0].checkbox("ไม่ล้างมือก่อนรับประทานอาหาร", key="behav_handwash")
        child_history_data['กินอาหาร/น้ำจากภาชนะเสี่ยง'] = behavior_cols[1].checkbox("กินอาหาร/น้ำจากภาชนะที่มีสีสัน หรือหม้อที่ไม่ได้มาตรฐาน", key="behav_container")
        child_history_data['เล่นนอกบ้าน'] = behavior_cols[0].checkbox("ชอบเล่นนอกบ้าน", key="behav_outside")
        child_history_data['เล่นดินทราย'] = behavior_cols[1].checkbox("ชอบเล่นคลุกคลีกับดิน ทราย", key="behav_sand")
        child_history_data['พฤติกรรมอื่นๆ'] = st.text_input("พฤติกรรมอื่นๆ:", key="behav_other")

        st.markdown("**ประวัติการใช้ยา/อาหารเสริม**")
        med_cols = st.columns(3)
        child_history_data['ยาหม้อ/ยาลูกกลอน'] = med_cols[0].checkbox("ยาหม้อ/ยาลูกกลอน", key="med_herbal")
        child_history_data['แคลเซียม'] = med_cols[1].checkbox("แคลเซียม", key="med_calcium")
        child_history_data['วิตามิน'] = med_cols[2].checkbox("วิตามิน", key="med_vitamin")
        
        form_data['ประวัติเด็ก'] = child_history_data

    # --- Section 2: Risk Factors ---
    with st.expander("ส่วนที่ 2: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่วของเด็ก", expanded=True):
        st.subheader("2.1 อาชีพผู้ปกครอง ผู้ดูแล หรือคนที่อยู่อาศัยบ้านเดียวกับเด็ก")
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)",
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]

        work_outside = st.radio("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน", ["ไม่ใช่", "ใช่"], key="work_outside_radio_v2")
        if work_outside == "ใช่":
            selected_jobs_outside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="jobs_outside_select_v2")
            other_job_outside = st.text_input("อื่นๆ:", key="other_job_outside_text_v2")
            if other_job_outside: selected_jobs_outside.append(other_job_outside)
            form_data['อาชีพนอกบ้าน'] = ", ".join(selected_jobs_outside)
            form_data['ความเกี่ยวข้อง_นอกบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="rel_outside_select_v2")

        work_inside = st.radio("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน", ["ไม่ใช่", "ใช่"], key="work_inside_radio_v2")
        if work_inside == "ใช่":
            selected_jobs_inside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="jobs_inside_select_v2")
            other_job_inside = st.text_input("อื่นๆ:", key="other_job_inside_text_v2")
            if other_job_inside: selected_jobs_inside.append(other_job_inside)
            form_data['อาชีพในบ้าน'] = ", ".join(selected_jobs_inside)
            form_data['ความเกี่ยวข้อง_ในบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="rel_inside_select_v2")

        store_nearby = st.radio("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย)", ["ไม่มี", "มี"], key="store_nearby_radio_v2")
        if store_nearby == "มี":
            selected_stores = st.multiselect("ระบุกิจการ:", risk_jobs_list, key="stores_select_v2")
            other_store = st.text_input("อื่นๆ:", key="other_store_text_v2")
            if other_store: selected_stores.append(other_store)
            form_data['ร้านค้าใกล้บ้าน'] = ", ".join(selected_stores)

        st.subheader("2.2 แผนผังลักษณะที่อยู่อาศัย")
        st.markdown("วาดแผนผังลักษณะที่อยู่อาศัย, บริเวณที่อยู่อาศัย, วัสดุ, บ้านเก่า, ทาสี, ลักษณะการเก็บข้าวของเครื่องใช้ในบ้าน และให้ใส่ **ดาว (⭐)** บริเวณที่ทำงานเกี่ยวกับตะกั่วในบ้าน, บริเวณที่นอน, ที่รับประทานอาหาร, สถานที่จัดเก็บอุปกรณ์ที่เกี่ยวข้องกับตะกั่ว (โดยการเดินสำรวจ)")
        form_data['แผนผังที่อยู่อาศัย'] = st.file_uploader("อัปโหลดรูปภาพแผนผัง", type=["png", "jpg", "jpeg"], key="map_upload_v2")

        st.subheader("2.3 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก")
        risk_factors_data = {}
        st.markdown("**เกี่ยวกับที่พักอาศัย**")
        risk_factors_data['บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา'] = st.radio("บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_paint_v2")
        risk_factors_data['โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น'] = st.radio("โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_floor_v2")
        risk_factors_data['มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน'] = st.radio("มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_tools_v2")
        risk_factors_data['สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)'] = st.radio("สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_clean_v2")

        st.markdown("**เกี่ยวกับพฤติกรรมเสี่ยงของผู้ปกครอง/ผู้ดูแล**")
        risk_factors_data['ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป'] = st.radio("ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_work_freq_v2")
        risk_factors_data['บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน'] = st.radio("บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_work_loc_v2")
        risk_factors_data['หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที'] = st.radio("หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_shower_v2")
        risk_factors_data['ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก'] = st.radio("ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_contamination_v2")
        risk_factors_data['ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว'] = st.radio("ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_feed_v2")
        risk_factors_data['อุ้มหรือกอดเด็กระหว่างทำงาน'] = st.radio("อุ้มหรือกอดเด็กระหว่างทำงาน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_hold_v2")

        st.markdown("**พฤติกรรมของเด็ก**")
        risk_factors_data['เด็กชอบอมหรือดูดนิ้วหรือไม่'] = st.radio("เด็กชอบอมหรือดูดนิ้วหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_suck_v2")
        risk_factors_data['เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่'] = st.radio("เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_mouth_v2")
        risk_factors_data['ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร'] = st.radio("ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_handwash_v2")
        risk_factors_data['เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว'] = st.radio("เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_sleep_v2")
        risk_factors_data['บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว'] = st.radio("บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_play_v2")
        risk_factors_data['ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก'] = st.radio("ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="rf_toys_v2")
        form_data['ปัจจัยเกี่ยวข้อง'] = risk_factors_data

    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.markdown("##### ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        col1, col2, col3 = st.columns([2,2,1])
        col1.markdown("**จุดเก็บตัวอย่าง**")
        col2.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
        col3.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")

        with col1: st.markdown("พื้น (Floors)")
        with col2: form_data['พื้น (Floors)'] = st.number_input("พื้น (Floors)", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_floor_v2")
        with col3: st.markdown("5")

        with col1: st.markdown("ขอบหน้าต่าง (Window Sills)")
        with col2: form_data['ขอบหน้าต่าง'] = st.number_input("ขอบหน้าต่าง", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_sill_v2")
        with col3: st.markdown("40")

        with col1: st.markdown("รางหน้าต่าง (window troughs)")
        with col2: form_data['รางหน้าต่าง'] = st.number_input("รางหน้าต่าง", min_value=0.0, format="%.2f", label_visibility="collapsed", key="wipe_trough_v2")
        with col3: st.markdown("100")
        
        form_data['ข้อมูลเพิ่มเติม_สิ่งแวดล้อม'] = st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:", key="env_other_info_v2")
        form_data['ผู้สำรวจ'] = st.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):", key="surveyor_name_v2")
        form_data['เบอร์โทรผู้สำรวจ'] = st.text_input("เบอร์โทรหรือ ID Line:", key="surveyor_contact_v2")

    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา")
        symptoms_data_child = {}
        symptoms_list_child = [
            "ปวดท้อง", "อาเจียน", "อ่อนเพลีย", "ท้องเสีย", "โลหิตจาง", "ชัก", "หมดสติ",
            "การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "ระดับสติปัญญาต่ำกว่าเกณฑ์",
            "ท้องผูก", "เบื่ออาหาร", "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย"
        ]
        st.markdown("""
        | อาการ | เป็นประจำหรือแทบทุกวัน | นาน ๆ ครั้ง | ไม่มี |
        | :--- | :---: | :---: | :---: |
        """)
        for symptom in symptoms_list_child:
            col1, col2, col3, col4 = st.columns([2,1,1,1])
            col1.write(symptom)
            symptoms_data_child[symptom] = st.radio(symptom, ["เป็นประจำหรือแทบทุกวัน", "นาน ๆ ครั้ง", "ไม่มี"], horizontal=True, label_visibility="collapsed", key=f"symp_child_{symptom}_v2")
        form_data['อาการเด็ก'] = symptoms_data_child

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        st.info("ส่วนการตรวจร่างกายโดยแพทย์ สามารถใช้ข้อมูลจากแบบบันทึกการตรวจร่างกาย (แบบ Pb-2) ได้")
        
        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        st.info("ส่วนผลการตรวจทางห้องปฏิบัติการ สามารถใช้ข้อมูลจากแบบบันทึกการตรวจร่างกาย (แบบ Pb-2) ได้")

    st.markdown("---")
    if st.button("บันทึกข้อมูล", use_container_width=True, type="primary", key="submit_child_pb_v2"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)

