# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from utils.g_sheets_connector import save_to_sheet

def render():
    """Renders the Lead Environmental Child Risk Assessment Form (PbC03)."""
    st.header("แบบประเมินความเสี่ยงการสัมผัสสารตะกั่วในเด็กแรกเกิดถึงอายุต่ำกว่า 15 ปี")
    st.caption("(แบบ PbC03) (ใช้ได้ทั้งกรณีเชิงรับและเชิงรุก)")

    form_data = {}

    # --- Section 1: General Info ---
    with st.expander("ส่วนที่ 1: ข้อมูลทั่วไป", expanded=True):
        col1, col2 = st.columns(2)
        form_data['ชื่อเด็ก'] = col1.text_input("ชื่อ ด.ช./ด.ญ.:")
        form_data['เพศ'] = col2.radio("เพศ:", ["ชาย", "หญิง"], horizontal=True)

        col1, col2, col3 = st.columns(3)
        form_data['วัน/เดือน/ปีเกิด'] = col1.date_input("วัน/เดือน/ปีเกิด:")
        form_data['น้ำหนัก (กก.)'] = col2.number_input("น้ำหนัก (กก.):", min_value=0.0, format="%.2f")
        form_data['ส่วนสูง (ซม.)'] = col3.number_input("ส่วนสูง (ซม.):", min_value=0.0, format="%.2f")

        form_data['ชื่อผู้ปกครอง'] = st.text_input("ชื่อผู้ปกครอง:")
        form_data['ที่อยู่ปัจจุบัน'] = st.text_area("ที่อยู่ปัจจุบัน:", placeholder="บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด")

    # --- Section 2: Exposure Opportunity Assessment ---
    with st.expander("ส่วนที่ 2: ประเมินโอกาสการสัมผัสสารตะกั่ว", expanded=True):
        
        exposure_data = {}

        # --- Callback Functions for Exclusive Selection ---
        def not_related_callback():
            """If the 'not related' checkbox is checked, reset all previous radio buttons to 'ไม่ใช่'."""
            if st.session_state.get('pbc03_is_not_related'):
                st.session_state.work_outside_radio = "ไม่ใช่"
                st.session_state.work_inside_radio = "ไม่ใช่"
                st.session_state.near_source_radio = "ไม่ใช่"
                st.session_state.paint_peeling_radio = "ไม่ใช่"

        def questions_1_to_4_callback():
            """If any of the 'yes' options are selected, uncheck the 'not related' checkbox."""
            if (st.session_state.get('work_outside_radio') == 'ใช่' or
                st.session_state.get('work_inside_radio') == 'ใช่' or
                st.session_state.get('near_source_radio') == 'ใช่' or
                st.session_state.get('paint_peeling_radio') == 'ใช่'):
                st.session_state.pbc03_is_not_related = False
        
        # --- Question 1 ---
        st.write("1. ทำงานเกี่ยวข้องกับตะกั่ว โดยสถานที่ทำงานอยู่นอกบ้าน")
        is_work_outside = st.radio(
            " ", ["ไม่ใช่", "ใช่"], 
            key="work_outside_radio", 
            label_visibility="collapsed", 
            horizontal=True,
            on_change=questions_1_to_4_callback
        )
        if is_work_outside == 'ใช่':
            work_outside_options = st.multiselect(
                "ระบุอาชีพ:",
                ["ทำเครื่องประดับ", "ก่อสร้าง/รื้อถอนอาคาร", "อู่ซ่อมเรือไม้", "งานเกี่ยวข้องกับสี", "งานเกี่ยวกับเครื่องยนต์", 
                 "งานเกี่ยวกับแบตเตอรี่", "หลอมตะกั่ว/กระสุน", "รีไซเคิลขยะอิเล็กทรอนิกส์", "ร้อยเม็ดตะกั่ว เบ็ดตกปลา/อวนหาปลา"],
                key="work_outside_multiselect"
            )
            other_work_outside = st.text_input("อื่นๆ:", key="work_outside_other")
            if other_work_outside: work_outside_options.append(other_work_outside)
            exposure_data['work_outside'] = ", ".join(work_outside_options)
            exposure_data['work_outside_relation'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="work_outside_relation")
        else:
            exposure_data['work_outside'] = "ไม่ใช่"

        # --- Question 2 ---
        st.write("2. ทำงานที่เกี่ยวข้องกับตะกั่วในบ้าน/บริเวณบ้าน")
        is_work_inside = st.radio(
            " ", ["ไม่ใช่", "ใช่"], 
            key="work_inside_radio", 
            label_visibility="collapsed", 
            horizontal=True,
            on_change=questions_1_to_4_callback
        )
        if is_work_inside == 'ใช่':
            work_inside_options = st.multiselect(
                "ระบุอาชีพ:",
                ["ทำเครื่องประดับ", "ก่อสร้าง/รื้อถอนอาคาร", "อู่ซ่อมเรือไม้", "งานเกี่ยวข้องกับสี", "งานเกี่ยวกับเครื่องยนต์", 
                 "งานเกี่ยวกับแบตเตอรี่", "หลอมตะกั่ว/กระสุน", "รีไซเคิลขยะอิเล็กทรอนิกส์", "ร้อยเม็ดตะกั่ว เบ็ดตกปลา/อวนหาปลา"],
                key="work_inside_multiselect"
            )
            other_work_inside = st.text_input("อื่นๆ:", key="work_inside_other")
            if other_work_inside: work_inside_options.append(other_work_inside)
            exposure_data['work_inside'] = ", ".join(work_inside_options)
            exposure_data['work_inside_relation'] = st.multiselect("ความเกี่ยวข้องกับเด็ก:", ["บิดา", "มารดา", "พี่", "ญาติคนอื่นๆ"], key="work_inside_relation")
        else:
             exposure_data['work_inside'] = "ไม่ใช่"

        # --- Question 3 ---
        st.write("3. บ้านอยู่ใกล้แหล่งอุตสาหกรรม หรือกิจการ ร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตร)")
        is_near_source = st.radio(
            " ", ["ไม่ใช่", "ใช่"], 
            key="near_source_radio", 
            label_visibility="collapsed", 
            horizontal=True,
            on_change=questions_1_to_4_callback
        )
        if is_near_source == 'ใช่':
             source_options = st.multiselect(
                "ระบุ:",
                ["ทำเครื่องประดับ", "ก่อสร้าง/รื้อถอนอาคาร", "อู่ซ่อมเรือไม้", "งานเกี่ยวข้องกับสี", "งานเกี่ยวกับเครื่องยนต์", 
                 "งานเกี่ยวกับแบตเตอรี่", "หลอมตะกั่ว/กระสุน", "รีไซเคิลขยะอิเล็กทรอนิกส์", "ร้อยเม็ดตะกั่ว เบ็ดตกปลา/อวนหาปลา"],
                key="near_source_multiselect"
            )
             other_source = st.text_input("อื่นๆ:", key="near_source_other")
             if other_source: source_options.append(other_source)
             exposure_data['near_source'] = ", ".join(source_options)
        else:
            exposure_data['near_source'] = "ไม่ใช่"
            
        # --- Question 4 ---
        exposure_data['paint_peeling'] = st.radio(
            "4. อาศัยอยู่ในบ้านที่มีสีทาบ้านหลุดลอก", 
            ["ไม่ใช่", "ใช่"], 
            horizontal=True,
            key="paint_peeling_radio",
            on_change=questions_1_to_4_callback
        )
        
        # --- Question 5 (Exclusive Checkbox) ---
        is_not_related = st.checkbox(
            "5. ไม่เกี่ยวข้องกับ ข้อ 1 - 4 ดังกล่าวข้างต้น (จัดเป็นกลุ่มที่ไม่ได้สัมผัส จบข้อคำถาม)",
            key="pbc03_is_not_related",
            on_change=not_related_callback
        )
        form_data['การประเมินโอกาสการสัมผัส'] = str(exposure_data)
        
        if is_not_related:
            st.info("จากข้อมูลข้างต้น จัดเป็นกลุ่มที่ไม่ได้สัมผัส")
            if st.button("บันทึกข้อมูล", use_container_width=True, type="primary"):
                 save_to_sheet("LeadEnvChildRisk", form_data)
            st.stop()

    # --- Section 3: Risk Assessment ---
    with st.expander("ส่วนที่ 3: การประเมินความเสี่ยงของเด็กในการสัมผัสสารตะกั่ว", expanded=True):
        
        risk_questions = {
            "เกี่ยวกับที่พักอาศัย": {
                "บ้านมีการหลุดลอกของสีทาบ้าน": 1.5,
                "บ้านอยู่ใกล้แหล่งอุตสาหกรรม หรือกิจการ ร้านค้าที่เกี่ยวข้องกับตะกั่ว (ระยะไม่เกิน 30 เมตร)": 1.5,
                "โดยส่วนใหญ่สมาชิกครอบครัวนอนบนพื้น": 1.0,
                "มีการเก็บอุปกรณ์ทำความสะอาดบ้านไว้ในบ้าน": 1.0,
            },
            "เกี่ยวกับที่ทำงาน": {
                "ทำงานเกี่ยวข้องกับตะกั่วทุกวัน หรือสัปดาห์ละ 2-3 วันขึ้นไป": 1.5,
                "บริเวณที่ทำงานเกี่ยวข้องกับตะกั่วอยู่ในบ้านหรือบริเวณบ้าน": 3.0,
                "หลังเลิกงานที่เกี่ยวข้องกับตะกั่ว ส่วนใหญ่ไม่ได้อาบน้ำและเปลี่ยนเสื้อผ้าทันที": 1.5,
                "การเก็บวัสดุ อุปกรณ์ ที่ทำงานเกี่ยวข้องกับตะกั่วไว้ในบ้าน หรือมีแบตเตอรี่วางไว้ในบ้าน": 1.5,
                "เก็บชุดทำงานที่ใส่แล้วไว้ในบ้าน": 1.5,
                "ซักชุดทำงานรวมกับเสื้อผ้าอื่นๆ": 1.0,
            },
            "ข้อมูลเด็ก": {
                "เด็กชอบอมหรือดูดนิ้วหรือไม่": 1.5,
                "เด็กชอบเอาสิ่งแปลกปลอม/ของเล่นเข้าปากหรือไม่": 1.5,
                "ส่วนใหญ่เด็กไม่ได้ล้างมือก่อนรับประทานอาหาร": 1.5,
                "เด็กนอนกับผู้ปกครองที่ทำงานสัมผัสสารตะกั่ว": 1.5,
                "บ่อยครั้งที่เด็กอยู่บริเวณที่ทำงานเกี่ยวกับตะกั่ว": 2.0,
                "ของเล่นของเด็ก เป็นวัสดุที่สีหลุดลอก": 1.5,
            },
            "ข้อมูลการป่วยด้วยโรคจากตะกั่ว": {
                 "มีประวัติสมาชิกครอบครัวป่วยด้วยโรคจากตะกั่ว หรือสารประกอบของตะกั่ว": 3.0
            }
        }

        scores = {}
        total_score = 0
        
        # Header
        col_h1, col_h2, col_h3, col_h4 = st.columns([4, 2, 1, 1])
        col_h1.markdown("**ข้อมูล**")
        col_h2.markdown("<div style='text-align: center;'><b>ไม่ใช่ / ใช่</b></div>", unsafe_allow_html=True)
        col_h3.markdown("<div style='text-align: center;'><b>ค่าน้ำหนัก C</b></div>", unsafe_allow_html=True)
        col_h4.markdown("<div style='text-align: center;'><b>คะแนน D = BxC</b></div>", unsafe_allow_html=True)


        for category, questions in risk_questions.items():
            st.markdown(f"**{category}**")
            for question, weight in questions.items():
                
                col1, col2, col3, col4 = st.columns([4, 2, 1, 1])
                
                with col1:
                    st.write(question)
                
                key = f"risk_{question.replace(' ', '_').replace('/', '_')}"
                
                with col2:
                    score = st.radio(
                        "selection for " + key,
                        [0, 1],
                        horizontal=True,
                        key=key,
                        label_visibility="collapsed",
                        index=0
                    )

                with col3:
                    st.markdown(f"<div style='text-align: center; padding-top: 8px;'>{weight}</div>", unsafe_allow_html=True)

                calculated_score = score * weight
                with col4:
                    st.markdown(f"<div style='text-align: center; padding-top: 8px;'>{calculated_score:.1f}</div>", unsafe_allow_html=True)
                
                scores[question] = {
                    'answer': score,
                    'weight': weight,
                    'calculated_score': calculated_score
                }
                total_score += calculated_score
        
        st.markdown("---")
        _, col_total_label, col_total_val = st.columns([6, 1, 1])
        col_total_label.markdown("**คะแนนรวม**")
        col_total_val.markdown(f"<div style='text-align: center;'><b>{total_score:.1f}</b></div>", unsafe_allow_html=True)

        form_data['คะแนนความเสี่ยงรายข้อ'] = str(scores)
        form_data['คะแนนความเสี่ยงรวม'] = total_score
        
    # --- Section 4: Summary ---
    with st.expander("ส่วนที่ 4: สรุปผลการประเมินความเสี่ยงเบื้องต้น", expanded=True):
        st.write(f"**คะแนนรวมของคำตอบข้อ 1 - 17: {total_score:.2f}**")
        
        risk_level = ""
        if total_score >= 19:
            risk_level = "สูง"
            st.error(f"**ระดับความเสี่ยง: {risk_level}**")
        elif 10 <= total_score < 19:
            risk_level = "ปานกลาง"
            st.warning(f"**ระดับความเสี่ยง: {risk_level}**")
        else: # < 10
            risk_level = "ต่ำ"
            st.success(f"**ระดับความเสี่ยง: {risk_level}**")
        
        form_data['ระดับความเสี่ยง'] = risk_level
        
        if risk_level in ["ปานกลาง", "สูง"]:
            st.info("ควรประเมินระดับฝุ่นตะกั่วในบ้านเพิ่มเติม, ซักประวัติเด็กเพิ่มเติมตามแบบฟอร์ม PbC01 พร้อมเจาะเลือดหาระดับตะกั่วในเลือด หรือส่งเด็กไปยังหน่วยบริการสาธารณสุขในพื้นที่")

    # --- Section 5: Environmental Dust Levels (Conditional) ---
    if form_data.get('ระดับความเสี่ยง') in ["ปานกลาง", "สูง"]:
        with st.expander("ส่วนที่ 5: ระดับฝุ่นตะกั่วในบ้าน (เก็บด้วย Wipe technique)", expanded=True):
            env_data = {}
            
            # Header Row
            header_col1, header_col2, header_col3 = st.columns(3)
            with header_col1:
                st.markdown("**จุดเก็บตัวอย่าง**")
            with header_col2:
                st.markdown("**ระดับตะกั่วบนพื้นผิว (µg/ft²)**")
            with header_col3:
                st.markdown("**ค่าอ้างอิง EPA (µg/ft²)**")

            # Data Row 1: Floor
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            with row1_col1:
                st.write("พื้น (Floors)")
            with row1_col2:
                env_data['floor'] = st.number_input("พื้น (Floors)", min_value=0.0, format="%.2f", key="env_floor", label_visibility="collapsed")
            with row1_col3:
                st.markdown("<div style='padding-top: 8px;'>5</div>", unsafe_allow_html=True)
            
            # Data Row 2: Window Sills
            row2_col1, row2_col2, row2_col3 = st.columns(3)
            with row2_col1:
                st.write("ขอบหน้าต่าง (Window Sills)")
            with row2_col2:
                env_data['window_sills'] = st.number_input("ขอบหน้าต่าง (Window Sills)", min_value=0.0, format="%.2f", key="env_sills", label_visibility="collapsed")
            with row2_col3:
                st.markdown("<div style='padding-top: 8px;'>40</div>", unsafe_allow_html=True)

            # Data Row 3: Window Troughs
            row3_col1, row3_col2, row3_col3 = st.columns(3)
            with row3_col1:
                st.write("รางหน้าต่าง (window troughs)")
            with row3_col2:
                env_data['window_troughs'] = st.number_input("รางหน้าต่าง (window troughs)", min_value=0.0, format="%.2f", key="env_troughs", label_visibility="collapsed")
            with row3_col3:
                st.markdown("<div style='padding-top: 8px;'>100</div>", unsafe_allow_html=True)
            
            form_data['ระดับฝุ่นตะกั่วในบ้าน'] = str(env_data)

    # --- Section 6: Recommendations ---
    with st.expander("ส่วนที่ 6: ข้อเสนอแนะในการควบคุมความเสี่ยงจากการสัมผัสสารตะกั่ว", expanded=True):
        form_data['ข้อเสนอแนะ'] = st.text_area("", key="recommendations_text", label_visibility="collapsed")
        
    form_data['วันที่เก็บข้อมูล'] = st.date_input("วันที่เก็บข้อมูล:", key="collection_date")

    if st.button("บันทึกข้อมูล", use_container_width=True, type="primary"):
        success = save_to_sheet("LeadEnvChildRisk", form_data)
        if success:
            st.success("บันทึกข้อมูลเรียบร้อยแล้ว")
        else:
            st.error("การบันทึกข้อมูลล้มเหลว กรุณาตรวจสอบการตั้งค่าและลองอีกครั้ง")

