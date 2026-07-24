from datetime import datetime, timedelta
from typing import List, Optional
from models.perfil import Perfil
from models.usuario import Usuario
from models.localizacao import Localizacao
from models.recurso import Recurso
from models.reserva import Reserva, StatusReserva

class DatabaseRepository:
    """
    Repositório de dados em memória/SQLite para gerenciar persistência de entidades do FlexDesk.
    Fornece inicialização com dados de demonstração (seed data).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseRepository, cls).__new__(cls)
            cls._instance._init_database()
        return cls._instance

    def reset_db(self):
        """Reinicia o banco de dados para estado inicial (útil para testes)."""
        self._init_database()

    def _init_database(self):
        self.perfis: List[Perfil] = [
            Perfil(id=1, nome=Perfil.PERFIL_COLABORADOR, descricao="Acesso a reservas e mapas"),
            Perfil(id=2, nome=Perfil.PERFIL_GESTOR, descricao="Gestão de recursos e dashboards")
        ]

        self.usuarios: List[Usuario] = [
            Usuario(
                id=1,
                nome="Ana Colaboradora",
                email="ana@ufu.br",
                senha_hash=Usuario.hash_senha("senha1234"),
                perfil_id=1
            ),
            Usuario(
                id=2,
                nome="Bruno Colaborador",
                email="bruno@empresa.com.br",
                senha_hash=Usuario.hash_senha("senha1234"),
                perfil_id=1
            ),
            Usuario(
                id=3,
                nome="Carlos Gestor Facilities",
                email="carlos.gestor@ufu.br",
                senha_hash=Usuario.hash_senha("admin1234"),
                perfil_id=2
            )
        ]

        self.localizacoes: List[Localizacao] = [
            Localizacao(id=1, nome="Ala A - Open Space", tipo="Setor", andar=1),
            Localizacao(id=2, nome="Ala B - Reuniões & Cabines", tipo="Setor", andar=1),
            Localizacao(id=3, nome="Andar 2 - Executive", tipo="Andar", andar=2),
        ]

        self.recursos: List[Recurso] = [
            Recurso(id=1, codigo_identificacao="Mesa A-01", tipo="Mesa", capacidade=1, localizacao_id=1),
            Recurso(id=2, codigo_identificacao="Mesa A-02", tipo="Mesa", capacidade=1, localizacao_id=1),
            Recurso(id=3, codigo_identificacao="Mesa A-03", tipo="Mesa", capacidade=1, localizacao_id=1),
            Recurso(id=4, codigo_identificacao="Mesa A-04", tipo="Mesa", capacidade=1, localizacao_id=1),
            Recurso(id=5, codigo_identificacao="Sala Reunião 1", tipo="Sala Reunião", capacidade=8, localizacao_id=2),
            Recurso(id=6, codigo_identificacao="Cabine Call 1", tipo="Cabine", capacidade=1, localizacao_id=2),
            Recurso(id=7, codigo_identificacao="Mesa B-01 (Andar 2)", tipo="Mesa", capacidade=1, localizacao_id=3),
        ]

        agora = datetime.now()
        inicio_hoje = agora.replace(hour=9, minute=0, second=0, microsecond=0)
        fim_hoje = agora.replace(hour=12, minute=0, second=0, microsecond=0)

        self.reservas: List[Reserva] = [
            # Reserva ocupada no momento por Ana na Mesa A-01
            Reserva(
                id=1,
                usuario_id=1,
                recurso_id=1,
                data_hora_inicio=agora - timedelta(minutes=30),
                data_hora_fim=agora + timedelta(hours=2),
                status_reserva=StatusReserva.EM_USO,
                data_checkin=agora - timedelta(minutes=25)
            ),
            # Reserva pendente para Bruno na Mesa A-04
            Reserva(
                id=2,
                usuario_id=2,
                recurso_id=4,
                data_hora_inicio=agora - timedelta(minutes=5),
                data_hora_fim=agora + timedelta(hours=3),
                status_reserva=StatusReserva.PENDENTE
            ),
            # Histórico de reservas passadas para relatórios
            Reserva(
                id=3,
                usuario_id=1,
                recurso_id=5,
                data_hora_inicio=agora - timedelta(days=1, hours=4),
                data_hora_fim=agora - timedelta(days=1, hours=2),
                status_reserva=StatusReserva.FINALIZADA,
                data_checkin=agora - timedelta(days=1, hours=4)
            ),
            Reserva(
                id=4,
                usuario_id=2,
                recurso_id=2,
                data_hora_inicio=agora - timedelta(days=2, hours=3),
                data_hora_fim=agora - timedelta(days=2, hours=1),
                status_reserva=StatusReserva.WO
            )
        ]

    # --- Consultas de Usuário ---
    def get_usuario_by_email(self, email: str) -> Optional[Usuario]:
        for u in self.usuarios:
            if u.email.lower() == email.lower():
                return u
        return None

    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        for u in self.usuarios:
            if u.id == usuario_id:
                return u
        return None

    def add_usuario(self, usuario: Usuario) -> Usuario:
        if not usuario.id:
            usuario.id = max([u.id for u in self.usuarios], default=0) + 1
        self.usuarios.append(usuario)
        return usuario

    # --- Consultas de Perfil ---
    def get_perfil_by_id(self, perfil_id: int) -> Optional[Perfil]:
        for p in self.perfis:
            if p.id == perfil_id:
                return p
        return None

    # --- Consultas de Localizacao ---
    def get_localizacoes(self) -> List[Localizacao]:
        return self.localizacoes

    def get_localizacao_by_id(self, loc_id: int) -> Optional[Localizacao]:
        for l in self.localizacoes:
            if l.id == loc_id:
                return l
        return None

    # --- Consultas de Recurso ---
    def get_recursos(self, apenas_ativos: bool = True) -> List[Recurso]:
        if apenas_ativos:
            return [r for r in self.recursos if r.ativo]
        return self.recursos

    def get_recurso_by_id(self, recurso_id: int) -> Optional[Recurso]:
        for r in self.recursos:
            if r.id == recurso_id:
                return r
        return None

    def get_recurso_by_codigo(self, codigo: str) -> Optional[Recurso]:
        for r in self.recursos:
            if r.codigo_identificacao.lower() == codigo.lower():
                return r
        return None

    def add_recurso(self, recurso: Recurso) -> Recurso:
        if not recurso.id:
            recurso.id = max([r.id for r in self.recursos], default=0) + 1
        self.recursos.append(recurso)
        return recurso

    def remove_recurso(self, recurso_id: int) -> bool:
        r = self.get_recurso_by_id(recurso_id)
        if r:
            r.ativo = False
            return True
        return False

    # --- Consultas de Reserva ---
    def get_reservas(self) -> List[Reserva]:
        return self.reservas

    def get_reserva_by_id(self, reserva_id: int) -> Optional[Reserva]:
        for r in self.reservas:
            if r.id == reserva_id:
                return r
        return None

    def add_reserva(self, reserva: Reserva) -> Reserva:
        if not reserva.id:
            reserva.id = max([r.id for r in self.reservas], default=0) + 1
        self.reservas.append(reserva)
        return reserva
