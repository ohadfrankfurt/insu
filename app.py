import streamlit as st
import google.generativeai as genai

# כותרת האפליקציה
st.title("בדיקת כפל ביטוחים (Gemini)")

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # הגדרת האייג'נט - מתמחה בהשוואות
    system_instruction = """
    אתה יועץ ביטוח מומחה של משפחת פרנקפורט.
    המטרה שלך היא לחסוך כסף על ידי איתור כפל ביטוח.
    
    הנחיות לפעולה:
    1. אם הועלה מסמך אחד: סכם אותו, ציין מחיר וכיסויים עיקריים.
    2. אם הועלו שני מסמכים או יותר: בצע השוואה ראש-בראש.
       - צור טבלה שמשווה את הכיסויים בכל מסמך.
       - ציין במפורש: "נמצאה חפיפה בכיסוי X".
       - המלץ איזה ביטוח נראה משתלם יותר (מבחינת עלות מול תועלת).
    3. דבר קצר, ברור ובעברית.
    """
    
    # שימוש במודל שעבד לנו בהצלחה
    model_name = "gemini-flash-latest"

    try:
        model = genai.GenerativeModel(
            model_name=model_name, 
            system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"שגיאה בטעינת המודל: {e}")

    # --- אזור להעלאת קבצים (מרובה) ---
    with st.sidebar:
        st.header("העלאת פוליסות להשוואה")
        # השינוי כאן: accept_multiple_files=True
        uploaded_files = st.file_uploader("בחר קבצי PDF (אפשר כמה יחד)", type=["pdf"], accept_multiple_files=True)
        
        pdf_parts = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    bytes_data = uploaded_file.getvalue()
                    pdf_parts.append({
                        "mime_type": "application/pdf",
                        "data": bytes_data
                    })
                except Exception as e:
                    st.error(f"תקלה בקובץ {uploaded_file.name}: {e}")
            
            if len(pdf_parts) > 0:
                st.success(f"נטענו {len(pdf_parts)} מסמכים בהצלחה! לחץ על הצ'אט כדי להשוות.")

    # היסטוריית צ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # תיבת טקסט למשתמש
    user_input = st.chat_input("למשל: האם יש לי כפל ביטוח בין הקבצים?")

    if user_input:
