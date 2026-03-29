import streamlit as st
from config import URL_API
import requests as rq

if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        resposta_get = rq.get(f"{URL_API}/chat/get")
        if resposta_get.status_code == 200:
            conversa = resposta_get.json().get("conversa", [])
            for chat in conversa:
                st.session_state.messages.append({"role": "user", "content": chat["user_message"]})
                st.session_state.messages.append({"role": "assistant", "content": chat["agent_response"]})
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    st.title("Chat IA")

with col2:
    has_messages = len(st.session_state.messages) > 0
    if st.button("Limpar chat", use_container_width=True, type="secondary", disabled=not has_messages):
        with st.spinner("Limpando..."):
            try:
                rq.delete(f"{URL_API}/chat/clear")
                st.session_state.messages = []
            except Exception as e:
                st.error(f"Erro ao limpar chat: {e}")



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Pergunte algo sobre o currículo...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Pensando..."):
        try:
            url = f"{URL_API}/chat/send"
            payload = {"message": user_input}
            resposta_post = rq.post(url, json=payload)
            
            if resposta_post.status_code == 200:
                agent_response = resposta_post.json().get("response", "Sem resposta da API.")
                st.session_state.messages.append({"role": "assistant", "content": agent_response})
                st.rerun()
            else:
                st.error("Erro ao enviar mensagem.")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")


