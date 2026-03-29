import streamlit as st
from config import URL_API
import requests as rq
import os

st.title("Analisador de currículo")

if 'analisado' not in st.session_state:
    st.session_state.analisado = False
if 'infos' not in st.session_state:
    st.session_state.infos = None
if 'curriculos_salvos' not in st.session_state:
    st.session_state.curriculos_salvos = None


uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], key="file_upload")

if uploaded_file and not st.session_state.analisado:
    btn_analisar = st.button("Analisar currículo", use_container_width=True)
    btn_salvar_ir = st.button("Salvar currículo e ir para o chat", use_container_width=True)
    btn_salvar = st.button("Salvar", use_container_width=True)

    if btn_analisar:
        with st.spinner("Analisando currículo..."):
            binary_data = uploaded_file.getvalue()
            try:
                res_send = rq.post(
                    f"{URL_API}/upload/send", 
                    files={"file": (uploaded_file.name, binary_data, "application/pdf")}
                )
                
                if res_send.status_code == 200:
                    st.session_state.curriculos_salvos = None
                    res_resume = rq.get(f"{URL_API}/upload/resume")
                    
                    if res_resume.status_code == 200:
                        st.session_state.infos = res_resume.json()
                        st.session_state.analisado = True
                        st.rerun()
                    else:
                        st.error("Erro ao gerar resumo do currículo.")
                else:
                    st.error(f"Erro no upload: {res_send.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

    if btn_salvar_ir:
        with st.spinner("Salvando e redirecionando..."):
            binary_data = uploaded_file.getvalue()
            try:
                res_send = rq.post(
                    f"{URL_API}/upload/send", 
                    files={"file": (uploaded_file.name, binary_data, "application/pdf")}
                )
                
                if res_send.status_code == 200:
                    st.session_state.curriculos_salvos = None
                    st.switch_page("pages/chat.py")
                else:
                    st.error(f"Erro ao salvar currículo: {res_send.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

    if btn_salvar:
        with st.spinner("Salvando..."):
            binary_data = uploaded_file.getvalue()
            try:
                res_send = rq.post(
                    f"{URL_API}/upload/send", 
                    files={"file": (uploaded_file.name, binary_data, "application/pdf")}
                )
                
                if res_send.status_code == 200:
                    st.session_state.curriculos_salvos = None
                    st.success("Currículo salvo com sucesso!")
                else:
                    st.error(f"Erro ao salvar currículo: {res_send.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")



if st.session_state.analisado:
    infos = st.session_state.infos
    
    with st.form("meu_formulario"):
        st.write("# Dados do Participante")
        st.subheader(f"Participante: \n*{infos['nome']}*")
        st.subheader(f"Idade: \n*{infos['idade']}*")
        st.subheader(f"LinkedIn: \n*{infos['linkedin']}*")
        st.subheader(f"GitHub: \n*{infos['github']}*")
        st.subheader(f"Resumo: \n*{infos['resumo']}*")

        submit = st.form_submit_button("Ir para o chat", use_container_width=True, type="primary")
        
        if submit:
            st.switch_page("pages/chat.py")

st.divider()
st.subheader("PDF salvo")

try:
    if st.session_state.curriculos_salvos is None:
        with st.spinner("Buscando PDF..."):
            res_get = rq.get(f"{URL_API}/upload/get")
            if res_get.status_code == 200:
                st.session_state.curriculos_salvos = res_get.json()
            else:
                st.session_state.curriculos_salvos = []

    curriculos = st.session_state.curriculos_salvos
    if curriculos:
        for c in curriculos:
            st.write(f"📄 **{c['titulo']}**")
        
        if st.button("Excluir currículo", type="primary", use_container_width=True):
            with st.spinner("Excluindo..."):
                res_clear = rq.delete(f"{URL_API}/upload/clear")
                if res_clear.status_code == 200:
                    st.session_state.analisado = False
                    st.session_state.infos = None
                    st.session_state.curriculos_salvos = []
                    st.rerun()
                else:
                    st.error("Erro ao excluir currículos.")
    else:
        st.info("Nenhum currículo salvo no momento.")
except Exception as e:
    st.error(f"Erro ao buscar currículos salvos: {e}")

