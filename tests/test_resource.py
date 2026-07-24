import pytest
from repositories.database import DatabaseRepository
from services.resource_service import ResourceService

@pytest.fixture
def resource_service():
    db = DatabaseRepository()
    db.reset_db()
    return ResourceService(db)

def test_cadastrar_recurso_sucesso(resource_service):
    """US005: Cadastra um novo recurso com sucesso."""
    sucesso, msg, recurso = resource_service.cadastrar_recurso("Mesa X-99", "Mesa", 1, 1)
    assert sucesso is True
    assert recurso is not None
    assert recurso.codigo_identificacao == "Mesa X-99"

def test_cadastrar_recurso_codigo_duplicado(resource_service):
    """US005/Extensão 4a: Rejeita cadastro com código existente."""
    sucesso, msg, recurso = resource_service.cadastrar_recurso("Mesa A-01", "Mesa", 1, 1)
    assert sucesso is False
    assert "Já existe um recurso cadastrado" in msg

def test_remover_recurso_com_reserva_ativa(resource_service):
    """US005/Extensão 6a: Impede remoção de recurso com reservas ativas."""
    # Mesa A-01 (id=1) possui reserva em uso no seed data
    sucesso, msg = resource_service.remover_recurso(1)
    assert sucesso is False
    assert "possui 1 reserva(s) ativa(s)" in msg
