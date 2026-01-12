import streamlit as st
import google.generativeai as genai

# כותרת האפליקציה
st.title("הצ'אט שלי עם Gemini - יועץ ביטוח")

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # הגדרת האייג'נט
    system_instruction = """
    אתה יועץ ביטוח מומחה ופיננסי אישי של משפחת פרנקפורט.
    התפקיד שלך הוא לנתח מסמכי ביטוח, פוליסות ודוחות שנתיים מקבצי PDF.
    
    כללים:
    1. ענה תמיד בעברית קצרה ותכליתית.
    2. סכם את המסמך: מה סוג הביטוח, כמה משלמים, ומה הכיסוי העיקרי.
    3. חפש "מוקשים" או חריגים בפוליסה וציין אותם.
    4. כששואלים אותך על כסף, תציג את התשובה בצורה של טבלה אם אפשר.
    """
    
    # שימוש בשם שהופיע במפורש ברשימה שלך
    model_name = "gemini-flash-latest"

    try:
        model = genai.GenerativeModel(
            model_name=model_name, 
            system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"שגיאה בטעינת המודל: {e}")

    # --- אזור להעלאת קבצים בצד ---
    with st.sidebar:
        st.header("צרף מסמך ביטוח")
        uploaded_file = st.file_uploader("בחר קובץ PDF", type=["pdf"])
        
        pdf_part = None
        if uploaded_file is not None:
            try:
                # קריאת הקובץ והכנתו לשליחה ל-Gemini
                bytes_data = uploaded_file.getvalue()
                pdf_part = {
                    "mime_type": "application/pdf",
                    "data": bytes_data
                }
                st.success("הקובץ נטען! אפשר לשאול שאלות.")
            except Exception as e:
                st.error(f"תקלה בטעינת הקובץ: {e}")

    # היסטוריית צ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # הצגת ההיסטוריה
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # תיבת טקסט למשתמש
    user_input = st.chat_input("שאל משהו על הפוליסה...")

    if user_input:
        # הצגת השאלה
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # הכנת הפנייה (טקסט + PDF אם קיים)
        inputs = [user_input]
        if pdf_part:
            inputs.append(pdf_part)
            st.toast("Gemini קורא את המסמך... 📄")

        # קבלת תשובה
        try:
            # אם המודל לא הוגדר בהצלחה למעלה, נמנע קריסה
            if 'model' in locals():
                response = model.generate_content(inputs)
                st.chat_message("assistant").write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("המודל לא נטען כראוי, אנא בדוק את הגדרות ה-API.")
        except Exception as e:
            st.error(f"שגיאה: {e}")
