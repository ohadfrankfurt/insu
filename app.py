{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import google.generativeai as genai\
\
# \uc0\u1499 \u1493 \u1514 \u1512 \u1514  \u1492 \u1488 \u1508 \u1500 \u1497 \u1511 \u1510 \u1497 \u1492 \
st.title("\uc0\u1492 \u1510 '\u1488 \u1496  \u1513 \u1500 \u1497  \u1506 \u1501  Gemini")\
\
# \uc0\u1492 \u1490 \u1491 \u1512 \u1514  \u1492 \u1502 \u1508 \u1514 \u1495  - \u1492 \u1513 \u1493 \u1512 \u1492  \u1492 \u1494 \u1493  \u1502 \u1495 \u1508 \u1513 \u1514  \u1488 \u1514  \u1492 \u1505 \u1497 \u1505 \u1502 \u1492  \u1489 \u1514 \u1493 \u1498  \u1492 \u1492 \u1490 \u1491 \u1512 \u1493 \u1514  \u1513 \u1500  \u1492 \u1506 \u1504 \u1503 \
# \uc0\u1488 \u1501  \u1494 \u1492  \u1500 \u1488  \u1502 \u1493 \u1510 \u1488  \u1502 \u1508 \u1514 \u1495 , \u1494 \u1492  \u1497 \u1489 \u1511 \u1513  \u1502 \u1492 \u1502 \u1513 \u1514 \u1502 \u1513  \u1500 \u1492 \u1494 \u1497 \u1503  (\u1496 \u1493 \u1489  \u1500 \u1489 \u1491 \u1497 \u1511 \u1493 \u1514 )\
if "GOOGLE_API_KEY" in st.secrets:\
    api_key = st.secrets["GOOGLE_API_KEY"]\
else:\
    api_key = st.text_input("\uc0\u1504 \u1488  \u1500 \u1492 \u1494 \u1497 \u1503  \u1502 \u1508 \u1514 \u1495  API", type="password")\
\
if api_key:\
    # \uc0\u1495 \u1497 \u1489 \u1493 \u1512  \u1500 -Gemini\
    genai.configure(api_key=api_key)\
    model = genai.GenerativeModel('gemini-pro')\
\
    # \uc0\u1514 \u1497 \u1489 \u1514  \u1496 \u1511 \u1505 \u1496  \u1500 \u1502 \u1513 \u1514 \u1502 \u1513 \
    user_input = st.chat_input("\uc0\u1499 \u1514 \u1493 \u1489  \u1502 \u1513 \u1492 \u1493 ...")\
\
    # \uc0\u1492 \u1497 \u1505 \u1496 \u1493 \u1512 \u1497 \u1497 \u1514  \u1510 '\u1488 \u1496  (\u1499 \u1491 \u1497  \u1513 \u1492 \u1513 \u1497 \u1495 \u1492  \u1514 \u1497 \u1513 \u1502 \u1512  \u1506 \u1500  \u1492 \u1502 \u1505 \u1498 )\
    if "messages" not in st.session_state:\
        st.session_state.messages = []\
\
    # \uc0\u1492 \u1510 \u1490 \u1514  \u1492 \u1492 \u1497 \u1505 \u1496 \u1493 \u1512 \u1497 \u1492 \
    for msg in st.session_state.messages:\
        st.chat_message(msg["role"]).write(msg["content"])\
\
    # \uc0\u1496 \u1497 \u1508 \u1493 \u1500  \u1489 \u1492 \u1493 \u1491 \u1506 \u1492  \u1495 \u1491 \u1513 \u1492 \
    if user_input:\
        # \uc0\u1492 \u1510 \u1490 \u1514  \u1492 \u1493 \u1491 \u1506 \u1514  \u1492 \u1502 \u1513 \u1514 \u1502 \u1513 \
        st.chat_message("user").write(user_input)\
        st.session_state.messages.append(\{"role": "user", "content": user_input\})\
\
        # \uc0\u1511 \u1489 \u1500 \u1514  \u1514 \u1513 \u1493 \u1489 \u1492  \u1502 \u1492 -AI\
        response = model.generate_content(user_input)\
\
        # \uc0\u1492 \u1510 \u1490 \u1514  \u1492 \u1514 \u1513 \u1493 \u1489 \u1492 \
        st.chat_message("assistant").write(response.text)\
        st.session_state.messages.append(\{"role": "assistant", "content": response.text\})}