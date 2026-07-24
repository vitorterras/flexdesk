import streamlit as st
from services.resource_service import ResourceService
from repositories.database import DatabaseRepository

def render_resource_admin_view(resource_service: ResourceService, db: DatabaseRepository):
    st.subheader("🛠️ Gerenciamento de Recursos (UC005 / US005)")
    st.markdown("Painel administrativo para cadastrar, visualizar e desativar estações de trabalho e salas.")

    tab1, tab2 = st.tabs(["Recursos Cadastrados", "Novo Recurso"])

    with tab1:
        recursos = resource_service.listar_recursos(apenas_ativos=True)

        if not recursos:
            st.info("Nenhum recurso ativo encontrado.")
        else:
            for r in recursos:
                loc = db.get_localizacao_by_id(r.localizacao_id)
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.markdown(f"**{r.codigo_identificacao}** ({r.tipo})")
                    st.caption(f"Localização: {loc.nome if loc else 'N/A'} | Capacidade: {r.capacidade} pessoa(s)")
                with col2:
                    st.markdown('<span style="color: green; font-weight: bold;">● Ativo</span>', unsafe_allow_html=True)
                with col3:
                    if st.button("Remover", key=f"del_rec_{r.id}", type="secondary"):
                        sucesso, msg = resource_service.remover_recurso(r.id)
                        if sucesso:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                st.markdown("---")

    with tab2:
        st.markdown("##### Cadastrar Nova Estação ou Sala")
        localizacoes = db.get_localizacoes()
        loc_options = {l.id: f"{l.nome} (Andar {l.andar})" for l in localizacoes}

        with st.form("form_novo_recurso"):
            codigo = st.text_input("Código de Identificação (Ex: Mesa C-01, Sala 4B)", value="Mesa A-05")
            tipo = st.selectbox("Tipo de Recurso", ["Mesa", "Sala Reunião", "Cabine"])
            capacidade = st.number_input("Capacidade Máxima de Pessoas", min_value=1, value=1)
            loc_id = st.selectbox("Localização", list(loc_options.keys()), format_func=lambda x: loc_options[x])

            btn_salvar = st.form_submit_button("Cadastrar Recurso")

            if btn_salvar:
                sucesso, msg, recurso = resource_service.cadastrar_recurso(codigo, tipo, capacidade, loc_id)
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
