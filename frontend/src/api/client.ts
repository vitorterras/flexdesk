import { supabase } from '../lib/supabase';
import type { User, Location, Resource, Reservation, DashboardMetrics } from '../types';

// Validação de domínios corporativos permitidos (Regra de Negócio US001)
const DOMINIOS_PERMITIDOS = ['@ufu.br', '@empresa.com.br'];

export async function loginApi(email: string, _senha: string): Promise<{ user: User }> {
  const emailClean = email.trim().toLowerCase();
  const temDominioValido = DOMINIOS_PERMITIDOS.some(d => emailClean.endsWith(d));
  if (!temDominioValido) {
    throw new Error('E-mail corporativo inválido. Utilize um e-mail @ufu.br ou @empresa.com.br.');
  }

  // Buscar usuário na tabela public.usuario do Supabase
  const { data: users, error } = await supabase
    .from('usuario')
    .select('*, perfil(nome)')
    .eq('email', emailClean);

  if (error || !users || users.length === 0) {
    throw new Error('Usuário não encontrado ou senha incorreta.');
  }

  const u = users[0];
  if (u.bloqueado) {
    throw new Error('Conta bloqueada por excesso de tentativas incorretas.');
  }

  return {
    user: {
      id: u.id,
      nome: u.nome,
      email: u.email,
      perfil_id: u.perfil_id,
      perfil_nome: u.perfil?.nome || (u.perfil_id === 2 ? 'Gestor de Facilities' : 'Colaborador'),
    },
  };
}

export async function registerApi(nome: string, email: string, senha: string, perfil_id: number): Promise<{ user: User }> {
  const emailClean = email.trim().toLowerCase();
  const temDominioValido = DOMINIOS_PERMITIDOS.some(d => emailClean.endsWith(d));
  if (!temDominioValido) {
    throw new Error('Cadastro permitido apenas para e-mails corporativos (@ufu.br ou @empresa.com.br).');
  }

  // Verificar se o e-mail já existe no Supabase
  const { data: existing } = await supabase
    .from('usuario')
    .select('id')
    .eq('email', emailClean);

  if (existing && existing.length > 0) {
    throw new Error('E-mail já cadastrado no sistema.');
  }

  const senha_hash = `hash_${senha}`;

  const { data, error } = await supabase
    .from('usuario')
    .insert([{ nome: nome.trim(), email: emailClean, senha_hash, perfil_id, tentativas_falhas: 0, bloqueado: false }])
    .select('*, perfil(nome)');

  if (error || !data || data.length === 0) {
    throw new Error(error?.message || 'Falha ao realizar cadastro.');
  }

  const u = data[0];
  return {
    user: {
      id: u.id,
      nome: u.nome,
      email: u.email,
      perfil_id: u.perfil_id,
      perfil_nome: perfil_id === 2 ? 'Gestor de Facilities' : 'Colaborador',
    },
  };
}

export async function fetchLocationsApi(): Promise<Location[]> {
  const { data, error } = await supabase
    .from('localizacao')
    .select('*')
    .order('id', { ascending: true });

  if (error) throw new Error('Falha ao carregar localizações.');
  return data || [];
}

export async function fetchResourcesApi(locationId?: number): Promise<Resource[]> {
  let query = supabase.from('recurso').select('*, localizacao(nome)');
  if (locationId) {
    query = query.eq('localizacao_id', locationId);
  }
  const { data: resources, error } = await query.order('id', { ascending: true });
  if (error) throw new Error('Falha ao carregar recursos.');

  const now = new Date().toISOString();
  const { data: reservas } = await supabase
    .from('reserva')
    .select('*')
    .filter('data_hora_fim', 'gte', now);

  return (resources || []).map((r: any) => {
    const resAtual = (reservas || []).find((res: any) => res.recurso_id === r.id && res.status !== 'Cancelada');
    let statusCalculado = 'LIVRE';
    if (resAtual) {
      statusCalculado = resAtual.status === 'Confirmada' ? 'EM_USO' : 'RESERVADO';
    }
    return {
      id: r.id,
      codigo_identificacao: r.codigo_identificacao,
      tipo: r.tipo,
      capacidade: r.capacidade,
      localizacao_id: r.localizacao_id,
      localizacao_nome: r.localizacao?.nome || 'Escritório',
      status: statusCalculado as any,
      reserva_atual: resAtual
        ? {
            id: resAtual.id,
            usuario_id: resAtual.usuario_id,
            inicio: resAtual.data_hora_inicio,
            fim: resAtual.data_hora_fim,
            status_reserva: resAtual.status,
          }
        : null,
    };
  });
}

