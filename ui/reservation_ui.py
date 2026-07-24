import streamlit as st
from datetime import datetime, timedelta, time
from services.reservation_service import ReservationService
from repositories.database import DatabaseRepository
from ui.components import render_status_badge

def render_reservation_view(reservation_service: ReservationService, db: DatabaseRepository):
    st.subheader("📅 Agendamento & Check-in de Espaços (UC003 & UC004 / US003 & US004)")

    tab1, tab2 = st.tabs(["Nova Reserva", "Meus Agendamentos"])

    usuario_atual = st.session_state.get("usuario_logado")
    if not usuario_atual:
        st.warning("Efetue login para gerenciar reservas.")
        return

    with tab1:
        st.markdown("##### Preencha os dados do agendamento")
        recursos = db.get_recursos(apenas_ativos=True)
        rec_options = {r.id: f"{r.codigo_identificacao} ({r.tipo})" for r in recursos}

        idx_default = 0
        if "recurso_selecionado_id" in st.session_state and st.session_state["recurso_selecionado_id"] in rec_options:
            idx_default = list(rec_options.keys()).index(st.session_state["recurso_selecionado_id"])

        recurso_id = st.selectbox("Recurso:", list(rec_options.keys()), index=idx_default, format_func=lambda x: rec_options[x])

        col1, col2, col3 = st.columns(3)
        with col1:
            data_reserva = st.date_input("Data:", datetime.now())
        with col2:
            hora_inicio = st.time_input("Horário Início:", time(hour=9, minute=0))
        with col3:
            hora_fim = st.time_input("Horário Término:", time(hour=11, minute=0))

        if st.button("Confirmar Reserva", type="primary", use_container_width=True):
            dt_inicio = datetime.combine(data_reserva, hora_inicio)
            dt_fim = datetime.combine(data_reserva, hora_fim)

            sucesso, msg, reserva = reservation_service.reservar_espaco(usuario_atual.id, recurso_id, dt_inicio, dt_fim)
            if sucesso:
                st.success(msg)
                st.session_state.pop("recurso_selecionado_id", None)
            else:
                st.error(msg)

    with tab2:
        st.markdown("##### Histórico e Próximas Reservas")
        reservas_user = reservation_service.listar_reservas_usuario(usuario_atual.id)

        if not reservas_user:
            st.info("Você ainda não possui agendamentos.")
            return

        for r in reversed(reservas_user):
            recurso = db.get_recurso_by_id(r.recurso_id)
            loc = db.get_localizacao_by_id(recurso.localizacao_id) if recurso else None

            st.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(16px);
                    -webkit-backdrop-filter: blur(16px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 18px;
                    padding: 18px;
                    margin-bottom: 16px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-size: 16px; color: #ffffff;">{recurso.codigo_identificacao if recurso else 'Recurso'}</strong>
                            <span style="font-size: 13px; color: #94a3b8; margin-left: 8px;">({loc.nome if loc else ''})</span>
                            <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">
                                🕒 {r.data_hora_inicio.strftime('%d/%m/%Y %H:%M')} às {r.data_hora_fim.strftime('%H:%M')}
                            </div>
                        </div>
                        <div>
                            {render_status_badge(r.status_reserva)}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if r.status_reserva == "Pendente":
                if st.button("Efetuar Check-in", key=f"ck_tab_{r.id}", use_container_width=True):
                    sucesso, msg = reservation_service.efetuar_checkin(r.id, usuario_atual.id)
                    if sucesso:
                        st.success(msg)
                    else:
                        st.error(msg)
                    st.rerun()
