export interface User {
  id: number;
  nome: string;
  email: string;
  perfil_id: number;
  perfil_nome: string;
}

export interface Location {
  id: number;
  nome: string;
  tipo: string;
  andar: number;
}

export interface Resource {
  id: number;
  codigo_identificacao: string;
  tipo: string;
  capacidade: number;
  localizacao_id: number;
  localizacao_nome: string;
  status: 'LIVRE' | 'EM_USO' | 'RESERVADO';
  reserva_atual?: {
    id: number;
    usuario_id: number;
    inicio: string;
    fim: string;
    status_reserva: string;
  } | null;
}

export interface Reservation {
  id: number;
  recurso_id: number;
  recurso_codigo: string;
  recurso_tipo: string;
  localizacao_nome: string;
  inicio: string;
  fim: string;
  status: string;
  checkin?: string | null;
}

export interface DashboardMetrics {
  total_recursos: number;
  total_reservas: number;
  total_em_uso: number;
  total_wo: number;
  taxa_wo: number;
  detalhes_localizacao: Array<{
    Localização: string;
    "Total Recursos": number;
    "Total Reservas": number;
    "Taxa de Ocupação Est. (%)": number;
  }>;
}
