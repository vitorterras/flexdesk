import streamlit as st
from services.auth_service import AuthService
from models.perfil import Perfil

def render_login_view(auth_service: AuthService):
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.15);
        ">
            <h3 style="margin: 0 0 10px 0; font-size: 24px; font-weight: 800; color: #ffffff;">🔑 Acesso Corporativo FlexDesk</h3>
            <p style="margin: 0; font-size: 14px; color: #94a3b8;">Entre com sua conta institucional para gerenciar e agendar estações de trabalho.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Entrar na Conta", "Criar Nova Conta"])

    with tab1:
        with st.form("form_login"):
            email = st.text_input("E-mail Corporativo", value="ana@ufu.br")
            senha = st.text_input("Senha de Acesso", type="password", value="senha1234")
            btn_entrar = st.form_submit_button("Acessar Painel")

            if btn_entrar:
                sucesso, msg, usuario = auth_service.autenticar(email, senha)
                if sucesso:
                    st.session_state["usuario_logado"] = usuario
                    st.success(f"Bem-vindo(a), {usuario.nome}!")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("""
            <div style="
                background: rgba(59, 130, 246, 0.08);
                border: 1px solid rgba(59, 130, 246, 0.25);
                border-radius: 16px;
                padding: 16px;
                margin-top: 20px;
            ">
                <div style="font-size: 12px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">💡 CREDENCIAIS DE TESTE RÁPIDO:</div>
                <div style="font-size: 13px; color: #e2e8f0;">
                    • <strong>Colaborador 1:</strong> <code>ana@ufu.br</code> | Senha: <code>senha1234</code><br>
                    • <strong>Colaborador 2:</strong> <code>bruno@empresa.com.br</code> | Senha: <code>senha1234</code><br>
                    • <strong>Gestor de Facilities:</strong> <code>carlos.gestor@ufu.br</code> | Senha: <code>admin1234</code>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo")
            email_cad = st.text_input("E-mail Corporativo (@ufu.br ou @empresa.com.br)")
            senha_cad = st.text_input("Senha (mínimo 8 caracteres)", type="password")
            perfil = st.selectbox("Perfil de Acesso", ["Colaborador", "Gestor de Facilities"])
            btn_cadastrar = st.form_submit_button("Cadastrar Usuário")

            if btn_cadastrar:
                perfil_id = 2 if perfil == "Gestor de Facilities" else 1
                sucesso, msg, user = auth_service.cadastrar_usuario(nome, email_cad, senha_cad, perfil_id)
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)
