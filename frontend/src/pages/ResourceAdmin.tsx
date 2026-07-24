import React, { useEffect, useState } from 'react';
import { PlusCircle, Trash2, ShieldCheck, AlertCircle, Building2 } from 'lucide-react';
import { fetchLocationsApi, fetchResourcesApi, createResourceApi, deleteResourceApi } from '../api/client';
import type { Location, Resource } from '../types';

export const ResourceAdmin: React.FC = () => {
  const [activeSubTab, setActiveSubTab] = useState<'list' | 'create'>('list');
  const [locations, setLocations] = useState<Location[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  
  const [codigo, setCodigo] = useState('Mesa B-02');
  const [tipo, setTipo] = useState('Mesa');
  const [capacidade, setCapacidade] = useState(1);
  const [localizacaoId, setLocalizacaoId] = useState<number>(1);
  
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const loadData = async () => {
    try {
      const locs = await fetchLocationsApi();
      setLocations(locs);
      if (locs.length > 0) setLocalizacaoId(locs[0].id);

      const resList = await fetchResourcesApi();
      setResources(resList);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMsg(null);
    try {
      const res = await createResourceApi(codigo, tipo, capacidade, localizacaoId);
      setMsg({ text: res.message, isError: false });
      loadData();
      setActiveSubTab('list');
    } catch (err: any) {
      setMsg({ text: err.message || 'Erro ao cadastrar.', isError: true });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number, codigoRec: string) => {
    if (!window.confirm(`Tem certeza que deseja remover o recurso '${codigoRec}'?`)) return;
    setMsg(null);
    try {
      const res = await deleteResourceApi(id);
      setMsg({ text: res.message, isError: false });
      loadData();
    } catch (err: any) {
      setMsg({ text: err.message || 'Erro ao remover.', isError: true });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-6 rounded-3xl">
        <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider mb-1">
          <PlusCircle className="w-4 h-4" />
          Casos de Uso UC005 & US005 (Gestor de Facilities)
        </div>
        <h2 className="text-2xl font-black text-white">Gerenciamento de Recursos</h2>
        <p className="text-sm text-slate-400">
          Cadastre, altere e remova estações de trabalho, cabines e salas do escritório.
        </p>

        {/* Sub-tabs */}
        <div className="flex bg-white/5 p-1 rounded-xl mt-6 max-w-md border border-white/10">
          <button
            onClick={() => setActiveSubTab('list')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'list' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Recursos Cadastrados
          </button>
          <button
            onClick={() => setActiveSubTab('create')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'create' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Novo Recurso
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
          {msg.isError ? <AlertCircle className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />}
          {msg.text}
        </div>
      )}

      {activeSubTab === 'list' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resources.map((r) => (
            <div key={r.id} className="glass-card p-6 rounded-3xl flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-black text-white">{r.codigo_identificacao}</h3>
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                    {r.tipo}
                  </span>
                </div>
                <div className="text-xs text-slate-400 mb-4 flex items-center gap-1.5">
                  <Building2 className="w-3.5 h-3.5 text-slate-400" />
                  {r.localizacao_nome}
                </div>
                <div className="text-xs text-slate-300 bg-slate-950/40 p-2.5 rounded-xl border border-white/5">
                  Capacidade: <strong>{r.capacidade} pessoa(s)</strong>
                </div>
              </div>

              <button
                onClick={() => handleDelete(r.id, r.codigo_identificacao)}
                className="w-full mt-6 py-2.5 rounded-xl text-xs font-bold text-rose-400 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 flex items-center justify-center gap-1.5 transition-all"
              >
                <Trash2 className="w-3.5 h-3.5" />
                Desativar Recurso
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-panel p-8 rounded-3xl max-w-xl">
          <form onSubmit={handleCreateSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Código de Identificação Único (Ex: Mesa A-05, Sala 4B)
              </label>
              <input
                type="text"
                required
                value={codigo}
                onChange={(e) => setCodigo(e.target.value)}
                className="w-full glass-input px-4 py-3 rounded-xl text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Tipo de Recurso
              </label>
              <select
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
                className="w-full glass-input px-4 py-3 rounded-xl text-sm bg-slate-950 text-white"
              >
                <option value="Mesa">Mesa</option>
                <option value="Sala Reunião">Sala Reunião</option>
                <option value="Cabine">Cabine Call</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Capacidade Máxima de Pessoas
              </label>
              <input
                type="number"
                min={1}
                required
                value={capacidade}
                onChange={(e) => setCapacidade(Number(e.target.value))}
                className="w-full glass-input px-4 py-3 rounded-xl text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Localização / Setor
              </label>
              <select
                value={localizacaoId}
                onChange={(e) => setLocalizacaoId(Number(e.target.value))}
                className="w-full glass-input px-4 py-3 rounded-xl text-sm bg-slate-950 text-white"
              >
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id} className="bg-slate-900 text-white">
                    {loc.nome} (Andar {loc.andar})
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full glass-button py-3.5 rounded-xl text-sm font-bold text-white flex items-center justify-center gap-2 mt-6 cursor-pointer"
            >
              <PlusCircle className="w-4 h-4" />
              {loading ? 'Cadastrando...' : 'Cadastrar Recurso'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
