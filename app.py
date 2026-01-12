import streamlit as st
import google.generativeai as genai
import time

# --- הגדרת דף (חובה שיהיה בהתחלה) ---
st.set_page_config(page_title="הביטוחים של משפחת פרנקפורט", page_icon="🛡️")

# --- פונקציית אבטחה (Login) ---
def check_password():
    """Returns `True` if the user had the correct password."""
    
    # אם לא הוגדרה סיסמה ב-Secrets, נאפשר כניסה חופשית (למניעת נעילה עצמית)
    if "APP_PASSWORD" not in st.secrets:
        st.warning("לא הוגדרה סיסמה ב-Secrets. האפליקציה פתוחה לכולם.")
        return True

    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.title("🔒 כניסה מאובטחת")
        password = st.text_input("הזן סיסמה לכניסה:", type="password")
        
        if password:
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("סיסמה שגויה")
        return False
    return True

# אם הסיסמה לא נכונה - הקוד עוצר כאן
if not check_password():
    st.stop()

# --- מכאן מתחילה האפליקציה הרגילה (רק למורשים) ---

st.title("🛡️ יועץ הביטוח המשפחתי")

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # הגדרת האייג'נט
    system_instruction = """
    אתה יועץ ביטוח מומחה ופיננסי אישי.
    
    תפקידך:
    1. לנתח מסמכים ולהשוות ביניהם.
    2. במצב של "סיכום מהיר" (Dashboard): שלוף רק את המחיר, תוקף וציון.
    3. במצב צ'אט: ענה על שאלות המשתמש.
    
    ענה תמיד בעברית קצרה.
    """
    
    model_name = "gemini-flash-latest"

    try:
        model = genai.GenerativeModel(
            model_name=model_name, 
            system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"שגיאה בטעינת המודל: {e}")

    # --- סרגל צד: העלאה + ניתוח אוטומטי ---
    with st.sidebar:
        st.header("📂 מסמכים")
        uploaded_files = st.file_uploader("גרור לכאן פוליסות (PDF)", type=["pdf"], accept_multiple_files=True)
        
        pdf_parts = []
        if uploaded_files:
            # עיבוד הקבצים
            for uploaded_file in uploaded_files:
                try:
                    bytes_data = uploaded_file.getvalue()
                    pdf_parts.append({
                        "mime_type": "application/pdf",
                        "data": bytes_data
                    })
                except Exception as e:
                    st.error(f"תקלה בקובץ: {e}")
            
            # --- פיצ'ר חדש: ניתוח אוטומטי (השורה התחתונה) ---
            if len(pdf_parts) > 0:
                st.divider()
                st.subheader("📊 שורה תחתונה")
                with st.spinner("מנתח עלויות..."):
                    try:
                        # שליחת בקשה מיוחדת רק לסיכום
                        summary_prompt = """
                        עבור המסמכים המצורפים, צור סיכום קצר מאוד עבור דשבורד ניהולי.
                        תציג רק:
                        1. סה"כ לתשלום חודשי (בשקלים).
                        2. תאריך חידוש הביטוח הבא.
                        3. ציון לביטוח (1-10) והערה קצרה של מילה אחת (למשל: "יקר", "מצוין", "כפול").
                        
                        תעצב את זה יפה עם אימוג'י.
                        """
                        response_summary = model.generate_content([summary_prompt] + pdf_parts)
                        st.info(response_summary.text)
                    except Exception as e:
                        st.warning("לא הצלחתי לייצר סיכום אוטומטי")

    # --- אזור הצ'אט ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "היי אוהד! אני מוגן בסיסמה. תעלה קבצים ואתן לך ניתוח מיידי בצד ימין, או תשאל אותי שאלות כאן."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("שאל שאלות מתקדמות על הפוליסה...")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        inputs = [user_input]
        if pdf_parts:
            inputs.extend(pdf_parts)
            
        try:
            if 'model' in locals():
                response = model.generate_content(inputs)
                st.chat_message("assistant").write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"שגיאה: {e}")
