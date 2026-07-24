from typing import Dict, List, Any, Optional
import pandas as pd
from repositories.database import DatabaseRepository
from models.reserva import StatusReserva

class DashboardService:
    def __init__(self, db: Optional[DatabaseRepository] = None):
        self.db = db or DatabaseRepository()

    def calcular_metricas_ocupacao(self) -> Dict[str, Any]:
        """
        UC006: Visualizar Dashboards de Ocupação.
        Calcula taxas de ocupação por setor/andar e estatísticas operacionais.
        """
        recursos = self.db.get_recursos(apenas_ativos=True)
        reservas = self.db.get_reservas()
        localizacoes = self.db.get_localizacoes()

        total_recursos = len(recursos)
        total_reservas = len(reservas)
        total_wo = len([r for r in reservas if r.status_reserva == StatusReserva.WO])
        total_em_uso = len([r for r in reservas if r.status_reserva == StatusReserva.EM_USO])

        taxa_wo = (total_wo / total_reservas * 100) if total_reservas > 0 else 0.0

        # Ocupação por Localização
        loc_map = {l.id: l.nome for l in localizacoes}
        rec_loc_map = {r.id: r.localizacao_id for r in recursos}

        ocupacao_por_loc: Dict[str, int] = {l.nome: 0 for l in localizacoes}
        total_recursos_por_loc: Dict[str, int] = {l.nome: 0 for l in localizacoes}

        for r in recursos:
            loc_nome = loc_map.get(r.localizacao_id, "Desconhecido")
            total_recursos_por_loc[loc_nome] = total_recursos_por_loc.get(loc_nome, 0) + 1

        for res in reservas:
            if res.status_reserva in [StatusReserva.EM_USO, StatusReserva.PENDENTE, StatusReserva.FINALIZADA]:
                rec = self.db.get_recurso_by_id(res.recurso_id)
                if rec:
                    loc_nome = loc_map.get(rec.localizacao_id, "Desconhecido")
                    ocupacao_por_loc[loc_nome] = ocupacao_por_loc.get(loc_nome, 0) + 1

        dados_localizacao = []
        for loc_nome, qtd_reservas in ocupacao_por_loc.items():
            qtd_rec = total_recursos_por_loc.get(loc_nome, 1)
            taxa = min(100.0, round((qtd_reservas / (qtd_rec * 5)) * 100, 1))  # Estimativa baseada em capacidade média
            dados_localizacao.append({
                "Localização": loc_nome,
                "Total Recursos": qtd_rec,
                "Total Reservas": qtd_reservas,
                "Taxa de Ocupação Est. (%)": taxa
            })

        return {
            "total_recursos": total_recursos,
            "total_reservas": total_reservas,
            "total_em_uso": total_em_uso,
            "total_wo": total_wo,
            "taxa_wo": round(taxa_wo, 1),
            "detalhes_localizacao": dados_localizacao
        }

    def gerar_dataframe_exportacao(self) -> pd.DataFrame:
        """Gera DataFrame para exportação de relatório (CSV)."""
        reservas = self.db.get_reservas()
        dados = []
        for r in reservas:
            usuario = self.db.get_usuario_by_id(r.usuario_id)
            recurso = self.db.get_recurso_by_id(r.recurso_id)
            localizacao = self.db.get_localizacao_by_id(recurso.localizacao_id) if recurso else None

            dados.append({
                "ID Reserva": r.id,
                "Usuário": usuario.nome if usuario else "N/A",
                "E-mail": usuario.email if usuario else "N/A",
                "Recurso": recurso.codigo_identificacao if recurso else "N/A",
                "Tipo": recurso.tipo if recurso else "N/A",
                "Localização": localizacao.nome if localizacao else "N/A",
                "Início": r.data_hora_inicio.strftime("%Y-%m-%d %H:%M"),
                "Fim": r.data_hora_fim.strftime("%Y-%m-%d %H:%M"),
                "Status": r.status_reserva,
                "Check-in": r.data_checkin.strftime("%Y-%m-%d %H:%M") if r.data_checkin else "N/A"
            })
        return pd.DataFrame(dados)
