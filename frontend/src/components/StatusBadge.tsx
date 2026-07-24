import React from 'react';
import { CheckCircle2, Clock, AlertCircle, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  switch (status) {
    case 'LIVRE':
    case 'Confirmada':
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shadow-[0_0_12px_rgba(16,185,129,0.2)]">
          <CheckCircle2 className="w-3.5 h-3.5" />
          LIVRE
        </span>
      );
    case 'EM_USO':
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-500/10 text-rose-400 border border-rose-500/30 shadow-[0_0_12px_rgba(244,63,94,0.2)]">
          <AlertCircle className="w-3.5 h-3.5" />
          EM USO
        </span>
      );
    case 'RESERVADO':
    case 'Pendente':
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30 shadow-[0_0_12px_rgba(59,130,246,0.2)]">
          <Clock className="w-3.5 h-3.5" />
          RESERVADO
        </span>
      );
    case 'WO':
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 shadow-[0_0_12px_rgba(245,158,11,0.2)]">
          <XCircle className="w-3.5 h-3.5" />
          W.O. (NO-SHOW)
        </span>
      );
    default:
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-slate-500/10 text-slate-300 border border-slate-500/30">
          {status}
        </span>
      );
  }
};
