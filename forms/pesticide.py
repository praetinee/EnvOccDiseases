# -*- coding: utf-8 -*-
import streamlit as st

def render():
    """Renders the Pesticide Investigation Form."""
    
    st.header("แบบสอบสวนโรคหรืออาการสำคัญของพิษจากสารกำจัดศัตรูพืช")

    form_data = {}

    # --- Section 1: Population Characteristics ---
    with st.expander("ส่วนที่ 1: ข้อมูลลักษณะประชากร", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อ-สกุล'] = col1.text_input("1.1 ชื่อ - สกุล:")
        form_data['เพศ'] = col2.radio("1.2 เพศ:", ["ชาย", "หญิง"], horizontal=True)

        col1, col2, col3 = st.columns(3)
        form_data['น้ำหนัก (กก.)'] = col1.number_input("1.3 น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง (ซม.)'] = col2.number_input("1.4 ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")
        form_data['อายุ (ปี)'] = col3.number_input("1.5 อายุ (ปี):", min_value=0, step=1)

        comorbidities = st.multiselect(
            "1.6 โรคประจำตัว:",
            ["เบาหวาน", "ความดันโลหิตสูง", "ภูมิแพ้"]
        )
        other_comorbidity = st.text_input("โรคประจำตัวอื่นๆ (ระบุ):")
        if other_comorbidity:
            comorbidities.append(other_comorbidity)
        form_data['โรคประจำตัว'] = ", ".join(comorbidities) if comorbidities else "ไม่มี"

        col1, col2 = st.columns(2)
        form_data['การสูบบุหรี่'] = col1.radio("1.7 ท่านสูบบุหรี่/ยาเส้นหรือไม่:", ["สูบ", "ไม่สูบ"])
        form_data['การดื่มแอลกอฮอล์'] = col2.radio("1.8 ท่านดื่มเครื่องดื่มแอลกอฮอล์หรือไม่:", ["ดื่ม", "ไม่ดื่ม"])

        occupation_opt = st.radio("1.9 ลักษณะอาชีพที่ทำ:", ["เพาะปลูกด้วยตนเอง", "รับจ้างเพาะปลูก", "อื่นๆ"])
        if occupation_opt == "อื่นๆ":
            occupation_other = st.text_input("ระบุลักษณะอาชีพอื่นๆ:", label_visibility="collapsed")
            form_data['ลักษณะอาชีพที่ทำ'] = occupation_other
        else:
            form_data['ลักษณะอาชีพที่ทำ'] = occupation_opt

        col1, col2 = st.columns(2)
        form_data['ประเภทของพืชที่เพาะปลูก'] = col1.text_input("1.10 ประเภทของพืชที่ทำการเพาะปลูก:")
        form_data['พื้นที่เกษตรกรรม (ไร่)'] = col2.number_input("1.11 พื้นที่เกษตรกรรมของท่านทั้งหมด (ไร่):", min_value=0)

        knowledge_opt = st.radio("1.12 ท่านเคยรู้เรื่องอันตรายจากสารกำจัดศัตรูพืชหรือไม่:", ["ไม่เคย", "เคย"])
        if knowledge_opt == "เคย":
            knowledge_source = st.text_input("จากแหล่ง (ระบุ):")
            form_data['ความรู้เรื่องอันตราย'] = f"เคย (จาก: {knowledge_source})"
        else:
            form_data['ความรู้เรื่องอันตราย'] = "ไม่เคย"

    # --- Section 2: Exposure Possibility ---
    with st.expander("ส่วนที่ 2: ความเป็นไปได้ของการได้รับสัมผัส", expanded=True):
        form_data['เป็นผู้ได้รับผลกระทบ'] = st.radio("2.1 ท่านเป็นผู้ได้รับผลกระทบหรือผู้ป่วยจากเหตุการณ์วันนั้นหรือไม่:", ["ใช่", "ไม่ใช่"])
        form_data['เคยเป็นผู้ใช้สารเคมีเอง'] = st.radio("2.2 ท่านเคยเป็นผู้ใช้สารกำจัดศัตรูพืชด้วยตนเองมาก่อนหรือไม่:", ["ใช่", "ไม่ใช่"])

        involvement_opts = st.multiselect(
            "2.3 ในวันเกิดเหตุ ท่านเกี่ยวข้องกับการใช้สารเคมีกำจัดศัตรูพืชอย่างไร:",
            ["เป็นผู้ผสมสารเคมี", "เป็นผู้ฉีดพ่นเองหรือหว่านเมล็ดเอง", "อยู่ในบริเวณที่มีการฉีดพ่นหรือสัมผัส", "ไม่เกี่ยวข้องเลย"]
        )
        involvement_other = st.text_input("ความเกี่ยวข้องอื่นๆ:")
        if involvement_other: involvement_opts.append(involvement_other)
        form_data['ความเกี่ยวข้องในวันเกิดเหตุ'] = ", ".join(involvement_opts)

        source_opts = st.multiselect("2.4 ท่านได้สารเคมีกำจัดศัตรูพืชมาจากแหล่งใด:", ["ซื้อร้านค้า", "จากเพื่อนบ้าน", "หน่วยงานรัฐ"])
        source_other = st.text_input("แหล่งที่มาอื่นๆ:")
        if source_other: source_opts.append(source_other)
        form_data['แหล่งที่มาของสารเคมี'] = ", ".join(source_opts)

        chem_knowledge_opt = st.radio("2.5 ในวันดังกล่าว ก่อนการใช้สารเคมีท่านทราบหรือไม่ว่าสารเคมีนี้ คืออะไร:", ["ไม่ทราบ", "ทราบ"])
        if chem_knowledge_opt == "ทราบ":
            chem_name = st.text_input("ระบุชื่อสาร:", label_visibility="collapsed")
            form_data['ทราบชนิดสารเคมี'] = f"ทราบ (ชื่อ: {chem_name})"
        else:
             form_data['ทราบชนิดสารเคมี'] = "ไม่ทราบ"
        
        st.write("พฤติกรรมการป้องกัน:")
        
        protection_behaviors = {
            "2.6 ได้อ่านฉลากหรือไม่:": "อ่านฉลาก",
            "2.7 ใส่หน้ากาก/ผ้าปิดจมูกหรือไม่:": "ใส่หน้ากาก",
            "2.8 สวมถุงมือยางหรือไม่:": "สวมถุงมือ",
            "2.9 สวมเสื้อแขนยาว/กางเกงขายาวหรือไม่:": "สวมเสื้อผ้าแขนยาว",
            "2.10 สวมรองเท้าบู๊ทยางหรือไม่:": "สวมรองเท้าบู๊ท",
            "2.11 ถอดเสื้อผ้าทันทีหลังทำงานหรือไม่:": "ถอดเสื้อผ้าทันที",
            "2.12 ท่านมีการแยกซักเสื้อผ้าที่สวมใส่ทำงานกับเสื้อผ้าอื่นๆ:": "แยกซักเสื้อผ้า"
        }

        for question, key in protection_behaviors.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"<div style='height: 38px; display: flex; align-items: center;'>{question}</div>", unsafe_allow_html=True)
            with col2:
                form_data[key] = st.radio(
                    question, 
                    ["ใช่", "ไม่ใช่"], 
                    key=f"ppe_{key}", 
                    horizontal=True, 
                    label_visibility="collapsed"
                )

        disposal_opt = st.radio("2.13 ท่านทิ้งภาชนะที่ใส่เมล็ดพืชที่ไหนอย่างไร:", ["ทิ้งไว้ทั่วไป", "ฝังกลบ", "เผา", "อื่นๆ"])
        if disposal_opt == "อื่นๆ":
            disposal_other = st.text_input("วิธีทิ้งภาชนะอื่นๆ:", label_visibility="collapsed")
            form_data['การทิ้งภาชนะ'] = disposal_other
        else:
            form_data['การทิ้งภาชนะ'] = disposal_opt

        col1, col2 = st.columns(2)
        form_data['ล้างมือ/ร่างกายหลังทำงาน'] = col1.radio("2.14 ล้างมือ/ร่างกายหลังทำงาน หรือไม่:", ["มี", "ไม่มี"])
        form_data['ล้างมือ/ร่างกายก่อนกินอาหาร'] = col2.radio("2.15 ล้างมือ/ร่างกายก่อนกินอาหาร หรือไม่:", ["มี", "ไม่มี"])

        col1, col2 = st.columns(2)
        form_data['เวลาก่อนกินอาหาร'] = col1.text_input("2.16 หลังใช้สารเคมีนานเท่าไหร่จึงกินอาหาร (นาที/ชม.):")
        form_data['เวลาก่อนเกิดอาการ'] = col2.text_input("2.17 หลังกินอาหารนานเท่าไหร่จึงเกิดอาการ (นาที/ชม.):")

    # --- Section 3: Symptoms ---
    with st.expander("ส่วนที่ 3: ลักษณะอาการหรือผลกระทบ", expanded=True):
        symptoms = [
            "เวียนศีรษะ/ปวดศีรษะ", "คลื่นไส้", "อาเจียน", "หายใจติดขัด",
            "เจ็บหน้าอก/แน่นหน้าอก", "คันที่ผิวหนัง/มีตุ่มที่ผิวหนัง", "แสบจมูก", "แสบตา/ตาแดง/คันตา"
        ]
        
        # Table Header
        header_cols = st.columns([3, 2, 3])
        header_cols[0].markdown("**ลักษณะอาการ**")
        header_cols[1].markdown("<div style='text-align: center;'><b>อาการ</b></div>", unsafe_allow_html=True)
        header_cols[2].markdown("<div style='text-align: center;'><b>การรักษา (กรณีมีอาการ)</b></div>", unsafe_allow_html=True)
        st.divider()

        for symptom in symptoms:
            row_cols = st.columns([3, 2, 3])
            row_cols[0].write(symptom)
            
            with row_cols[1]:
                has_symptom = st.radio("", ["มี", "ไม่มี"], key=f"has_{symptom}", label_visibility="collapsed", horizontal=True)

            with row_cols[2]:
                if has_symptom == "มี":
                    treatment = st.radio("", ["ไม่ได้รับการรักษา", "รักษา/admit"], key=f"treat_{symptom}", label_visibility="collapsed", horizontal=True)
                    form_data[f"การรักษา: {symptom}"] = treatment
                else:
                    st.write("") # Placeholder for alignment

            form_data[f"อาการ: {symptom}"] = has_symptom


    # --- Section 4: Other Info ---
    with st.expander("ส่วนที่ 4: ข้อมูลอื่นๆ เพิ่มเติม", expanded=True):
        clinic_opt = st.radio(
            "4.1 ท่านรู้จักคลินิกเกษตรกรหรือไม่:",
            ["ไม่รู้จัก", "รู้จัก และเคยไปใช้บริการ", "รู้จัก แต่ไม่เคยไปรับบริการ", "อื่นๆ"]
        )
        if clinic_opt == "อื่นๆ":
            clinic_other = st.text_input("อื่นๆ (เกี่ยวกับคลินิกเกษตรกร):", label_visibility="collapsed")
            form_data['รู้จักคลินิกเกษตรกร'] = clinic_other
        else:
            form_data['รู้จักคลินิกเกษตรกร'] = clinic_opt

        form_data['ข้อมูลอื่นๆ'] = st.text_area("4.2 ข้อมูลอื่นๆ:")
        
        st.write("ข้อมูลผู้บันทึก")
        col1, col2, col3 = st.columns(3)
        form_data['ผู้บันทึก'] = col1.text_input("ผู้บันทึกข้อมูล ชื่อ-สกุล:")
        form_data['เบอร์โทรผู้บันทึก'] = col2.text_input("โทรศัพท์:")
        form_data['หน่วยงานผู้บันทึก'] = col3.text_input("หน่วยงาน:")

    st.markdown("---")
    if st.button("เสร็จสิ้นและบันทึกข้อมูล", use_container_width=True, type="primary"):
        st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว (จำลอง)")
        st.write(form_data)
