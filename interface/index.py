# streamlit run index.py

import streamlit as st

st.set_page_config(
    page_title="Analisador de Currículo",
    page_icon="📄"
)

# Definição das páginas
upload_page = st.Page("pages/upload.py", title="Upload e Análise", default=True)
chat_page = st.Page("pages/chat.py", title="Chat com IA")

# Gerenciador de Navegação
pg = st.navigation([upload_page, chat_page])
pg.run()
