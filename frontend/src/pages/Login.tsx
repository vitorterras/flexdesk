import React, { useState } from 'react';
import { Building2, Lock, Mail, User as UserIcon, ArrowRight, ShieldCheck } from 'lucide-react';
import { loginApi, registerApi } from '../api/client';
import type { User } from '../types';

interface LoginProps {
  onLoginSuccess: (user: User) => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('ana@ufu.br');
  const [senha, setSenha] = useState('senha1234');
  const [nome, setNome] = useState('');
  const [perfilId, setPerfilId] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (isRegister) {
        const data = await registerApi(nome, email, senha, perfilId);
        onLoginSuccess(data.user);
      } else {
        const data = await loginApi(email, senha);
        onLoginSuccess(data.user);
      }
    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro.');
    } finally {
      setLoading(false);
    }
  };

  const autofillUser = (e: string, p: string) => {
    setEmail(e);
    setSenha(p);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />

      {/* Floating Liquid Glass Modal */}
      <div className="w-full max-w-md glass-panel p-8 rounded-3xl relative z-10 border border-white/15 bg-slate-950/60 backdrop-blur-3xl shadow-2xl">
        {/* Brand Icon */}
        <div className="flex justify-center mb-6">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-xl shadow-blue-500/30 border border-white/20">
            <Building2 className="w-7 h-7 text-white" />
          </div>
        </div>

        {/* Title */}
        <div className="text-center mb-6">
          <h2 className="text-2xl font-black tracking-tight text-white mb-1">
            FlexDesk
          </h2>
          <p className="text-xs text-slate-400 font-medium">
            Gestão de Coworking & Espaços Híbridos (ES2 UFU)
          </p>
        </div>

        {/* Tabs: Sign In / Join */}
        <div className="flex bg-white/5 p-1 rounded-xl mb-6 border border-white/10">
          <button
            type="button"
            onClick={() => setIsRegister(false)}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${
              !isRegister ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Entrar
          </button>
          <button
            type="button"
            onClick={() => setIsRegister(true)}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${
              isRegister ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            Novo Cadastro
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Nome Completo
              </label>
              <div className="relative">
                <UserIcon className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
                <input
                  type="text"
                  required
                  placeholder="Seu nome"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  className="w-full glass-input pl-10 pr-4 py-2.5 rounded-xl text-sm"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
              E-mail Corporativo (@ufu.br ou @empresa.com.br)
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
              <input
                type="email"
                required
                placeholder="seu.email@ufu.br"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full glass-input pl-10 pr-4 py-2.5 rounded-xl text-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
              Senha (Mínimo 8 caracteres)
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                className="w-full glass-input pl-10 pr-4 py-2.5 rounded-xl text-sm"
              />
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Perfil de Acesso
              </label>
              <select
                value={perfilId}
                onChange={(e) => setPerfilId(Number(e.target.value))}
                className="w-full glass-input px-4 py-2.5 rounded-xl text-sm bg-slate-900"
              >
                <option value={1}>Colaborador</option>
                <option value={2}>Gestor de Facilities</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full glass-button py-3 rounded-xl text-sm font-bold text-white flex items-center justify-center gap-2 mt-6 cursor-pointer"
          >
            {loading ? 'Processando...' : isRegister ? 'Cadastrar Usuário' : 'Acessar Sistema'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Quick Demo Login Fillers */}
        {!isRegister && (
          <div className="mt-6 pt-6 border-t border-white/10">
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2 text-center">
              Dica para Teste Rápido:
            </div>
            <div className="flex flex-col gap-2">
              <button
                type="button"
                onClick={() => autofillUser('ana@ufu.br', 'senha1234')}
                className="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-300 flex justify-between items-center"
              >
                <span>👤 Ana (Colaboradora)</span>
                <span className="text-[10px] text-blue-400 font-bold">ana@ufu.br</span>
              </button>
              <button
                type="button"
                onClick={() => autofillUser('carlos.gestor@ufu.br', 'admin1234')}
                className="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-300 flex justify-between items-center"
              >
                <span>🛡️ Carlos (Gestor Facilities)</span>
                <span className="text-[10px] text-indigo-400 font-bold">carlos.gestor@ufu.br</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