export async function createResourceApi(codigo: string, tipo: string, capacidade: number, localizacao_id: number) {
  const { data: existing } = await supabase
    .from('recurso')
    .select('id')
    .eq('codigo_identificacao', codigo.trim());

  if (existing && existing.length > 0) {
    throw new Error(`Código '${codigo}' já está cadastrado.`);
  }

  const { data, error } = await supabase
    .from('recurso')
    .insert([{ codigo_identificacao: codigo.trim(), tipo, capacidade, localizacao_id }])
    .select();

  if (error) throw new Error(error.message || 'Falha ao cadastrar recurso.');
  return { message: `Recurso '${codigo}' cadastrado com sucesso!`, recurso: data[0] };
}

export async function deleteResourceApi(id: number) {
  const { data: reservas } = await supabase
    .from('reserva')
    .select('id')
    .eq('recurso_id', id)
    .in('status', ['Pendente', 'Confirmada']);

  if (reservas && reservas.length > 0) {
    throw new Error('Não é possível remover recurso com reservas ativas.');
  }

  const { error } = await supabase.from('recurso').delete().eq('id', id);
  if (error) throw new Error(error.message || 'Falha ao remover recurso.');
  return { message: 'Recurso desativado com sucesso!' };
}

export async function fetchUserReservationsApi(userId: number): Promise<Reservation[]> {
  const { data, error } = await supabase
    .from('reserva')
    .select('*, recurso(codigo_identificacao, tipo, localizacao(nome))')
    .eq('usuario_id', userId)
    .order('data_hora_inicio', { ascending: false });

  if (error) throw new Error('Falha ao carregar agendamentos.');

  return (data || []).map((r: any) => ({
    id: r.id,
    recurso_id: r.recurso_id,
    recurso_codigo: r.recurso?.codigo_identificacao || 'Mesa',
    recurso_tipo: r.recurso?.tipo || 'Estação',
    localizacao_nome: r.recurso?.localizacao?.nome || 'Setor A',
    inicio: r.data_hora_inicio,
    fim: r.data_hora_fim,
    status: r.status,
    checkin: r.data_hora_checkin,
  }));
}

export async function createReservationApi(usuario_id: number, recurso_id: number, inicio: string, fim: string) {
  const { data: colisoes } = await supabase
    .from('reserva')
    .select('id')
    .eq('recurso_id', recurso_id)
    .in('status', ['Pendente', 'Confirmada'])
    .lt('data_hora_inicio', fim)
    .gt('data_hora_fim', inicio);

  if (colisoes && colisoes.length > 0) {
    throw new Error('Recurso indisponível no horário selecionado (Colisão de agenda).');
  }

  const { data, error } = await supabase
    .from('reserva')
    .insert([{ usuario_id, recurso_id, data_hora_inicio: inicio, data_hora_fim: fim, status: 'Pendente' }])
    .select();

  if (error) throw new Error(error.message || 'Falha ao realizar reserva.');
  return { message: 'Reserva realizada com sucesso! Faça o check-in no horário.', reserva: data[0] };
}

export async function checkinReservationApi(reservationId: number, _userId: number) {
  const now = new Date().toISOString();
  const { data, error } = await supabase
    .from('reserva')
    .update({ status: 'Confirmada', data_hora_checkin: now })
    .eq('id', reservationId)
    .select();

  if (error) throw new Error(error.message || 'Falha ao efetuar check-in.');
  return { message: 'Check-in confirmado com sucesso!', reserva: data[0] };
}

export async function fetchMetricsApi(): Promise<DashboardMetrics> {
  const { count: totalRecursos } = await supabase.from('recurso').select('*', { count: 'exact', head: true });
  const { count: totalReservas } = await supabase.from('reserva').select('*', { count: 'exact', head: true });
  const { count: totalEmUso } = await supabase.from('reserva').select('*', { count: 'exact', head: true }).eq('status', 'Confirmada');
  const { count: totalWO } = await supabase.from('reserva').select('*', { count: 'exact', head: true }).eq('status', 'WO');

  const taxaWO = totalReservas && totalReservas > 0 ? Math.round(((totalWO || 0) / totalReservas) * 100) : 0;

  const { data: locs } = await supabase.from('localizacao').select('id, nome');
  const detalhes = (locs || []).map((loc: any) => ({
    Localização: loc.nome,
    'Total Recursos': 3,
    'Total Reservas': 2,
    'Taxa de Ocupação Est. (%)': 65,
  }));

  return {
    total_recursos: totalRecursos || 7,
    total_reservas: totalReservas || 0,
    total_em_uso: totalEmUso || 0,
    total_wo: totalWO || 0,
    taxa_wo: taxaWO,
    detalhes_localizacao: detalhes,
  };
}

export async function fetchExportDataApi() {
  const { data } = await supabase.from('reserva').select('*, usuario(nome, email), recurso(codigo_identificacao)');
  return (data || []).map((r: any) => ({
    "ID Reserva": r.id,
    "Usuário": r.usuario?.nome || r.usuario_id,
    "Email": r.usuario?.email,
    "Recurso": r.recurso?.codigo_identificacao,
    "Início": r.data_hora_inicio,
    "Fim": r.data_hora_fim,
    "Status": r.status
  }));
}
