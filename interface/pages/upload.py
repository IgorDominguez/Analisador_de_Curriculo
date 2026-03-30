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
if 'mostrar_analise' not in st.session_state:
    st.session_state.mostrar_analise = "Não"
if 'analytics' not in st.session_state:
    st.session_state.analytics = None


def excluir_analise_callback():
    try:
        res = rq.delete(f"{URL_API}/upload/clear/analytics")
        if res.status_code == 200:
            st.session_state.analytics = []
            st.session_state.mostrar_analise = "Não"
    except Exception as e:
        st.session_state.erro_exclusao = str(e)


# ... resto do código ...



uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], key="file_upload")

if uploaded_file:
    btn_salvar_ir = st.button("Salvar currículo e ir para o chat", use_container_width=True)
    btn_salvar = st.button("Salvar", use_container_width=True)

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
                    st.session_state.analytics = None
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
                    st.session_state.analytics = None
                    st.success("Currículo salvo com sucesso!")
                else:
                    st.error(f"Erro ao salvar currículo: {res_send.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")


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
                    st.session_state.mostrar_analise = "Não"
                    st.session_state.analytics = None
                    st.rerun()
                else:
                    st.error("Erro ao excluir currículos.")
        
        if st.session_state.analytics is None:
            res_analytics = rq.get(f"{URL_API}/upload/get/analytics")
            if res_analytics.status_code == 200:
                st.session_state.analytics = res_analytics.json()
            else:
                st.session_state.analytics = []

        has_analysis = len(st.session_state.analytics) > 0
        
        if st.button("Analisar currículo", use_container_width=True, disabled=has_analysis):
            with st.spinner("Analisando..."):
                try:
                    res_resume = rq.get(f"{URL_API}/upload/resume")
                    if res_resume.status_code == 200:
                        st.session_state.analytics = None
                        st.session_state.mostrar_analise = "Sim"
                        st.rerun()
                    else:
                        st.error("Erro ao gerar análise.")
                except Exception as e:
                    st.error(f"Erro ao conectar: {e}")

        st.write("---")
        st.selectbox("Mostrar análise", ["Não", "Sim"], key="mostrar_analise")

        if st.session_state.mostrar_analise == "Sim":
            analytics = st.session_state.analytics
            if analytics:
                ana = analytics[0]
                m1, m2 = st.columns(2)
                m1.metric("Participante", ana["participante"])
                m2.metric("Idade", f"{ana['idade']} anos")
                
                st.subheader("LinkedIn")
                st.write(ana["linkedin"])
                st.subheader("GitHub")
                st.write(ana["github"])
                st.subheader("Resumo")
                st.write(ana["resumo"])

                st.button(
                    "Excluir análise", 
                    use_container_width=True, 
                    type="secondary", 
                    on_click=excluir_analise_callback
                )
                
                if "erro_exclusao" in st.session_state:
                    st.error(f"Erro ao excluir: {st.session_state.erro_exclusao}")
                    del st.session_state.erro_exclusao

            else:
                st.info("não há nenhuma análise no momento")



    else:
        st.info("Nenhum currículo salvo no momento.")
except Exception as e:
    st.error(f"Erro ao buscar currículos salvos: {e}")



