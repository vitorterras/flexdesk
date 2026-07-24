import streamlit as st
import pandas as pd
import plotly.express as px
from services.dashboard_service import DashboardService

def render_dashboard_view(dashboard_service: DashboardService):
    st.subheader("📊 Dashboards e Métricas de Ocupação (UC006 / US006)")
    st.markdown("Análise quantitativa do uso da infraestrutura do escritório em modo Dark Liquid Glass.")

    metricas = dashboard_service.calcular_metricas_ocupacao()

    # Métricas Globais (Cards)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Recursos", metricas["total_recursos"])
    with col2:
        st.metric("Reservas Registradas", metricas["total_reservas"])
    with col3:
        st.metric("Em Uso Agora", metricas["total_em_uso"])
    with col4:
        st.metric("Taxa de W.O. (No-Show)", f"{metricas['taxa_wo']}%")

    st.markdown("---")

    # Gráfico de Ocupação por Setor
    df_loc = pd.DataFrame(metricas["detalhes_localizacao"])
    if not df_loc.empty:
        st.markdown("##### Taxa Média de Ocupação por Setor / Andar")
        fig = px.bar(
            df_loc,
            x="Localização",
            y="Taxa de Ocupação Est. (%)",
            color="Localização",
            text="Taxa de Ocupação Est. (%)",
            template="plotly_dark",
            labels={"Taxa de Ocupação Est. (%)": "Ocupação (%)"}
        )
        fig.update_layout(
            showlegend=False,
            yaxis_range=[0, 100],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc")
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tabela detalhada e Exportação
    st.markdown("##### Relatório Geral de Reservas")
    df_exp = dashboard_service.gerar_dataframe_exportacao()
    st.dataframe(df_exp, use_container_width=True)

    # Botão de Exportação CSV
    csv_data = df_exp.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Relatório em CSV",
        data=csv_data,
        file_name="relatorio_ocupacao_flexdesk.csv",
        mime="text/csv",
        use_container_width=True
    )
