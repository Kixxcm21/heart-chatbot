import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# 載入 .env 中的 OpenAI 金鑰（若有）
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# 初始化 LLM
chat = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# Streamlit 頁面設定
st.set_page_config(page_title="心語對話", page_icon="🌿")
st.title("🌿 與心語對話")
st.markdown("💬 和心語聊聊今天的心情，讓它陪你一起走過 🌱")

# 初始 Prompt 設定
system_prompt = SystemMessage(content="""
你是一位溫柔、善解人意的心理對話夥伴，名為「心語」。
請用簡單平實的口吻與使用者對話，鼓勵他們表達情緒、探索想法。
避免直接給出建議，請多用開放式問題引導對話。
不進行心理診斷或治療，僅作為情緒陪伴。
""")

# 初始化對話紀錄（Session State）
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_prompt]

# 顯示歷史訊息
for msg in st.session_state.chat_history[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# 使用者輸入訊息
user_input = st.chat_input("今天想聊什麼呢？")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = chat(st.session_state.chat_history)
        st.markdown(response.content)
        st.session_state.chat_history.append(AIMessage(content=response.content))

""")
