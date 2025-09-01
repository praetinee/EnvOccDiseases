# -*- coding: utf-8 -*-
import streamlit as st
import datetime

def render():
    """Renders the Lead Environmental Child Investigation Form (Pb), correctly structured as per the source document."""
    st.header("แบบสอบสวนการสัมผัสสารตะกั่วของเด็กในบ้านพักอาศัย และในชุมชน")
    st.caption("(แบบสอบสวน Pb)")

    # This dictionary will hold all the collected data.
    form_data = {}

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อเด็ก'] = col1.text_input("1.1 ชื่อ ด.ช./ด.ญ.:")
        form_data['เลขบัตรประชาชน'] = col2.text_input("เลขบัตรประชาชน:")
        
        col1, col2, col3 = st.columns(3)
        form_data['วันเกิด'] = col1.date_input("1.2 วัน/เดือน/ปีเกิด:")
        form_data['น้ำหนัก'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("1.3 ชื่อผู้ปกครอง:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, เบอร์โทร")
        
        st.write("จำนวนสมาชิกในครอบครัว:")
        col1, col2 = st.columns(2)
        form_data['สมาชิกทั้งหมด'] = col1.number_input("รวม (คน)", min_value=0, step=1, key="pb_total_fam")
        form_data['สมาชิกเด็ก<7ปี'] = col2.number_input("เด็ก < 7 ปี (คน)", min_value=0, step=1, key="pb_u7_fam")

    # --- Section 2: Risk Factors ---
    with st.expander("ส่วนที่ 2: ปัจจัยเสี่ยงต่อการสัมผัสสารตะกั่วของเด็ก", expanded=True):
        st.subheader("2.1 อาชีพผู้ปกครอง ผู้ดูแล หรือคนที่อยู่อาศัยบ้านเดียวกับเด็ก")
        risk_jobs_list = [
            "งานเกี่ยวกับแบตเตอรี่", "ถลุงตะกั่ว หลอมตะกั่ว", "งานเชื่อมหรือบัดกรี", "หลอมตะกั่ว/กระสุน",
            "ทาหรือพ่นสี", "ซ่อมยานยนต์", "ซ่อมแห อวน (ที่มีตะกั่วถ่วงน้ำหนัก)", "ซ่อมเรือประมง (ที่มีการใช้เสน)",
            "ซ่อมเครื่องใช้ไฟฟ้า", "คัดแยกขยะอิเล็กทรอนิกส์", "เครื่องเคลือบ เครื่องปั้นดินเผา",
            "งานโรงพิมพ์/งานหล่อตัวพิมพ์", "งานเกี่ยวกับสี", "ทำเครื่องประดับ"
        ]

        work_outside = st.radio("1) ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน", ["ไม่ใช่", "ใช่"], key="pb_work_outside", horizontal=True)
        if work_outside == "ใช่":
            selected_jobs_outside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="pb_jobs_outside")
            other_job_outside = st.text_input("อื่นๆ:", key="pb_other_job_outside")
            if other_job_outside: selected_jobs_outside.append(other_job_outside)
            form_data['อาชีพนอกบ้าน'] = ", ".join(selected_jobs_outside)
            form_data['ความเกี่ยวข้อง_นอกบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="pb_rel_outside")

        work_inside = st.radio("2) ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน", ["ไม่ใช่", "ใช่"], key="pb_work_inside", horizontal=True)
        if work_inside == "ใช่":
            selected_jobs_inside = st.multiselect("ระบุอาชีพ:", risk_jobs_list, key="pb_jobs_inside")
            other_job_inside = st.text_input("อื่นๆ:", key="pb_other_job_inside")
            if other_job_inside: selected_jobs_inside.append(other_job_inside)
            form_data['อาชีพในบ้าน'] = ", ".join(selected_jobs_inside)
            form_data['ความเกี่ยวข้อง_ในบ้าน'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="pb_rel_inside")

        store_nearby = st.radio("3) กิจการร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตรจากที่อยู่อาศัย)", ["ไม่มี", "มี"], key="pb_store_nearby", horizontal=True)
        if store_nearby == "มี":
            selected_stores = st.multiselect("ระบุกิจการ:", risk_jobs_list, key="pb_stores_select")
            other_store = st.text_input("อื่นๆ:", key="pb_other_store_text")
            if other_store: selected_stores.append(other_store)
            form_data['ร้านค้าใกล้บ้าน'] = ", ".join(selected_stores)

        st.subheader("2.2 แผนผังลักษณะที่อยู่อาศัย")
        st.markdown("วาดแผนผังลักษณะที่อยู่อาศัย, บริเวณที่อยู่อาศัย, วัสดุ, บ้านเก่า, ทาสี, ลักษณะการเก็บข้าวของเครื่องใช้ในบ้าน และให้ใส่ **ดาว (⭐)** บริเวณที่ทำงานเกี่ยวกับตะกั่วในบ้าน, บริเวณที่นอน, ที่รับประทานอาหาร, สถานที่จัดเก็บอุปกรณ์ที่เกี่ยวข้องกับตะกั่ว (โดยการเดินสำรวจ)")
        form_data['แผนผังที่อยู่อาศัย'] = st.file_uploader("อัปโหลดรูปภาพแผนผัง", type=["png", "jpg", "jpeg"], key="pb_map_upload")
        
        st.subheader("2.3 ปัจจัยเกี่ยวข้องกับการสัมผัสสารตะกั่วของเด็ก")
        risk_factors_data = {}
        st.markdown("**เกี่ยวกับที่พักอาศัย**")
        risk_factors_data['บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา'] = st.radio("1. บ้านใช้สีน้ำมันทาภายใน และ/หรือมีการหลุดลอกของสีทา", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_paint")
        risk_factors_data['โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น'] = st.radio("2. โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_floor")
        risk_factors_data['มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน'] = st.radio("3. มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_tools")
        risk_factors_data['สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)'] = st.radio("4. สภาพภายในบ้านไม่ค่อยได้ทำความสะอาด (จากการสังเกต)", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_clean")

        st.markdown("**เกี่ยวกับพฤติกรรมเสี่ยงของผู้ปกครอง/ผู้ดูแล**")
        risk_factors_data['ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป'] = st.radio("5. ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_work_freq")
        risk_factors_data['บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน'] = st.radio("6. บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้าน หรือบริเวณบ้าน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_work_loc")
        risk_factors_data['หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที'] = st.radio("7. หลังเลิกงาน ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_shower")
        risk_factors_data['ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก'] = st.radio("8. ในแต่ละวันท่านปนเปื้อน ฝุ่น หรือสีเป็นปริมาณมาก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_contamination")
        risk_factors_data['ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว'] = st.radio("9. ป้อนอาหารเด็กขณะทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_feed")
        risk_factors_data['อุ้มหรือกอดเด็กระหว่างทำงาน'] = st.radio("10. อุ้มหรือกอดเด็กระหว่างทำงาน", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_hold")

        st.markdown("**พฤติกรรมของเด็ก**")
        risk_factors_data['เด็กชอบอมหรือดูดนิ้วหรือไม่'] = st.radio("11. เด็กชอบอมหรือดูดนิ้วหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_suck")
        risk_factors_data['เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่'] = st.radio("12. เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_mouth")
        risk_factors_data['ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร'] = st.radio("13. ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_handwash")
        risk_factors_data['เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว'] = st.radio("14. เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_sleep")
        risk_factors_data['บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว'] = st.radio("15. บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_play")
        risk_factors_data['ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก'] = st.radio("16. ของเล่นของเด็กเป็นวัสดุที่สีหลุดลอก", ["ใช่/มี", "ไม่ใช่/ไม่มี"], horizontal=True, key="pb_rf_toys")
        form_data['ปัจจัยเกี่ยวข้อง'] = risk_factors_data

    # --- Section 3: Environmental Measurement ---
    with st.expander("ส่วนที่ 3: การตรวจวัดสภาพแวดล้อมในบ้าน", expanded=True):
        st.markdown("##### ผลการตรวจวัดระดับฝุ่นตะกั่วในบ้าน (Wipe technique)")
        col1, col2, col3 = st.columns([2,2,1])
        col1.markdown("**จุดเก็บตัวอย่าง**")
        col2.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
        col3.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")

        with col1: st.markdown("พื้น (Floors)")
        with col2: form_data['พื้น (Floors)'] = st.number_input("พื้น (Floors)", min_value=0.0, format="%.2f", label_visibility="collapsed", key="pb_wipe_floor")
        with col3: st.markdown("10")

        with col1: st.markdown("ขอบหน้าต่าง (Window Sills)")
        with col2: form_data['ขอบหน้าต่าง'] = st.number_input("ขอบหน้าต่าง", min_value=0.0, format="%.2f", label_visibility="collapsed", key="pb_wipe_sill")
        with col3: st.markdown("100")

        with col1: st.markdown("รางหน้าต่าง (window troughs)")
        with col2: form_data['รางหน้าต่าง'] = st.number_input("รางหน้าต่าง", min_value=0.0, format="%.2f", label_visibility="collapsed", key="pb_wipe_trough")
        with col3: st.markdown("100")
        
        form_data['ข้อมูลเพิ่มเติม_สิ่งแวดล้อม'] = st.text_area("ข้อมูลเพิ่มเติมอื่นๆ:", key="pb_env_other_info")
        form_data['ผู้สำรวจ'] = st.text_input("ผู้ทำการสำรวจ (ชื่อ-สกุล):", key="pb_surveyor_name")
        form_data['เบอร์โทรผู้สำรวจ'] = st.text_input("เบอร์โทรหรือ ID Line:", key="pb_surveyor_contact")

    # --- Section 4: Symptoms and Physical Exam ---
    with st.expander("ส่วนที่ 4: ข้อมูลอาการและการตรวจร่างกาย", expanded=True):
        st.subheader("4.1 การซักประวัติ อาการและอาการแสดงของเด็กในรอบ 3 เดือนที่ผ่านมา")
        symptoms_data_child = {}
        symptoms_list_child = [
            "ปวดท้อง", "อาเจียน", "อ่อนเพลีย", "ท้องเสีย", "โลหิตจาง", "ชัก", "หมดสติ",
            "การเจริญเติบโตและพัฒนาการล่าช้ากว่าเกณฑ์", "ระดับสติปัญญาต่ำกว่าเกณฑ์",
            "ท้องผูก", "เบื่ออาหาร", "กระวนกระวาย/ไม่มีสมาธิ", "หงุดหงิดง่าย"
        ]
        
        # Table Header
        st.markdown("""
        <style>
        .header-grid {{
            display: grid;
            grid-template-columns: 2fr 3fr;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .symptom-grid {{
            display: grid;
            grid-template-columns: 2fr 3fr;
            align-items: center;
            margin-bottom: -15px;
        }}
        </style>
        <div class="header-grid">
            <div>อาการ</div>
            <div style="text-align: center;">ความถี่ของอาการดังกล่าว</div>
        </div>
        """, unsafe_allow_html=True)


        # Displaying symptoms in a more compact way
        for symptom in symptoms_list_child:
            with st.container():
                cols = st.columns([2,3])
                with cols[0]:
                    st.write(symptom)
                with cols[1]:
                    symptoms_data_child[symptom] = st.radio(
                        symptom, 
                        ["เป็นประจำ/แทบทุกวัน", "นานๆครั้ง", "ไม่มี"], 
                        horizontal=True, 
                        label_visibility="collapsed", 
                        key=f"pb_symp_{symptom.replace('/','')}"
                    )

        form_data['อาการเด็ก'] = symptoms_data_child

        st.subheader("4.2 การตรวจร่างกายตามระบบ")
        st.info("ส่วนการตรวจร่างกายโดยแพทย์ สามารถใช้ข้อมูลจากแบบบันทึกการตรวจร่างกาย (แบบ Pb-2) ได้")
        
        st.subheader("4.3 ข้อมูลผลตรวจทางห้องปฏิบัติการ")
        st.info("ส่วนผลการตรวจทางห้องปฏิบัติการ สามารถใช้ข้อมูลจากแบบบันทึกการตรวจร่างกาย (แบบ Pb-2) ได้")

    st.markdown("---")
    if st.button("บันทึกข้อมูล", use_container_width=True, type="primary", key="pb_submit_child_pb"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        # For debugging, you can uncomment the line below to see the collected data
        # st.write(form_data)
