"""Global theme and styling utilities (light theme variant)."""

import streamlit as st

# Gradients
GRADIENT_PRIMARY = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
GRADIENT_ACCENT = "linear-gradient(45deg, #FF6B6B, #4ECDC4)"
GRADIENT_BRAND = "linear-gradient(90deg, #6D58FF 0%, #886BFF 50%, #A289FF 100%)"

# Light theme colors (white background requested)
COLOR_BG = "#ffffff"
COLOR_SURFACE = "#ffffff"
COLOR_SURFACE_HOVER = "#f6f7fb"
COLOR_BORDER = "#e6e8f0"
COLOR_TEXT = "#1b1e28"
COLOR_TEXT_MUTED = "#6b7280"
COLOR_SUCCESS = "#4ECDC4"
COLOR_DANGER = "#FF6B6B"
RADIUS_SM = "8px"
RADIUS_MD = "12px"
RADIUS_LG = "18px"
SHADOW_MD = "0 10px 30px rgba(0, 0, 0, 0.12)"
FONT_STACK = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Ubuntu, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
)


def inject_global_css():
    """Inject global CSS variables and component styles."""
    st.markdown(
        f"""
        <style>
          :root {{
            --grad-primary: {GRADIENT_PRIMARY};
            --grad-accent: {GRADIENT_ACCENT};
            --grad-brand: {GRADIENT_BRAND};
            --bg: {COLOR_BG};
            --surface: {COLOR_SURFACE};
            --surface-hover: {COLOR_SURFACE_HOVER};
            --border: {COLOR_BORDER};
            --text: {COLOR_TEXT};
            --muted: {COLOR_TEXT_MUTED};
            --success: {COLOR_SUCCESS};
            --danger: {COLOR_DANGER};
            --radius-sm: {RADIUS_SM};
            --radius-md: {RADIUS_MD};
            --radius-lg: {RADIUS_LG};
            --shadow-md: {SHADOW_MD};
            --font: {FONT_STACK};
          }}

          html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], [data-testid="stAppViewBlockContainer"] {{
            background: var(--bg) !important;
            color: var(--text);
            font-family: var(--font);
          }}

          /* Sidebar */
          section[data-testid="stSidebar"] > div {{
            background: #ffffff;
            border-right: 1px solid var(--border);
          }}
          section[data-testid="stSidebar"] .stButton > button {{ width: 100%; }}

          /* Card */
          .app-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.1rem 1.25rem;
            box-shadow: var(--shadow-md);
          }}

          .grad-text {{
            background: var(--grad-primary);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          }}

          .stButton > button {{
            background: var(--grad-brand) !important;
            color: #fff !important;
            border: 0 !important;
            border-radius: var(--radius-md) !important;
            padding: 0.6rem 0.9rem !important;
            font-weight: 600;
            box-shadow: 0 6px 16px rgba(109,88,255,0.35);
          }}
          .stButton > button:hover {{ filter: brightness(1.05); transform: translateY(-1px); }}

          .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text) !important;
          }}
          .stTextInput input::placeholder {{ color: var(--muted); }}
          .stTextArea textarea::placeholder {{ color: var(--muted); }}

          .tab-content {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.25rem;
          }}

          [data-testid="stChatMessage"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 0.85rem 1rem;
            margin-bottom: 0.6rem;
          }}
          [data-testid="stChatMessage"]:has(div[data-testid="stMarkdownContainer"]) {{
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
          }}

          /* Conversations */
          .conv-item {{
            display: flex; align-items: center; gap: 10px;
            padding: 0.55rem 0.6rem; border-radius: var(--radius-md);
            border: 1px solid transparent; cursor: pointer;
          }}
          .conv-item:hover {{ background: var(--surface-hover); border-color: var(--border); }}
          .conv-item.active {{ outline: 2px solid var(--success); background: rgba(78,205,196,0.12); }}
          .conv-title {{ flex: 1; font-weight: 600; }}
          .conv-time {{ color: var(--muted); font-size: 12px; }}

          /* Auth layout */
          .auth-wrapper {{
            display: flex; gap: 3rem; align-items: stretch; justify-content: center;
            padding: 2.5rem 1.2rem 1.2rem; flex-wrap: wrap;
          }}
          .auth-hero {{
            flex: 1 1 360px; min-height: 480px;
            background: linear-gradient(145deg, #ffffff 0%, #fbfbfd 65%, #f5f6fa 100%);
            position: relative;
            padding: 3.2rem 2.4rem 2.6rem;
            border-radius: 32px;
            overflow: hidden;
            /* Make Streamlit tabs and form elements appear visually inside the right card */
            /* When using explicit .auth-card wrapper */
            .auth-card + div[data-testid="stTabs"] {{ position:relative; top:-2.2rem; margin-bottom:-2.2rem; background:transparent; padding:0 2.2rem; }}
            .auth-card + div[data-testid="stTabs"] > div {{ background:transparent; }}
            .auth-card + div[data-testid="stTabs"] [role="tablist"] {{ border-bottom:1px solid var(--border); background:transparent; padding-left:0.25rem; padding-right:0.25rem; }}
            .auth-card + div[data-testid="stTabs"] [role="tabpanel"] {{ padding-top:0.85rem; background:transparent; }}
            /* When using sentinel approach (kept for compatibility) */
            .auth-card-sentinel + div [data-testid="stTabs"] {{ margin-top:0.4rem; }}
            .auth-card-sentinel + div [data-testid="stTabs"] [role="tablist"] {{ border-bottom:1px solid var(--border); }}
            .auth-card-sentinel + div [data-testid="stTabs"] [role="tabpanel"] {{ padding-top:0.85rem; }}
                        radial-gradient(circle at 85% 80%, rgba(255,107,107,0.10), transparent 55%);
            mix-blend-mode: normal;
          }}
          .auth-hero-border {{
            position:absolute; inset:0; border-radius:32px; padding:2px;
            background: linear-gradient(120deg, rgba(109,88,255,0.65), rgba(78,205,196,0.55), rgba(255,107,107,0.55));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor; mask-composite: exclude;
          }}
          .auth-hero:before {{ display:none; }}
          .auth-hero h2 {{ font-size:2.05rem; line-height:1.2; font-weight:700; margin:0 0 1.2rem; }}
          .auth-hero p {{ font-size:1.05rem; max-width:420px; margin:0 0 0.75rem; }}
          .auth-card {{
            flex:1 1 420px; min-height:560px;
            background:linear-gradient(145deg,#ffffff 0%,#fbfbfd 65%,#f5f6fa 100%);
            border-radius:32px; padding:3.0rem 2.6rem 2.4rem; position:relative;
            box-shadow:0 20px 55px -15px rgba(23,25,35,0.18), 0 8px 18px -6px rgba(23,25,35,0.08);
            overflow:hidden;
             margin-bottom:-2.4rem; /* visually group tabs with card */
          }}
          /* Column sentinel makes entire right column behave as card */
          .auth-card-sentinel {{ display:block; }}
          /* Wrap column content (brand + tabs + footer) with card visuals */
          .auth-card-sentinel + div {{
            position:relative;
            background:linear-gradient(145deg,#ffffff 0%,#fbfbfd 65%,#f5f6fa 100%);
            border-radius:32px;
            padding:3.0rem 2.6rem 2.4rem;
            min-height:560px;
            overflow:hidden;
          }}
          .auth-card-sentinel + div:before {{
            content:""; position:absolute; inset:0; border-radius:32px; padding:2px;
            background: linear-gradient(120deg, rgba(109,88,255,0.65), rgba(78,205,196,0.55), rgba(255,107,107,0.55));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor; mask-composite: exclude;
            pointer-events:none;
          }}
          .auth-card-sentinel + div:after {{
            content:""; position:absolute; inset:0; pointer-events:none;
            background: radial-gradient(circle at 85% 80%, rgba(255,107,107,0.10), transparent 55%);
          }}
          .auth-card-border {{
            position:absolute; inset:0; border-radius:32px; padding:2px;
            background: linear-gradient(120deg, rgba(109,88,255,0.65), rgba(78,205,196,0.55), rgba(255,107,107,0.55));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor; mask-composite: exclude;
            pointer-events:none;
          }}
          .auth-card:after {{
            content:""; position:absolute; inset:0; pointer-events:none;
            background: radial-gradient(circle at 20% 25%, rgba(109,88,255,0.10), transparent 60%),
                        radial-gradient(circle at 80% 75%, rgba(255,107,107,0.08), transparent 55%);
          }}
          /* Brand heading inside card (solid to avoid gradient issues) */
          .auth-brand {{ font-size:2.4rem; font-weight:800; color:#6D58FF; margin:0 0 0.35rem; }}
          .auth-subtitle {{ color:var(--muted); margin:0 0 1.6rem; }}
          .auth-card .stTabs [role="tablist"] {{ border-bottom:1px solid var(--border); }}
          .auth-card .stTabs [role="tab"]:hover {{ background:var(--surface-hover); }}
          .auth-card .stButton > button {{ width:100%; margin-top:0.6rem; height:46px; font-size:15px; }}
          .auth-footer {{ text-align:center; margin-top:2.4rem; font-size:0.85rem; color:var(--muted); position:relative; top:-1.6rem; margin-bottom:-1.6rem; }}

       /* Tabs repositioned visually inside the preceding auth-card */
       .auth-card + div[data-testid="stTabs"] {{ position:relative; top:-2.2rem; margin-bottom:-2.2rem; background:transparent; padding:0 2.2rem; }}
       .auth-card + div[data-testid="stTabs"] > div {{ background:transparent; }}
       .auth-card + div[data-testid="stTabs"] [role="tablist"] {{ border-bottom:1px solid var(--border); background:transparent; padding-left:0.25rem; padding-right:0.25rem; }}
       .auth-card + div[data-testid="stTabs"] [role="tablist"] button {{ font-weight:600; }}
       .auth-card + div[data-testid="stTabs"] [role="tabpanel"] {{ padding-top:0.85rem; background:transparent; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def app_header(title: str, subtitle: str | None = None):
    """Render a gradient page header."""
    st.markdown(
        f"""
        <div style="margin:0 0 0.75rem 0;">
          <h1 class="grad-text" style="margin:0; line-height:1.1">{title}</h1>
          {f'<p style="margin:0.35rem 0 0; color: var(--muted);">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
