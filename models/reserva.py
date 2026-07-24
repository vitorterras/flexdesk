from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class StatusReserva:
    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    EM_USO = "Em Uso"
    CANCELADA = "Cancelada"
    WO = "W.O. (No-Show)"
    FINALIZADA = "Finalizada"

@dataclass
class Reserva:
    id: int
    usuario_id: int
    recurso_id: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status_reserva: str
    data_checkin: Optional[datetime] = None
