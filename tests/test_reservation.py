import pytest
from datetime import datetime, timedelta
from repositories.database import DatabaseRepository
from services.reservation_service import ReservationService

@pytest.fixture
def reservation_service():
    db = DatabaseRepository()
    db.reset_db()
    return ReservationService(db)

def test_reservar_espaco_sucesso(reservation_service):
    """US003: Realiza reserva de espaço com sucesso."""
    agora = datetime.now()
    inicio = agora + timedelta(days=5, hours=2)
    fim = inicio + timedelta(hours=2)

    sucesso, msg, reserva = reservation_service.reservar_espaco(usuario_id=1, recurso_id=3, inicio=inicio, fim=fim)
    assert sucesso is True
    assert reserva is not None

def test_reservar_espaco_colisao_horario(reservation_service):
    """US003/Extensão 5a: Impede reservas sobrepostas no mesmo recurso."""
    agora = datetime.now()
    inicio = agora + timedelta(days=5, hours=2)
    fim = inicio + timedelta(hours=2)

    # Primeira reserva
    reservation_service.reservar_espaco(usuario_id=1, recurso_id=3, inicio=inicio, fim=fim)

    # Segunda reserva no mesmo período
    sucesso, msg, reserva = reservation_service.reservar_espaco(usuario_id=2, recurso_id=3, inicio=inicio + timedelta(minutes=30), fim=fim + timedelta(minutes=30))
    assert sucesso is False
    assert "já possui uma reserva ativa no período" in msg

def test_checkin_dentro_tolerancia(reservation_service):
    """US004: Efetua check-in com sucesso dentro da tolerância de 15 minutos."""
    agora = datetime.now()
    inicio = agora + timedelta(minutes=10)
    fim = inicio + timedelta(hours=2)

    # Criar reserva pendente
    _, _, reserva = reservation_service.reservar_espaco(usuario_id=1, recurso_id=3, inicio=inicio, fim=fim)

    # Tentar check-in 5 minutos antes do início (dentro da tolerância)
    momento_checkin = inicio - timedelta(minutes=5)
    sucesso, msg = reservation_service.efetuar_checkin(reserva.id, usuario_id=1, momento_atual=momento_checkin)
    assert sucesso is True
    assert "Check-in realizado com sucesso" in msg

def test_checkin_expirado_marcado_wo(reservation_service):
    """US004/Extensão 4b: Marca reserva como W.O. após expirar prazo de check-in."""
    agora = datetime.now()
    inicio = agora - timedelta(minutes=30)
    fim = inicio + timedelta(hours=2)

    # Criar reserva pendente que já passou do prazo
    _, _, reserva = reservation_service.reservar_espaco(usuario_id=1, recurso_id=3, inicio=inicio, fim=fim)

    # Tentar check-in 20 minutos após o início (prazo de 15 min estourado)
    momento_checkin = inicio + timedelta(minutes=20)
    sucesso, msg = reservation_service.efetuar_checkin(reserva.id, usuario_id=1, momento_atual=momento_checkin)
    assert sucesso is False
    assert "W.O." in msg
