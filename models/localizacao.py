from dataclasses import dataclass

@dataclass
class Localizacao:
    id: int
    nome: str
    tipo: str  # Ex: 'Setor', 'Andar', 'Ala'
    andar: int
