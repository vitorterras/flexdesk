from dataclasses import dataclass

@dataclass
class Recurso:
    id: int
    codigo_identificacao: str
    tipo: str  # 'Mesa', 'Sala Reunião', 'Cabine'
    capacidade: int
    localizacao_id: int
    ativo: bool = True
