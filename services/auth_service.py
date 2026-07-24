from typing import Tuple, Optional
import config
from models.usuario import Usuario
from models.perfil import Perfil
from repositories.database import DatabaseRepository

class AuthService:
    def __init__(self, db: Optional[DatabaseRepository] = None):
        self.db = db or DatabaseRepository()

    def validar_dominio_email(self, email: str) -> bool:
        if "@" not in email:
            return False
        domain = email.split("@")[1].lower()
        return domain in [d.lower() for d in config.ALLOWED_EMAIL_DOMAINS]

    def autenticar(self, email: str, senha: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        UC001: Autenticar Usuário.
        Retorna (sucesso, mensagem, objeto_usuario).
        """
        if not self.validar_dominio_email(email):
            return False, f"Domínio do e-mail não corporativo. Permitidos: {', '.join(config.ALLOWED_EMAIL_DOMAINS)}", None

        usuario = self.db.get_usuario_by_email(email)

        if not usuario:
            return False, "Credenciais incorretas ou usuário não cadastrado.", None

        if usuario.bloqueado:
            return False, "Conta bloqueada por excesso de tentativas incorretas. Entre em contato com o suporte.", None

        if not usuario.verificar_senha(senha):
            usuario.tentativas_falhas += 1
            if usuario.tentativas_falhas >= config.MAX_FAILED_LOGIN_ATTEMPTS:
                usuario.bloqueado = True
                return False, "Conta bloqueada após 5 tentativas incorretas.", None
            return False, "Credenciais incorretas.", None

        # Reset tentativas falhas em caso de sucesso
        usuario.tentativas_falhas = 0
        return True, "Autenticação realizada com sucesso.", usuario

    def cadastrar_usuario(self, nome: str, email: str, senha: str, perfil_id: int = 1) -> Tuple[bool, str, Optional[Usuario]]:
        if not self.validar_dominio_email(email):
            return False, f"E-mail deve ser institucional: {', '.join(config.ALLOWED_EMAIL_DOMAINS)}", None

        if len(senha) < config.MIN_PASSWORD_LENGTH:
            return False, f"A senha deve ter no mínimo {config.MIN_PASSWORD_LENGTH} caracteres.", None

        if self.db.get_usuario_by_email(email):
            return False, "E-mail já cadastrado no sistema.", None

        novo_usuario = Usuario(
            id=0,
            nome=nome,
            email=email,
            senha_hash=Usuario.hash_senha(senha),
            perfil_id=perfil_id
        )
        self.db.add_usuario(novo_usuario)
        return True, "Usuário cadastrado com sucesso.", novo_usuario
