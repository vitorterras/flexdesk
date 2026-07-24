from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict
import config
from models.reserva import Reserva, StatusReserva
from models.recurso import Recurso
from repositories.database import DatabaseRepository

class ReservationService:
    def __init__(self, db: Optional[DatabaseRepository] = None):
        self.db = db or DatabaseRepository()

    def verificar_e_processar_wo(self, momento_atual: Optional[datetime] = None) -> int:
        """
        Extensão 4b - W.O. (No-Show): Cancela reservas pendentes que passaram da janela de tolerance sem check-in.
        """
        agora = momento_atual or datetime.now()
        tolerancia = timedelta(minutes=config.CHECKIN_TOLERANCE_MINUTES)
        processadas = 0

        for r in self.db.get_reservas():
            if r.status_reserva == StatusReserva.PENDENTE:
                limite_checkin = r.data_hora_inicio + tolerancia
                if agora > limite_checkin:
                    r.status_reserva = StatusReserva.WO
                    processadas += 1

        return processadas

    def obter_status_recurso_em_tempo_real(self, recurso_id: int, momento_atual: Optional[datetime] = None) -> Dict[str, any]:
        """
        UC002: Visualizar Mapa em Tempo Real.
        Determina o status do recurso no momento especificado.
        Status retornado: 'LIVRE', 'RESERVADO', 'EM_USO'
        """
        agora = momento_atual or datetime.now()
        self.verificar_e_processar_wo(agora)

        for r in self.db.get_reservas():
            if r.recurso_id == recurso_id:
                if r.data_hora_inicio <= agora <= r.data_hora_fim:
                    if r.status_reserva == StatusReserva.EM_USO:
                        return {"status": "EM_USO", "reserva": r}
                    elif r.status_reserva == StatusReserva.PENDENTE:
                        return {"status": "RESERVADO", "reserva": r}

        return {"status": "LIVRE", "reserva": None}

    def reservar_espaco(self, usuario_id: int, recurso_id: int, inicio: datetime, fim: datetime) -> Tuple[bool, str, Optional[Reserva]]:
        """
        UC003: Reservar Espaço.
        Valida regras de horário, limite diário e sobreposição de reservas.
        """
        if inicio >= fim:
            return False, "A hora de início deve ser anterior à hora de término.", None

        duracao_horas = (fim - inicio).total_seconds() / 3600.0
        if duracao_horas > config.MAX_RESERVATION_HOURS_PER_DAY:
            return False, f"A duração da reserva excede o limite máximo de {config.MAX_RESERVATION_HOURS_PER_DAY} horas por dia.", None

        recurso = self.db.get_recurso_by_id(recurso_id)
        if not recurso or not recurso.ativo:
            return False, "Recurso indisponível ou inexistente.", None

        # Validação de sobreposição (Colisão de horário)
        for r in self.db.get_reservas():
            if r.recurso_id == recurso_id and r.status_reserva in [StatusReserva.PENDENTE, StatusReserva.EM_USO, StatusReserva.CONFIRMADA]:
                # Houve sobreposição se max(inicio1, inicio2) < min(fim1, fim2)
                if max(inicio, r.data_hora_inicio) < min(fim, r.data_hora_fim):
                    return False, f"O recurso '{recurso.codigo_identificacao}' já possui uma reserva ativa no período informado.", None

        nova_reserva = Reserva(
            id=0,
            usuario_id=usuario_id,
            recurso_id=recurso_id,
            data_hora_inicio=inicio,
            data_hora_fim=fim,
            status_reserva=StatusReserva.PENDENTE
        )
        self.db.add_reserva(nova_reserva)
        return True, "Reserva realizada com sucesso!", nova_reserva

    def efetuar_checkin(self, reserva_id: int, usuario_id: int, momento_atual: Optional[datetime] = None) -> Tuple[bool, str]:
        """
        UC004: Efetuar Check-in.
        Valida a janela de tolerância (15 min antes/depois do início).
        """
        agora = momento_atual or datetime.now()
        reserva = self.db.get_reserva_by_id(reserva_id)

        if not reserva:
            return False, "Reserva não encontrada."

        if reserva.usuario_id != usuario_id:
            return False, "Esta reserva não pertence ao usuário logado."

        if reserva.status_reserva == StatusReserva.EM_USO:
            return False, "Check-in já foi realizado para esta reserva."

        if reserva.status_reserva == StatusReserva.WO:
            return False, "Reserva foi cancelada por W.O. (No-Show) por ter excedido a tolerância de 15 minutos."

        if reserva.status_reserva != StatusReserva.PENDENTE:
            return False, f"Status atual da reserva ({reserva.status_reserva}) não permite check-in."

        tolerancia = timedelta(minutes=config.CHECKIN_TOLERANCE_MINUTES)
        inicio_janela = reserva.data_hora_inicio - tolerancia
        fim_janela = reserva.data_hora_inicio + tolerancia

        if agora < inicio_janela:
            minutos_restantes = int((inicio_janela - agora).total_seconds() / 60)
            return False, f"Muito cedo para check-in. O check-in abre 15 minutos antes do início ({inicio_janela.strftime('%H:%M')})."

        if agora > fim_janela:
            reserva.status_reserva = StatusReserva.WO
            return False, "Prazo de check-in expirado. Reserva marcada como W.O. (No-Show)."

        reserva.status_reserva = StatusReserva.EM_USO
        reserva.data_checkin = agora
        return True, "Check-in realizado com sucesso! Bom trabalho!"

    def listar_reservas_usuario(self, usuario_id: int) -> List[Reserva]:
        return [r for r in self.db.get_reservas() if r.usuario_id == usuario_id]
