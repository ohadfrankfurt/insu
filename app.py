import streamlit as st
import google.generativeai as genai
import json

# --- הגדרת דף ---
st.set_page_config(page_title="ניהול ביטוחים ומיצוי זכויות", page_icon="🏥")

# --- פונקציית אבטחה (Login) ---
def check_password():
    if "APP_PASSWORD" not in st.secrets:
        return True 

    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.title("🔒 כניסה למערכת")
        password = st.text_input("סיסמה:", type="password")
        if password:
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("סיסמה שגויה")
        return False
    return True

if not check_password():
    st.stop()

# --- האפליקציה ---
st.title("🏥 מנהל הביטוחים המשפחתי")
st.caption("מיצוי זכויות • ניהול תביעות • הבנת כיסויים")

# חיבור למפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- המוח החדש: ממוקד מיצוי זכויות ותביעות ---
    system_instruction = """
    אתה מנהל תיק הביטוח של משפחת פרנקפורט.
    המטרה העליונה: עזרה במיצוי זכויות והגשת תביעות.
    
    הנחיות:
    1. אל תתמקד במחיר, אלא ב*מה מגיע למבוטח*.
    2. כשמנתחים פוליסה, הדגש את הכיסויים המרכזיים (ניתוחים, תרופות, לידה, התפתחות הילד).
    3. אם המשתמש שואל על פרוצדורה רפואית, הסבר בדיוק מה צריך להגיש כדי לקבל החזר.
    4. זהה השתתפות עצמית ותקרות כיסוי.
    
    ענה בעברית ברורה, מקצועית ומרגיעה.
    """
    
    model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

    # --- סרגל צד: דשבורד כיסויים ---
    with st.sidebar:
        st.header("📂 תיק מסמכים")
        uploaded_files = st.file_uploader("העלה פוליסות או כתבי שירות", type=["pdf"], accept_multiple_files=True)
        
        pdf_parts = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    pdf_parts.append({
                        "mime_type": "application/pdf",
                        "data": uploaded_file.getvalue()
                    })
                except:
                    pass
            
            # --- ניתוח אוטומטי מותאם לניהול כיסויים ---
            if len(pdf_parts) > 0:
                st.divider()
                st.subheader("📌 תמצית הכיסוי")
                
                with st.spinner("מחלץ זכויות..."):
                    try:
                        # פרומפט ששואב מידע אופרטיבי לשימוש בביטוח
                        dashboard_prompt = """
                        נתח את המסמך והחזר אובייקט JSON בלבד.
                        תתמקד בתוכן הכיסוי ולא במחיר.
                        המבנה:
                        {
                            "provider": "שם החברה (למשל: הראל, מכבי)",
                            "main_coverage": "מהות הביטוח ב-3 מילים (למשל: שב״ן, בריאות פרטי, תאונות)",
                            "deductible": "גובה השתתפות עצמית (אם יש)",
                            "key_benefit": "הטבה אחת בולטת (למשל: רופא עד הבית, החזר ייעוץ)"
                        }
                        """
                        
                        response = model.generate_content([dashboard_prompt] + pdf_parts)
                        clean_json = response.text.replace("```json", "").replace("```", "").strip()
                        data = json.loads(clean_json)
                        
                        # הצגת נתונים רלוונטיים לתביעה
                        st.info(f"**חברה:** {data.get('provider')}")
                        st.success(f"**סוג:** {data.get('main_coverage')}")
                        
                        c1, c2 = st.columns(2)
                        c1.metric("השתתפות עצמית", data.get('deductible', 'ללא'))
                        c2.metric("הטבה בולטת", "ראה פירוט", help=data.get('key_benefit'))
                        st.caption(f"✨ {data.get('key_benefit')}")
                        
                    except Exception as e:
                        st.warning("לא הצלחתי לחלץ נתונים אוטומטית")

    # --- צ'אט ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "היי אוהד. העלה את הפוליסה ואעזור לך להבין מה מגיע לכם ואיך מגישים את התביעה."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("למשל: האם מגיע לי החזר על ייעוץ רופא מומחה?")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        inputs = [user_input]
        if pdf_parts: inputs.extend(pdf_parts)
        
        try:
            response = model.generate_content(inputs)
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("שגיאה בתקשורת")
