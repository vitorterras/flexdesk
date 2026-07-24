from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from repositories.database import DatabaseRepository
from services.auth_service import AuthService
from services.resource_service import ResourceService
from services.reservation_service import ReservationService
from services.dashboard_service import DashboardService

app = FastAPI(title="FlexDesk API", version="2.0.0")

# Habilitar CORS para o Frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização de Serviços e Banco de Dados
db = DatabaseRepository()
auth_service = AuthService(db)
resource_service = ResourceService(db)
reservation_service = ReservationService(db)
dashboard_service = DashboardService(db)

# --- Schemas Pydantic ---
class LoginRequest(BaseModel):
    email: str
    senha: str

class RegisterRequest(BaseModel):
    nome: str
    email: str
    senha: str
    perfil_id: int = 1

class CreateResourceRequest(BaseModel):
    codigo: str
    tipo: str
    capacidade: int
    localizacao_id: int

class CreateReservationRequest(BaseModel):
    usuario_id: int
    recurso_id: int
    data_hora_inicio: str  # ISO string
    data_hora_fim: str     # ISO string

# --- Endpoints de Autenticação (US001/UC001) ---
@app.post("/api/auth/login")
def login(req: LoginRequest):
    sucesso, msg, usuario = auth_service.autenticar(req.email, req.senha)
    if not sucesso or not usuario:
        raise HTTPException(status_code=400, detail=msg)
    
    perfil = db.get_perfil_by_id(usuario.perfil_id)
    return {
        "success": True,
        "message": msg,
        "user": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil_id": usuario.perfil_id,
            "perfil_nome": perfil.nome if perfil else "Colaborador"
        }
    }

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    sucesso, msg, usuario = auth_service.cadastrar_usuario(req.nome, req.email, req.senha, req.perfil_id)
    if not sucesso or not usuario:
        raise HTTPException(status_code=400, detail=msg)
    
    perfil = db.get_perfil_by_id(usuario.perfil_id)
    return {
        "success": True,
        "message": msg,
        "user": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil_id": usuario.perfil_id,
            "perfil_nome": perfil.nome if perfil else "Colaborador"
        }
    }

# --- Endpoints de Localização e Recursos (US002, US005/UC002, UC005) ---
@app.get("/api/locations")
def get_locations():
    locs = db.get_localizacoes()
    return [{"id": l.id, "nome": l.nome, "tipo": l.tipo, "andar": l.andar} for l in locs]

@app.get("/api/resources")
def get_resources(location_id: Optional[int] = None):
    # Processar W.O. antes de consultar status
    reservation_service.verificar_e_processar_wo()
    
    recursos = resource_service.listar_recursos(apenas_ativos=True)
    if location_id:
        recursos = [r for r in recursos if r.localizacao_id == location_id]
        
    resultado = []
    for r in recursos:
        status_info = reservation_service.obter_status_recurso_em_tempo_real(r.id)
        loc = db.get_localizacao_by_id(r.localizacao_id)
        res = status_info["reserva"]
        
        resultado.append({
            "id": r.id,
            "codigo_identificacao": r.codigo_identificacao,
            "tipo": r.tipo,
            "capacidade": r.capacidade,
            "localizacao_id": r.localizacao_id,
            "localizacao_nome": loc.nome if loc else "",
            "status": status_info["status"],
            "reserva_atual": {
                "id": res.id,
                "usuario_id": res.usuario_id,
                "inicio": res.data_hora_inicio.isoformat(),
                "fim": res.data_hora_fim.isoformat(),
                "status_reserva": res.status_reserva
            } if res else None
        })
    return resultado

@app.post("/api/resources")
def create_resource(req: CreateResourceRequest):
    sucesso, msg, recurso = resource_service.cadastrar_recurso(req.codigo, req.tipo, req.capacidade, req.localizacao_id)
    if not sucesso or not recurso:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "message": msg, "recurso_id": recurso.id}

@app.delete("/api/resources/{recurso_id}")
def delete_resource(recurso_id: int):
    sucesso, msg = resource_service.remover_recurso(recurso_id)
    if not sucesso:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "message": msg}

# --- Endpoints de Reserva e Check-in (US003, US004/UC003, UC004) ---
@app.get("/api/reservations/user/{usuario_id}")
def get_user_reservations(usuario_id: int):
    reservation_service.verificar_e_processar_wo()
    reservas = reservation_service.listar_reservas_usuario(usuario_id)
    resultado = []
    for r in reversed(reservas):
        rec = db.get_recurso_by_id(r.recurso_id)
        loc = db.get_localizacao_by_id(rec.localizacao_id) if rec else None
        resultado.append({
            "id": r.id,
            "recurso_id": r.recurso_id,
            "recurso_codigo": rec.codigo_identificacao if rec else "N/A",
            "recurso_tipo": rec.tipo if rec else "N/A",
            "localizacao_nome": loc.nome if loc else "N/A",
            "inicio": r.data_hora_inicio.isoformat(),
            "fim": r.data_hora_fim.isoformat(),
            "status": r.status_reserva,
            "checkin": r.data_checkin.isoformat() if r.data_checkin else None
        })
    return resultado

@app.post("/api/reservations")
def create_reservation(req: CreateReservationRequest):
    try:
        dt_inicio = datetime.fromisoformat(req.data_hora_inicio)
        dt_fim = datetime.fromisoformat(req.data_hora_fim)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data/hora inválido.")

    sucesso, msg, reserva = reservation_service.reservar_espaco(req.usuario_id, req.recurso_id, dt_inicio, dt_fim)
    if not sucesso or not reserva:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "message": msg, "reserva_id": reserva.id}

@app.post("/api/reservations/{reserva_id}/checkin")
def do_checkin(reserva_id: int, usuario_id: int = Query(...)):
    sucesso, msg = reservation_service.efetuar_checkin(reserva_id, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "message": msg}

# --- Endpoints de Dashboards (US006/UC006) ---
@app.get("/api/dashboard/metrics")
def get_dashboard_metrics():
    reservation_service.verificar_e_processar_wo()
    return dashboard_service.calcular_metricas_ocupacao()

@app.get("/api/dashboard/export")
def export_dashboard_data():
    df = dashboard_service.gerar_dataframe_exportacao()
    return df.to_dict(orient="records")
