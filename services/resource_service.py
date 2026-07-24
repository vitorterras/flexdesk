from typing import List, Tuple, Optional
from models.recurso import Recurso
from models.reserva import StatusReserva
from repositories.database import DatabaseRepository

class ResourceService:
    def __init__(self, db: Optional[DatabaseRepository] = None):
        self.db = db or DatabaseRepository()

    def listar_recursos(self, apenas_ativos: bool = True) -> List[Recurso]:
        return self.db.get_recursos(apenas_ativos=apenas_ativos)

    def cadastrar_recurso(self, codigo: str, tipo: str, capacidade: int, localizacao_id: int) -> Tuple[bool, str, Optional[Recurso]]:
        """
        UC005: Gerenciar Recursos - Cadastrar.
        """
        if not codigo or not codigo.strip():
            return False, "O código de identificação é obrigatório.", None

        if self.db.get_recurso_by_codigo(codigo.strip()):
            return False, f"Já existe um recurso cadastrado com o código '{codigo}'.", None

        if capacidade < 1:
            return False, "Capacidade deve ser de no mínimo 1 pessoa.", None

        if not self.db.get_localizacao_by_id(localizacao_id):
            return False, "Localização informada não existe.", None

        recurso = Recurso(
            id=0,
            codigo_identificacao=codigo.strip(),
            tipo=tipo,
            capacidade=capacidade,
            localizacao_id=localizacao_id,
            ativo=True
        )
        self.db.add_recurso(recurso)
        return True, "Recurso cadastrado com sucesso.", recurso

    def remover_recurso(self, recurso_id: int) -> Tuple[bool, str]:
        """
        UC005: Gerenciar Recursos - Remover.
        Verifica se existem reservas futuras ativas para impedir exclusão inconsistente.
        """
        recurso = self.db.get_recurso_by_id(recurso_id)
        if not recurso:
            return False, "Recurso não encontrado."

        # Verificar se possui reservas ativas/pendentes
        reservas = self.db.get_reservas()
        reservas_ativas = [
            res for res in reservas
            if res.recurso_id == recurso_id and res.status_reserva in [StatusReserva.PENDENTE, StatusReserva.EM_USO, StatusReserva.CONFIRMADA]
        ]

        if reservas_ativas:
            return False, f"Não é possível remover o recurso '{recurso.codigo_identificacao}' pois possui {len(reservas_ativas)} reserva(s) ativa(s) ou pendente(s)."

        self.db.remove_recurso(recurso_id)
        return True, f"Recurso '{recurso.codigo_identificacao}' desativado com sucesso."
