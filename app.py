import streamlit as st
import google.generativeai as genai
from PIL import Image

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
    התפקיד שלך הוא לעזור לנהל את תביעות הביטוח, להבין את הפוליסות ולמצוא כפל ביטוחי.
    
    כללים:
    1. ענה תמיד בעברית קצרה ותכליתית.
    2. אם מעלים תמונה של מסמך, סכם בקצרה מה רואים בו והאם יש שם משהו דחוף לטיפול.
    3. תהיה אמפתי, אבל מקצועי.
    4. כששואלים אותך על כסף, תציג את התשובה בצורה של טבלה אם אפשר.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    # --- תוספת חדשה: אזור להעלאת קבצים בצד ---
    with st.sidebar:
        st.header("צרף מסמך ביטוח")
        uploaded_file = st.file_uploader("בחר תמונה (PNG/JPG)", type=["png", "jpg", "jpeg"])
        
        image_data = None
        if uploaded_file is not None:
            # הצגת התמונה בקטן כדי שנדע שזה עבד
            image_data = Image.open(uploaded_file)
            st.image(image_data, caption="המסמך שלך", use_column_width=True)

    # היסטוריית צ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # הצגת ההיסטוריה
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # תיבת טקסט למשתמש
    user_input = st.chat_input("שאל משהו על הביטוח או על המסמך שהעלית...")

    if user_input:
        # הצגת השאלה שלך
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # הכנת הפנייה ל-AI (עם או בלי תמונה)
        if image_data:
            # אם יש תמונה, שולחים גם אותה וגם את הטקסט
            inputs = [user_input, image_data]
            st.info("מנתח את המסמך שהעלית... 📄") # חיווי למשתמש
        else:
            # אם אין תמונה, שולחים רק טקסט
            inputs = [user_input]

        # שליחה וקבלת תשובה
        try:
            response = model.generate_content(inputs)
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"אופס, קרתה שגיאה: {e}")
