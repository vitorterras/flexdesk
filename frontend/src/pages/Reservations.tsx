import React, { useEffect, useState } from 'react';
import { Calendar, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import { fetchResourcesApi, createReservationApi, fetchUserReservationsApi, checkinReservationApi } from '../api/client';
import type { Resource, Reservation, User } from '../types';
import { StatusBadge } from '../components/StatusBadge';

interface ReservationsProps {
  user: User;
  initialSelectedResourceId?: number | null;
}

export const Reservations: React.FC<ReservationsProps> = ({ user, initialSelectedResourceId }) => {
  const [activeSubTab, setActiveSubTab] = useState<'new' | 'my'>('new');
  const [resources, setResources] = useState<Resource[]>([]);
  const [selectedResId, setSelectedResId] = useState<number>(initialSelectedResourceId || 0);
  const [dataReserva, setDataReserva] = useState<string>(new Date().toISOString().split('T')[0]);
  const [horaInicio, setHoraInicio] = useState<string>('09:00');
  const [horaFim, setHoraFim] = useState<string>('11:00');

  const [userReservations, setUserReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const loadResources = async () => {
    try {
      const res = await fetchResourcesApi();
      setResources(res);
      if (!selectedResId && res.length > 0) {
        setSelectedResId(initialSelectedResourceId || res[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadMyReservations = async () => {
    try {
      const list = await fetchUserReservationsApi(user.id);
      setUserReservations(list);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadResources();
    loadMyReservations();
  }, []);

  const handleBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMsg(null);
    try {
      const startIso = `${dataReserva}T${horaInicio}:00`;
      const endIso = `${dataReserva}T${horaFim}:00`;
      const res = await createReservationApi(user.id, selectedResId, startIso, endIso);
      setMsg({ text: res.message, isError: false });
      loadMyReservations();
      setActiveSubTab('my');
    } catch (err: any) {
      setMsg({ text: err.message || 'Erro ao criar reserva.', isError: true });
    } finally {
      setLoading(false);
    }
  };

  const handleCheckin = async (reservaId: number) => {
    try {
      const res = await checkinReservationApi(reservaId, user.id);
      setMsg({ text: res.message, isError: false });
      loadMyReservations();
    } catch (err: any) {
      setMsg({ text: err.message || 'Erro no check-in.', isError: true });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-6 rounded-3xl">
        <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-wider mb-1">
          <Calendar className="w-4 h-4" />
          Casos de Uso UC003 & UC004
        </div>
        <h2 className="text-2xl font-black text-white">Agendamento & Check-in de Espaços</h2>
        <p className="text-sm text-slate-400">
          Reserve mesas, cabines ou salas e faça o check-in no horário agendado.
        </p>

        {/* Sub-tabs */}
        <div className="flex bg-white/5 p-1 rounded-xl mt-6 max-w-md border border-white/10">
          <button
            onClick={() => setActiveSubTab('new')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'new' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Nova Reserva
          </button>
          <button
            onClick={() => setActiveSubTab('my')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'my' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Meus Agendamentos
          </button>
        </div>
      </div>

      {msg && (
        <div
          className={`p-4 rounded-2xl border text-xs font-semibold flex items-center gap-2 ${
            msg.isError
              ? 'bg-rose-500/10 border-rose-500/30 text-rose-300'
              : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
          }`}
        >
          {msg.isError ? <AlertCircle className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
          {msg.text}
        </div>
      )}

      {activeSubTab === 'new' ? (
        <div className="glass-panel p-8 rounded-3xl max-w-2xl">
          <form onSubmit={handleBookingSubmit} className="space-y-6">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Selecione o Recurso
              </label>
              <select
                value={selectedResId}
                onChange={(e) => setSelectedResId(Number(e.target.value))}
                className="w-full glass-input px-4 py-3 rounded-xl text-sm bg-slate-950 text-white"
              >
                {resources.map((r) => (
                  <option key={r.id} value={r.id} className="bg-slate-900 text-white">
                    {r.codigo_identificacao} ({r.tipo}) - Cap.: {r.capacidade} pessoa(s)
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Data do Agendamento
                </label>
                <input
                  type="date"
                  value={dataReserva}
                  onChange={(e) => setDataReserva(e.target.value)}
                  className="w-full glass-input px-4 py-3 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Horário Início
                </label>
                <input
                  type="time"
                  value={horaInicio}
                  onChange={(e) => setHoraInicio(e.target.value)}
                  className="w-full glass-input px-4 py-3 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Horário Término
                </label>
                <input
                  type="time"
                  value={horaFim}
                  onChange={(e) => setHoraFim(e.target.value)}
                  className="w-full glass-input px-4 py-3 rounded-xl text-sm"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full glass-button py-3.5 rounded-xl text-sm font-bold text-white flex items-center justify-center gap-2 cursor-pointer"
            >
              <Calendar className="w-4 h-4" />
              {loading ? 'Confirmando...' : 'Confirmar Reserva de Espaço'}
            </button>
          </form>
        </div>
      ) : (
        <div className="space-y-4">
          {userReservations.length === 0 ? (
            <div className="glass-panel p-8 rounded-3xl text-center text-slate-400 text-sm">
              Você ainda não possui agendamentos cadastrados.
            </div>
          ) : (
            userReservations.map((r) => (
              <div key={r.id} className="glass-card p-6 rounded-3xl flex items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-lg font-black text-white">{r.recurso_codigo}</span>
                    <span className="text-xs text-slate-400 font-medium">({r.localizacao_nome})</span>
                  </div>
                  <div className="text-xs text-slate-300 flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-blue-400" />
                    De <strong>{new Date(r.inicio).toLocaleString()}</strong> até{' '}
                    <strong>{new Date(r.fim).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <StatusBadge status={r.status} />
                  {r.status === 'Pendente' && (
                    <button
                      onClick={() => handleCheckin(r.id)}
                      className="px-4 py-2 rounded-xl text-xs font-bold text-emerald-400 bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 flex items-center gap-1.5 transition-all shadow-lg"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      Efetuar Check-in
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};
