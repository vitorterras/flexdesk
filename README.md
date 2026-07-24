# 🏢 FlexDesk - Sistema de Gestão de Coworking e Espaços Híbridos
> **Trabalho Prático da Disciplina de Engenharia de Software 2 (ES2)**  
> **Universidade Federal de Uberlândia (UFU)** — Prof. Dr. Fabiano Azevedo Dorça  
> **Autor:** Vitor Terra (`vitorterras`)

---

## 🎨 Visão Geral & Tecnologias
O **FlexDesk** é uma solução full-stack moderna para reserva em tempo real de estações de trabalho (*hot-desking*), cabines privadas e salas de reunião, prevenção de no-show (W.O.) e análise de ocupação.

- **Frontend:** React 18 + Vite + TypeScript + TailwindCSS (Liquid Glass Dark Mode) + Lucide Icons
- **Backend:** FastAPI (Python) + PyTest (13 testes automatizados de integração)
- **Banco de Dados:** Supabase Relational PostgreSQL (Tabelas: `perfil`, `usuario`, `localizacao`, `recurso`, `reserva`)

---

## 🔑 Credenciais de Teste para Avaliação

A tela de Login possui **botões interativos de preenchimento automático** com as seguintes credenciais pré-cadastradas:

| Perfil | E-mail Corporativo | Senha | Funcionalidades Liberadas na Interface |
| :--- | :--- | :--- | :--- |
| **🛡️ Gestor de Facilities** | `carlos.gestor@ufu.br` | `admin1234` | **Mapa em Tempo Real**, **Agendamentos**, **Gerenciar Recursos (CRUD)** e **Dashboards & Métricas (CSV)** |
| **👤 Colaboradora 1** | `ana@ufu.br` | `senha1234` | **Mapa em Tempo Real**, **Reservar Espaço** e **Efetuar Check-in** |
| **👤 Colaborador 2** | `bruno@empresa.com.br` | `senha1234` | **Mapa em Tempo Real**, **Reservar Espaço** e **Efetuar Check-in** |

---

## 🚀 Como Executar o Projeto Localmente

### 1. Iniciar o Backend API (FastAPI)
```bash
pip install -r requirements.txt
python3 -m uvicorn server:app --reload --port 8000
```

### 2. Iniciar o Frontend Web (React + Vite)
Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```
Acesse a aplicação no navegador em: **`http://localhost:5173`**

---

## 🧪 Suíte de Testes Automatizados (PyTest)
Para executar a suíte com os 13 testes automatizados (Auth, Recursos, Reservas, W.O. e Dashboards):
```bash
python3 -m pytest -v tests/
```
