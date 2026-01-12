import streamlit as st
import google.generativeai as genai

# כותרת האפליקציה
st.title("הצ'אט שלי עם Gemini")

# הגדרת המפתח - השורה הזו מחפשת את הסיסמה בתוך ההגדרות של הענן
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    # חיבור ל-Gemini
    genai.configure(api_key=api_key)
    # הגדרת האייג'נט וההנחיות שלו
    system_instruction = """
    אתה יועץ ביטוח מומחה ופיננסי אישי של משפחת פרנקפורט.
    התפקיד שלך הוא לעזור לנהל את תביעות הביטוח, להבין את הפוליסות ולמצוא כפל ביטוחי.
    
    כללים:
    1. ענה תמיד בעברית קצרה ותכליתית.
    2. אם אתה לא בטוח בכיסוי מסוים, תבקש לראות את הפוליסה.
    3. תהיה אמפתי, אבל מקצועי.
    4. כששואלים אותך על כסף, תציג את התשובה בצורה של טבלה אם אפשר.
    """
    
    # שימוש במודל מהיר וחדש יותר שתומך בהוראות מערכת
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    # תיבת טקסט למשתמש
    user_input = st.chat_input("כתוב משהו...")

    # היסטוריית צ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # הצגת ההיסטוריה
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # טיפול בהודעה חדשה
    if user_input:
        # הצגת הודעת המשתמש
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # קבלת תשובה מה-AI
        response = model.generate_content(user_input)
        
        # הצגת התשובה
        st.chat_message("assistant").write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
