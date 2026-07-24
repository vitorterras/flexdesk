import hashlib
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str
    perfil_id: int
    tentativas_falhas: int = 0
    bloqueado: bool = False

    @staticmethod
    def hash_senha(senha: str) -> str:
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return self.senha_hash == self.hash_senha(senha)
