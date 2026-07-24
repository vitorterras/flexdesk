import os

# Configurações de Segurança e Domínio
ALLOWED_EMAIL_DOMAINS = ["ufu.br", "empresa.com.br", "flexdesk.com"]
MIN_PASSWORD_LENGTH = 8
MAX_FAILED_LOGIN_ATTEMPTS = 5

# Regras de Negócio de Agendamento e Check-in
CHECKIN_TOLERANCE_MINUTES = 15
MAX_RESERVATION_HOURS_PER_DAY = 8

# Caminho do banco de dados (SQLite)
DB_PATH = os.path.join(os.path.dirname(__file__), "flexdesk.db")
