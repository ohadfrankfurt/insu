import streamlit as st
import google.generativeai as genai

st.title("בדיקת מודלים זמינים")

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    st.header("רשימת המודלים בחשבון שלך:")
    
    try:
        # הפקודה הזו מבקשת מגוגל את הרשימה האמיתית
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # מציג את השם המדויק
                count += 1
        
        if count == 0:
            st.error("לא נמצאו מודלים. ייתכן שיש בעיה במפתח או בהרשאות.")
            
    except Exception as e:
        st.error(f"שגיאה בהתחברות: {e}")
