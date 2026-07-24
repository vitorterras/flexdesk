import streamlit as st
from repositories.database import DatabaseRepository
from services.auth_service import AuthService
from services.resource_service import ResourceService
from services.reservation_service import ReservationService
from services.dashboard_service import DashboardService

from ui.components import render_header, inject_liquid_glass_css
from ui.auth_ui import render_login_view
from ui.map_ui import render_map_view
from ui.reservation_ui import render_reservation_view
from ui.resource_admin_ui import render_resource_admin_view
from ui.dashboard_ui import render_dashboard_view

def main():
    st.set_page_config(
        page_title="FlexDesk - Gestão de Espaços Híbridos",
        page_icon="🏢",
        layout="wide"
    )

    # Injetar CSS do Tema Liquid Glass Dark Mode
    inject_liquid_glass_css()

    # Inicialização das Camadas (Injeção de Dependência)
    db = DatabaseRepository()
    auth_service = AuthService(db)
    resource_service = ResourceService(db)
    reservation_service = ReservationService(db)
    dashboard_service = DashboardService(db)

    # Processar W.O. automático no carregamento
    reservation_service.verificar_e_processar_wo()

    render_header()

    # Controle de Sessão de Usuário
    usuario_logado = st.session_state.get("usuario_logado")

    # Sidebar Navigation
    st.sidebar.title("📌 Navegação FlexDesk")

    if usuario_logado:
        perfil_nome = "Gestor de Facilities" if usuario_logado.perfil_id == 2 else "Colaborador"
        st.sidebar.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.12);
                padding: 16px;
                border-radius: 16px;
                margin-bottom: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            ">
                <div style="font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0.5px; margin-bottom: 4px;">SESSÃO ATIVA</div>
                <strong style="font-size: 16px; color: #f8fafc;">{usuario_logado.nome}</strong><br>
                <span style="font-size: 12px; color: #38bdf8; font-weight: 600;">{perfil_nome}</span>
            </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("🚪 Sair (Logout)", type="secondary"):
            st.session_state.pop("usuario_logado", None)
            st.rerun()

        st.sidebar.markdown("---")

        opcoes_menu = ["Mapa em Tempo Real", "Reservar Espaço"]
        if usuario_logado.perfil_id == 2:  # Perfil Gestor
            opcoes_menu.extend(["Gerenciar Recursos", "Dashboards & Relatórios"])

        # Página padrão/selecionada
        page_default = st.session_state.get("pagina_atual", "Mapa em Tempo Real")
        if page_default not in opcoes_menu:
            page_default = "Mapa em Tempo Real"

        idx_sel = opcoes_menu.index(page_default)
        pagina = st.sidebar.radio("Ir para:", opcoes_menu, index=idx_sel)
        st.session_state["pagina_atual"] = pagina

        if pagina == "Mapa em Tempo Real":
            render_map_view(reservation_service, db)
        elif pagina == "Reservar Espaço":
            render_reservation_view(reservation_service, db)
        elif pagina == "Gerenciar Recursos" and usuario_logado.perfil_id == 2:
            render_resource_admin_view(resource_service, db)
        elif pagina == "Dashboards & Relatórios" and usuario_logado.perfil_id == 2:
            render_dashboard_view(dashboard_service)
    else:
        st.sidebar.info("Efetue login no painel ao lado para liberar as funcionalidades do sistema.")
        render_login_view(auth_service)

if __name__ == "__main__":
    main()
