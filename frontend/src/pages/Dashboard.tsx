import React, { useEffect, useState } from 'react';
import { BarChart3, Download, Building2, Calendar, Users, AlertTriangle } from 'lucide-react';
import { fetchMetricsApi, fetchExportDataApi } from '../api/client';
import type { DashboardMetrics } from '../types';

export const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [exportData, setExportData] = useState<any[]>([]);

  useEffect(() => {
    fetchMetricsApi().then(setMetrics).catch(console.error);
    fetchExportDataApi().then(setExportData).catch(console.error);
  }, []);

  const handleExportCSV = () => {
    if (exportData.length === 0) return;
    const headers = Object.keys(exportData[0]).join(',');
    const rows = exportData.map((row) => Object.values(row).map((v) => `"${v}"`).join(','));
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'relatorio_ocupacao_flexdesk.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!metrics) {
    return <div className="text-slate-400 text-sm">Carregando métricas...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider mb-1">
            <BarChart3 className="w-4 h-4" />
            Casos de Uso UC006 & US006
          </div>
          <h2 className="text-2xl font-black text-white">Dashboards & Relatórios de Ocupação</h2>
          <p className="text-sm text-slate-400">
            Análise agregada de uso da infraestrutura física para tomada de decisão.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="glass-button px-5 py-3 rounded-xl text-xs font-bold text-white flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          Exportar Relatório CSV
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Recursos</span>
            <Building2 className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-3xl font-black text-white">{metrics.total_recursos}</div>
        </div>

        <div className="glass-card p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Reservas</span>
            <Calendar className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-3xl font-black text-white">{metrics.total_reservas}</div>
        </div>

        <div className="glass-card p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Em Uso Agora</span>
            <Users className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-emerald-400">{metrics.total_em_uso}</div>
        </div>

        <div className="glass-card p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Taxa de W.O. (No-Show)</span>
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-amber-400">{metrics.taxa_wo}%</div>
        </div>
      </div>

      {/* Location Breakdown Table */}
      <div className="glass-panel p-6 rounded-3xl space-y-4">
        <h3 className="text-lg font-bold text-white">Taxa Média de Ocupação por Setor / Andar</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase font-bold">
                <th className="py-3 px-4">Localização</th>
                <th className="py-3 px-4">Total Recursos</th>
                <th className="py-3 px-4">Total Reservas</th>
                <th className="py-3 px-4">Taxa de Ocupação Est. (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-200">
              {metrics.detalhes_localizacao.map((item, idx) => (
                <tr key={idx} className="hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4 font-bold text-white">{item.Localização}</td>
                  <td className="py-3 px-4">{item['Total Recursos']}</td>
                  <td className="py-3 px-4">{item['Total Reservas']}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      <div className="w-24 bg-slate-800 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full"
                          style={{ width: `${item['Taxa de Ocupação Est. (%)']}%` }}
                        />
                      </div>
                      <span className="font-bold">{item['Taxa de Ocupação Est. (%)']}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
