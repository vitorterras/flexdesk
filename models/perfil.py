from dataclasses import dataclass

@dataclass
class Perfil:
    id: int
    nome: str
    descricao: str

    PERFIL_COLABORADOR = "Colaborador"
    PERFIL_GESTOR = "Gestor"
