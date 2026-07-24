import type { User, Location, Resource, Reservation, DashboardMetrics } from '../types';

const API_BASE = 'http://localhost:8000/api';

export async function loginApi(email: string, senha: string): Promise<{ user: User }> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, senha }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha ao autenticar.');
  return data;
}

export async function registerApi(nome: string, email: string, senha: string, perfil_id: number): Promise<{ user: User }> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome, email, senha, perfil_id }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha no cadastro.');
  return data;
}

export async function fetchLocationsApi(): Promise<Location[]> {
  const res = await fetch(`${API_BASE}/locations`);
  if (!res.ok) throw new Error('Falha ao carregar localizações.');
  return res.json();
}

export async function fetchResourcesApi(locationId?: number): Promise<Resource[]> {
  const url = locationId ? `${API_BASE}/resources?location_id=${locationId}` : `${API_BASE}/resources`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Falha ao carregar recursos.');
  return res.json();
}

export async function createResourceApi(codigo: string, tipo: string, capacidade: number, localizacao_id: number) {
  const res = await fetch(`${API_BASE}/resources`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ codigo, tipo, capacidade, localizacao_id }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha ao cadastrar recurso.');
  return data;
}

export async function deleteResourceApi(id: number) {
  const res = await fetch(`${API_BASE}/resources/${id}`, { method: 'DELETE' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha ao remover recurso.');
  return data;
}

export async function fetchUserReservationsApi(userId: number): Promise<Reservation[]> {
  const res = await fetch(`${API_BASE}/reservations/user/${userId}`);
  if (!res.ok) throw new Error('Falha ao carregar agendamentos.');
  return res.json();
}

export async function createReservationApi(usuario_id: number, recurso_id: number, inicio: string, fim: string) {
  const res = await fetch(`${API_BASE}/reservations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario_id, recurso_id, data_hora_inicio: inicio, data_hora_fim: fim }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha ao realizar reserva.');
  return data;
}

export async function checkinReservationApi(reservationId: number, userId: number) {
  const res = await fetch(`${API_BASE}/reservations/${reservationId}/checkin?usuario_id=${userId}`, {
    method: 'POST',
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Falha ao efetuar check-in.');
  return data;
}

export async function fetchMetricsApi(): Promise<DashboardMetrics> {
  const res = await fetch(`${API_BASE}/dashboard/metrics`);
  if (!res.ok) throw new Error('Falha ao carregar métricas.');
  return res.json();
}

export async function fetchExportDataApi() {
  const res = await fetch(`${API_BASE}/dashboard/export`);
  if (!res.ok) throw new Error('Falha ao exportar dados.');
  return res.json();
}
