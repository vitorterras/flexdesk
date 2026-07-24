import pytest
from repositories.database import DatabaseRepository
from services.dashboard_service import DashboardService

@pytest.fixture
def dashboard_service():
    db = DatabaseRepository()
    db.reset_db()
    return DashboardService(db)

def test_calcular_metricas_ocupacao(dashboard_service):
    """US006: Valida cálculo de métricas de ocupação para dashboards."""
    metricas = dashboard_service.calcular_metricas_ocupacao()
    assert "total_recursos" in metricas
    assert metricas["total_recursos"] > 0
    assert "total_reservas" in metricas
    assert "taxa_wo" in metricas
    assert isinstance(metricas["detalhes_localizacao"], list)

def test_gerar_dataframe_exportacao(dashboard_service):
    """US006: Valida exportação de relatório para DataFrame/CSV."""
    df = dashboard_service.gerar_dataframe_exportacao()
    assert not df.empty
    assert "ID Reserva" in df.columns
    assert "Status" in df.columns
