import streamlit as st
import google.generativeai as genai
import json

# --- הגדרת דף ---
st.set_page_config(page_title="האופטימייזר המשפחתי", page_icon="💸")

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
st.title("💸 האופטימייזר המשפחתי")
st.caption("ממקסמים החזרים • מנצלים פיצול שנים • עוקפים תקרות")

# חיבור למפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- המוח המעודכן: אסטרטגיית הראל + מכבי ---
    system_instruction = """
    אתה מנהל אופטימיזציית תביעות ביטוח למשפחה ישראלית.
    המטרה: להוציא מקסימום כסף מהביטוח, בצורה חוקית וחכמה.

    ### האלגוריתם שלך (חובה לפעול לפי סדר זה):
    
    1. **שלב ראשון: זיהוי "כסף מתחדש" (Renewable First)**
       - חפש בפוליסות סעיפים של "התייעצות עם רופא מומחה" (למשל סעיף 3.1 בהראל נספח 456).
       - בדוק אם יש תקרה *לביקור* (למשל 715 ש"ח) ותקרה *שנתית*.
       - **המלצה קריטית:** אם הטיפול מתפרס על פני דצמבר-ינואר, המלץ לפצל חשבוניות כדי להרוויח מכסה כפולה (שנת 2025 + שנת 2026).
       - הנחיה למשתמש: "בקשו קבלה על 'ייעוץ מומחה' ולא על 'בדיקה'".

    2. **שלב שני: "כסף ייעודי" (Specific Bucket)**
       - רק אחרי שסחטנו את הייעוצים, חפש סעיפים ייעודיים (כמו "בדיקות היריון" סעיף 3.7 בהראל, או "טיפולי התפתחות הילד").
       - נצל את הסעיפים האלה עד התקרה שלהם.

    3. **שלב שלישי: שב"ן (קופת חולים)**
       - את היתרה (או דברים שאין בפרטי, כמו דולה/הבראה) - שלח ל"סל היריון" של מכבי שלי/זהב.
       - זכור: סל היריון הוא חד-פעמי לכל ההיריון, שמור אותו לסוף או לדברים שאין להם כיסוי אחר.

    ### סגנון תשובה:
    - דבר "דוגרי" ובגובה העיניים (כמו יועץ שמכיר את הטריקים).
    - תמיד תן **Action Plan**: מה לבקש מהרופא לכתוב בחשבונית.
    - עשה חישוב כספי: "אם תעשו X תקבלו 500 ש"ח, אם תעשו Y תקבלו 1000 ש"ח".
    """
    
    model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

    # --- סרגל צד ---
    with st.sidebar:
        st.header("📂 מסמכים לניתוח")
        uploaded_files = st.file_uploader("העלה פוליסות / נספחים / קבלות", type=["pdf"], accept_multiple_files=True)
        
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
            
            if len(pdf_parts) > 0:
                st.success(f"התקבלו {len(pdf_parts)} קבצים. האופטימייזר מוכן.")

    # --- צ'אט ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "היי! אני מכיר את הטריקים של נספח 456 ושל מכבי. תעלו את המסמכים ואגיד לכם איך לפצל את החשבוניות כדי לקבל מקסימום כסף."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("למשל: איך להגיש 13 קבלות של רופא פרטי?")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        inputs = [user_input]
        if pdf_parts: inputs.extend(pdf_parts)
        
        with st.spinner("מחשב מסלול לכסף... 💰"):
            try:
                response = model.generate_content(inputs)
                st.chat_message("assistant").write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("שגיאה בתקשורת.")
