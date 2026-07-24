import React, { useEffect, useState } from 'react';
import { LayoutGrid, Users, Calendar, CheckCircle2, RefreshCw } from 'lucide-react';
import { fetchLocationsApi, fetchResourcesApi, checkinReservationApi } from '../api/client';
import type { Location, Resource, User } from '../types';
import { StatusBadge } from '../components/StatusBadge';

interface OfficeMapProps {
  user: User;
  onSelectResourceForBooking: (resourceId: number) => void;
}

export const OfficeMap: React.FC<OfficeMapProps> = ({ user, onSelectResourceForBooking }) => {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocId, setSelectedLocId] = useState<number | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const locs = await fetchLocationsApi();
      setLocations(locs);
      const initialLocId = selectedLocId || (locs.length > 0 ? locs[0].id : null);
      if (initialLocId) {
        setSelectedLocId(initialLocId);
        const resList = await fetchResourcesApi(initialLocId);
        setResources(resList);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedLocId]);

  const handleCheckin = async (reservaId: number) => {
    try {
      const res = await checkinReservationApi(reservaId, user.id);
      setMsg(res.message);
      loadData();
    } catch (err: any) {
      setMsg(err.message || 'Erro ao fazer check-in.');
    }
  };

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-wider mb-1">
            <LayoutGrid className="w-4 h-4" />
            Casos de Uso UC002 & US002
          </div>
          <h2 className="text-2xl font-black text-white">Mapa do Escritório em Tempo Real</h2>
          <p className="text-sm text-slate-400">
            Acompanhe a disponibilidade física de mesas, cabines e salas no horário atual.
          </p>
        </div>

        {/* Location Dropdown */}
        <div className="flex items-center gap-3">
          <select
            value={selectedLocId || ''}
            onChange={(e) => setSelectedLocId(Number(e.target.value))}
            className="glass-input px-4 py-2.5 rounded-xl text-sm font-semibold bg-slate-950/80 text-white min-w-[240px]"
          >
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id} className="bg-slate-900 text-white">
                {loc.nome} (Andar {loc.andar})
              </option>
            ))}
          </select>

          <button
            onClick={loadData}
            className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 transition-all"
            title="Atualizar Mapa"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {msg && (
        <div className="p-4 rounded-2xl bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold">
          {msg}
        </div>
      )}

      {/* Grid of Resource Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((r) => {
          const isLivre = r.status === 'LIVRE';
          const isEmUso = r.status === 'EM_USO';
          const isReservado = r.status === 'RESERVADO';
          const minhaReserva = r.reserva_atual && r.reserva_atual.usuario_id === user.id;

          const glowClass = isLivre
            ? 'border-emerald-500/30 hover:border-emerald-500/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.25)]'
            : isEmUso
            ? 'border-rose-500/30 hover:border-rose-500/60 hover:shadow-[0_0_25px_rgba(244,63,94,0.25)]'
            : 'border-blue-500/30 hover:border-blue-500/60 hover:shadow-[0_0_25px_rgba(59,130,246,0.25)]';

          return (
            <div
              key={r.id}
              className={`glass-card p-6 rounded-3xl flex flex-col justify-between transition-all duration-300 border ${glowClass}`}
            >
              <div>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-extrabold text-white">{r.codigo_identificacao}</h3>
                    <span className="text-xs font-semibold text-slate-400">{r.tipo}</span>
                  </div>
                  <StatusBadge status={r.status} />
                </div>

                <div className="bg-slate-950/40 p-3 rounded-xl border border-white/5 flex items-center gap-2 text-xs text-slate-300 mb-6">
                  <Users className="w-4 h-4 text-blue-400" />
                  <span>Capacidade: <strong>{r.capacidade} pessoa(s)</strong></span>
                </div>
              </div>

              <div>
                {isLivre && (
                  <button
                    onClick={() => onSelectResourceForBooking(r.id)}
                    className="w-full glass-button py-2.5 rounded-xl text-xs font-bold text-white flex items-center justify-center gap-2"
                  >
                    <Calendar className="w-4 h-4" />
                    Reservar Espaço
                  </button>
                )}

                {isReservado && minhaReserva && (
                  <button
                    onClick={() => handleCheckin(r.reserva_atual!.id)}
                    className="w-full py-2.5 rounded-xl text-xs font-bold text-emerald-400 bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 flex items-center justify-center gap-2 transition-all shadow-lg shadow-emerald-500/10"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    Confirmar Check-in
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
