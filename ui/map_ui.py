import streamlit as st
from datetime import datetime, timedelta
from services.reservation_service import ReservationService
from repositories.database import DatabaseRepository
from ui.components import render_status_badge

def render_map_view(reservation_service: ReservationService, db: DatabaseRepository):
    st.subheader("🗺️ Mapa do Escritório em Tempo Real (UC002 / US002)")
    st.markdown("Visualização interativa da ocupação de estações de trabalho e salas no horário atual com design Liquid Glass.")

    localizacoes = db.get_localizacoes()
    loc_options = {l.id: f"{l.nome} (Andar {l.andar})" for l in localizacoes}
    loc_id = st.selectbox("Selecione a Localização / Setor:", list(loc_options.keys()), format_func=lambda x: loc_options[x])

    recursos = [r for r in db.get_recursos(apenas_ativos=True) if r.localizacao_id == loc_id]

    if not recursos:
        st.info("Nenhum recurso cadastrado nesta localização.")
        return

    st.markdown("---")

    # Grid de Recursos (Cards no estilo Liquid Glass)
    cols = st.columns(3)
    usuario_atual = st.session_state.get("usuario_logado")

    for i, r in enumerate(recursos):
        col = cols[i % 3]
        status_info = reservation_service.obter_status_recurso_em_tempo_real(r.id)
        status = status_info["status"]
        reserva = status_info["reserva"]

        with col:
            accent_glow = "rgba(16, 185, 129, 0.2)" if status == "LIVRE" else ("rgba(244, 63, 94, 0.2)" if status == "EM_USO" else "rgba(59, 130, 246, 0.2)")
            accent_border = "rgba(16, 185, 129, 0.4)" if status == "LIVRE" else ("rgba(244, 63, 94, 0.4)" if status == "EM_USO" else "rgba(59, 130, 246, 0.4)")

            st.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.04);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border: 1px solid {accent_border};
                    border-radius: 20px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1), 0 0 20px {accent_glow};
                    transition: all 0.3s ease;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                        <div>
                            <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #ffffff;">{r.codigo_identificacao}</h4>
                            <span style="font-size: 12px; color: #94a3b8; font-weight: 500;">{r.tipo}</span>
                        </div>
                        {render_status_badge(status)}
                    </div>
                    
                    <div style="
                        background: rgba(15, 23, 42, 0.5);
                        border-radius: 12px;
                        padding: 10px 14px;
                        margin-top: 10px;
                        border: 1px solid rgba(255,255,255,0.06);
                    ">
                        <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">CAPACIDADE</div>
                        <div style="font-size: 14px; font-weight: 700; color: #e2e8f0;">👤 {r.capacidade} pessoa(s)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if status == "LIVRE":
                if st.button(f"📅 Reservar {r.codigo_identificacao}", key=f"btn_res_{r.id}", use_container_width=True):
                    st.session_state["recurso_selecionado_id"] = r.id
                    st.session_state["pagina_atual"] = "Reservar Espaço"
                    st.rerun()
            elif status in ["RESERVADO", "EM_USO"] and reserva:
                if usuario_atual and reserva.usuario_id == usuario_atual.id and status == "RESERVADO":
                    if st.button(f"✅ Check-in {r.codigo_identificacao}", key=f"btn_ck_{r.id}", use_container_width=True):
                        sucesso, msg = reservation_service.efetuar_checkin(reserva.id, usuario_atual.id)
                        if sucesso:
                            st.success(msg)
                        else:
                            st.error(msg)
                        st.rerun()
