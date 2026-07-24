import streamlit as st

def inject_liquid_glass_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

            html, body, .stApp {
                background-color: #090a0f !important;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(30, 58, 138, 0.28) 0px, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
                    radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.85) 0px, transparent 50%) !important;
                color: #f1f5f9 !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            /* Header e Títulos */
            h1, h2, h3, h4, h5, h6, label, p, span, li {
                color: #f8fafc !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            .stCaption, small {
                color: #94a3b8 !important;
            }

            /* Sidebar Liquid Glass */
            section[data-testid="stSidebar"] {
                background: rgba(15, 23, 42, 0.65) !important;
                backdrop-filter: blur(24px) !important;
                -webkit-backdrop-filter: blur(24px) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
            }

            section[data-testid="stSidebar"] * {
                color: #e2e8f0 !important;
            }

            /* Form Inputs, Selectboxes, Radio */
            div[data-baseweb="select"] > div, input, textarea, .stTextInput > div > div, .stNumberInput > div > div {
                background-color: rgba(15, 23, 42, 0.6) !important;
                backdrop-filter: blur(16px) !important;
                -webkit-backdrop-filter: blur(16px) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 14px !important;
                color: #ffffff !important;
                box-shadow: inset 0 1px 2px rgba(255,255,255,0.05) !important;
            }

            div[data-baseweb="select"] > div:hover, input:hover {
                border-color: rgba(99, 102, 241, 0.6) !important;
                box-shadow: 0 0 12px rgba(99, 102, 241, 0.25) !important;
            }

            /* Dropdowns e Menus Flutuantes (Liquid Glass) */
            div[data-baseweb="menu"], ul[role="listbox"] {
                background: rgba(15, 23, 42, 0.95) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                border-radius: 16px !important;
                box-shadow: 0 20px 40px rgba(0,0,0,0.7) !important;
            }

            li[role="option"] {
                color: #e2e8f0 !important;
                border-radius: 8px !important;
                margin: 4px !important;
            }

            li[role="option"]:hover, li[aria-selected="true"] {
                background: rgba(99, 102, 241, 0.3) !important;
                color: #ffffff !important;
            }

            /* Botões */
            .stButton > button, div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.85), rgba(37, 99, 235, 0.95)) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                border-radius: 14px !important;
                padding: 10px 24px !important;
                font-weight: 600 !important;
                letter-spacing: 0.3px !important;
                box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
                transform: translateY(-2px) scale(1.01) !important;
                box-shadow: 0 14px 28px rgba(37, 99, 235, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
                border-color: rgba(255, 255, 255, 0.5) !important;
            }

            /* Abas / Tabs */
            button[data-baseweb="tab"] {
                background-color: transparent !important;
                color: #94a3b8 !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 8px 16px !important;
                transition: all 0.2s ease !important;
            }

            button[aria-selected="true"] {
                background: rgba(255, 255, 255, 0.08) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            }

            /* Métricas e Dataframes */
            div[data-testid="stMetricValue"] {
                color: #60a5fa !important;
                font-weight: 800 !important;
                text-shadow: 0 0 12px rgba(96, 165, 250, 0.4) !important;
            }

            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.03) !important;
                backdrop-filter: blur(16px) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 18px !important;
                padding: 16px !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.5), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 25px 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.15);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0; font-size: 32px; font-weight: 800; background: linear-gradient(90deg, #ffffff, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏢 FlexDesk</h1>
                    <p style="margin: 6px 0 0 0; font-size: 15px; color: #94a3b8;">Sistema de Gestão de Coworking e Espaços Híbridos • ES2 UFU</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str) -> str:
    badges = {
        "LIVRE": {
            "bg": "rgba(16, 185, 129, 0.15)",
            "border": "rgba(16, 185, 129, 0.4)",
            "color": "#34d399",
            "shadow": "rgba(16, 185, 129, 0.25)",
            "label": "● LIVRE"
        },
        "EM_USO": {
            "bg": "rgba(244, 63, 94, 0.15)",
            "border": "rgba(244, 63, 94, 0.4)",
            "color": "#fb7185",
            "shadow": "rgba(244, 63, 94, 0.25)",
            "label": "● OCUPADA / EM USO"
        },
        "RESERVADO": {
            "bg": "rgba(59, 130, 246, 0.15)",
            "border": "rgba(59, 130, 246, 0.4)",
            "color": "#60a5fa",
            "shadow": "rgba(59, 130, 246, 0.25)",
            "label": "● RESERVADA"
        },
        "Pendente": {
            "bg": "rgba(59, 130, 246, 0.15)",
            "border": "rgba(59, 130, 246, 0.4)",
            "color": "#60a5fa",
            "shadow": "rgba(59, 130, 246, 0.25)",
            "label": "PENDENTE"
        },
        "Confirmada": {
            "bg": "rgba(16, 185, 129, 0.15)",
            "border": "rgba(16, 185, 129, 0.4)",
            "color": "#34d399",
            "shadow": "rgba(16, 185, 129, 0.25)",
            "label": "CONFIRMADA"
        },
        "WO": {
            "bg": "rgba(245, 158, 11, 0.15)",
            "border": "rgba(245, 158, 11, 0.4)",
            "color": "#fbbf24",
            "shadow": "rgba(245, 158, 11, 0.25)",
            "label": "W.O. (NO-SHOW)"
        }
    }

    style = badges.get(status, {
        "bg": "rgba(148, 163, 184, 0.15)",
        "border": "rgba(148, 163, 184, 0.4)",
        "color": "#cbd5e1",
        "shadow": "transparent",
        "label": status
    })

    return f'''
        <span style="
            background: {style['bg']};
            border: 1px solid {style['border']};
            color: {style['color']};
            box-shadow: 0 0 12px {style['shadow']};
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
            display: inline-block;
        ">{style['label']}</span>
    '''
