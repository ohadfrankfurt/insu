import streamlit as st
import google.generativeai as genai
import json

# --- הגדרת דף ---
st.set_page_config(page_title="האופטימייזר של משפחת פרנקפורט", page_icon="💸")

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
st.caption("ממקסמים החזרים • מנצלים כל שקל • עובדים חכם")

# חיבור למפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("נא להזין מפתח API", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- המוח: Strict Auditor & Creative Optimizer ---
    system_instruction = """
    You are a Strict Insurance Claims Auditor & Creative Family Optimizer.
    Your goal is to legally maximize the cash refund for the family by utilizing EVERY available policy (Husband & Wife) and EVERY clause type.

    --- VOICE & TONE GUIDELINES (CRITICAL) ---
    1. LANGUAGE: Hebrew Only. Natural, modern, Israeli ("בגובה העיניים").
    2. VIBE:
       - Calm & Reassuring ("אל דאגה, יש פה יופי של כיסוי").
       - Confident ("סמכו עלי, ככה מוציאים את המקסימום").
       - Folksy but Professional ("חבל לשרוף את סל ההריון על ההתחלה, בואו נעשה תרגיל קטן").
    3. FORMATTING:
       - Use Emojis to make it friendly (🤰, 💸, ✅).
       - No complex tables unless absolutely necessary. Use bullet points.
       - No technical jargon like "Asset Protection". Translate it to simple advice.

    --- STRATEGY ENGINE ---
    EXECUTE THESE TACTICS IN EXACT ORDER:
    
    TACTIC A: "QUOTA STACKING" (EXHAUST RENEWABLES FIRST)
    *Rule:* Before touching any "Specific Bucket" (Category 2), ALWAYS exhaust "Generic Consultation" quotas (Category 1) if the service involves a doctor.
    - Check if we can use the "Consultation" quota (usually 3-4 per year) BEFORE using the pregnancy basket.
    - Check if splitting invoices between calendar years (Dec/Jan) helps renew the quota.

    TACTIC B: "THE SPECIFIC BUCKET"
    Only after Renewable Quotas are dry, use the "Specific Service" bucket (e.g., Pregnancy Basket).

    INSTRUCTION:
    When the user asks a question, process the logic internally, then output the response in this structure:

    1. **השורה התחתונה (The Bottom Line):**
       Start with a reassuring summary.
    2. **מה עושים בפועל (Action Plan):**
       Clear instructions on how to ask for the receipts.
       - "3 חשבוניות ראשונות: בקשו על שם X כ'ייעוץ'."
    3. **כמה כסף חוזר (The Money):**
       Simple breakdown showing the total expected refund vs cost.
    """
    
    model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

    # --- סרגל צד: העלאת מסמכים ---
    with st.sidebar:
        st.header("📂 המסמכים שלכם")
        uploaded_files = st.file_uploader("העלה פוליסות / קבלות (PDF)", type=["pdf"], accept_multiple_files=True)
        
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
                st.success(f"התקבלו {len(pdf_parts)} מסמכים. אני מוכן לנתח! 😎")

    # --- צ'אט ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "אהלן אוהד ועמית! 👋 תעלו לי את הפוליסות או החשבוניות, ואני אדאג שתוציאו את המקסימום מהביטוח."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("למשל: יש לי 13 ביקורים אצל רופא פרטי, איך להגיש אותם?")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        inputs = [user_input]
        if pdf_parts: inputs.extend(pdf_parts)
        
        with st.spinner("בונה אסטרטגיה להחזר מקסימלי... 🧠"):
            try:
                response = model.generate_content(inputs)
                st.chat_message("assistant").write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("אופס, משהו השתבש בחיבור. נסה שוב.")
