import pytest
from repositories.database import DatabaseRepository
from services.auth_service import AuthService

@pytest.fixture
def auth_service():
    db = DatabaseRepository()
    db.reset_db()
    return AuthService(db)

def test_autenticacao_sucesso(auth_service):
    """US001: Valida login com e-mail corporativo e senha corretos."""
    sucesso, msg, usuario = auth_service.autenticar("ana@ufu.br", "senha1234")
    assert sucesso is True
    assert usuario is not None
    assert usuario.email == "ana@ufu.br"

def test_autenticacao_dominio_invalido(auth_service):
    """US001/Extensão 3a: Rejeita login com e-mail fora do domínio corporativo."""
    sucesso, msg, usuario = auth_service.autenticar("usuario@gmail.com", "senha1234")
    assert sucesso is False
    assert "Domínio do e-mail não corporativo" in msg

def test_autenticacao_senha_incorreta(auth_service):
    """US001/Extensão 4a: Rejeita login com senha incorreta."""
    sucesso, msg, usuario = auth_service.autenticar("ana@ufu.br", "senha_errada")
    assert sucesso is False
    assert "Credenciais incorretas" in msg

def test_bloqueio_conta_tentativas_excedidas(auth_service):
    """US001/Extensão 4b: Bloqueia conta após 5 tentativas incorretas."""
    email = "ana@ufu.br"
    for _ in range(5):
        auth_service.autenticar(email, "senha_errada")

    sucesso, msg, usuario = auth_service.autenticar(email, "senha1234")
    assert sucesso is False
    assert "bloqueada" in msg.lower()
