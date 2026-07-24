import React from 'react';
import { LayoutGrid, Calendar, PlusCircle, BarChart3, LogOut, User as UserIcon, Building2 } from 'lucide-react';
import type { User } from '../types';

interface SidebarProps {
  user: User;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ user, activeTab, setActiveTab, onLogout }) => {
  const isGestor = user.perfil_id === 2;

  const navItems = [
    { id: 'map', label: 'Mapa em Tempo Real', icon: LayoutGrid },
    { id: 'reservations', label: 'Reservas & Check-in', icon: Calendar },
    ...(isGestor
      ? [
          { id: 'admin', label: 'Gerenciar Recursos', icon: PlusCircle },
          { id: 'dashboard', label: 'Dashboards & Métricas', icon: BarChart3 },
        ]
      : []),
  ];

  return (
    <aside className="w-72 fixed left-0 top-0 bottom-0 bg-slate-950/70 backdrop-blur-2xl border-r border-white/10 p-6 flex flex-col justify-between z-40 shadow-2xl">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30 border border-white/20">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              FlexDesk
            </h1>
          </div>
        </div>

        {/* User Profile Card */}
        <div className="glass-panel p-4 rounded-2xl mb-8 border border-white/10 bg-white/[0.03] backdrop-blur-xl">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
            SESSÃO ATIVA
          </div>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center text-slate-300">
              <UserIcon className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-slate-100 leading-tight">{user.nome}</div>
              <div className="text-xs text-blue-400 font-medium">{user.perfil_nome}</div>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-2">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-2">
            Navegação
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-600/80 to-indigo-600/80 text-white shadow-lg shadow-blue-500/20 border border-white/20'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-white/5'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Logout Button */}
      <button
        onClick={onLogout}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-semibold text-rose-400 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 transition-all duration-200"
      >
        <LogOut className="w-4 h-4" />
        Sair da Conta
      </button>
    </aside>
  );
};
