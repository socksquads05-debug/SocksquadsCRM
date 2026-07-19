"""
Luxury theme helpers for the Socksquads CRM app.
"""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT_DIR / "assets" / "brand"
BACKGROUND_IMAGE = BRAND_DIR / "luxury-background.png"
BRAND_PANEL_IMAGE = BRAND_DIR / "brand-panel.png"


def _to_data_uri(image_path: Path) -> str:
    """Encode a local image as a base64 data URI for CSS use."""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    suffix = image_path.suffix.lower().lstrip(".") or "png"
    return f"data:image/{suffix};base64,{encoded}"


def inject_theme() -> None:
    """Apply the global Socksquads visual theme."""
    background_uri = _to_data_uri(BACKGROUND_IMAGE)
    panel_uri = _to_data_uri(BRAND_PANEL_IMAGE)

    st.markdown(
        f"""
        <style>
            :root {{
                --sq-navy: #07162f;
                --sq-navy-soft: #10264d;
                --sq-gold: #c9a66b;
                --sq-cream: #f7f2ea;
                --sq-panel: rgba(247, 242, 234, 0.92);
                --sq-panel-strong: rgba(255, 252, 247, 0.96);
                --sq-copy: #18263c;
                --sq-muted: #627287;
                --sq-border: rgba(201, 166, 107, 0.28);
            }}

            h1, h2, h3, h4 {{
                font-family: Georgia, "Times New Roman", serif !important;
                color: var(--sq-navy);
                letter-spacing: 0.02em;
            }}

            p, label, span, div {{
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}

            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(180deg, #02112b, #051730);
                color: #f7f5f2;
                background-attachment: fixed;
            }}

            [data-testid="stSidebar"] > div:first-child {{
                background: linear-gradient(180deg, #04142f, #071b40);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }}

            .block-container {{
                background: var(--sq-cream);
                border: 1px solid rgba(16,38,77,0.06);
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(3, 11, 24, 0.08);
                margin-top: 1rem;
                margin-bottom: 1.25rem;
                padding: 1.6rem 1.6rem 2rem;
                backdrop-filter: none;
            }}

            div[data-testid="stMetric"] {{
                background: linear-gradient(180deg, rgba(255, 252, 247, 0.98), rgba(246, 238, 226, 0.95));
                border: 1px solid var(--sq-border);
                border-radius: 24px;
                box-shadow: 0 16px 36px rgba(7, 22, 47, 0.12);
                padding: 1rem 1rem 0.9rem 1rem;
            }}

            div.stButton > button,
            div[data-testid="stDownloadButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {{
                background: linear-gradient(135deg, var(--sq-navy-soft), var(--sq-navy));
                color: white;
                border: 1px solid rgba(201, 166, 107, 0.42);
                border-radius: 999px;
                box-shadow: 0 10px 24px rgba(7, 22, 47, 0.22);
                font-weight: 600;
            }}

            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            .stDateInput > div > div,
            .stTextArea textarea,
            .stTextInput>div>div>input,
            .stTextArea>div>div>textarea,
            .stNumberInput>div>div>input,
            .stDateInput>div>div>input {{
                background: #ffffff !important;
                border: 1px solid rgba(16, 38, 77, 0.18) !important;
                border-radius: 12px !important;
                color: var(--sq-copy) !important;
            }}

            /* Make labels and placeholders more readable */
            label, .stTextInput label, .stDateInput label {{
                color: var(--sq-copy) !important;
                font-weight: 600;
            }}

            input::placeholder, textarea::placeholder {{
                color: rgba(24,38,60,0.45) !important;
            }}

            input, textarea {{
                color: #0f2038 !important;
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.5rem;
            }}

            .stTabs [data-baseweb="tab"] {{
                background: rgba(201, 166, 107, 0.1);
                border: 1px solid rgba(201, 166, 107, 0.18);
                border-radius: 999px;
                color: var(--sq-copy);
                padding: 0.55rem 1rem;
            }}

            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, var(--sq-navy-soft), var(--sq-navy));
                color: white !important;
            }}

            [data-testid="stExpander"] {{
                background: rgba(255, 255, 255, 0.68);
                border: 1px solid rgba(201, 166, 107, 0.18);
                border-radius: 22px;
                overflow: hidden;
            }}

            [data-testid="stDataFrame"] {{
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(201, 166, 107, 0.18);
                border-radius: 22px;
                padding: 0.3rem;
            }}

            .sq-brand-panel {{
                background: rgba(2, 17, 45, 0.96);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 28px;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.32);
                min-height: 260px;
                overflow: hidden;
            }}

            .sq-login-logo {{
                width: 108px;
                height: 108px;
                border-radius: 999px;
                background: white;
                color: #041329;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                font-weight: 800;
                margin: 0 auto 1rem auto;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }}

            .sq-brand-meta {{
                padding: 1.4rem 1.35rem 1.35rem;
                background: transparent;
                color: white;
                min-height: 260px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            }}

            .sq-brand-panel--compact {{
                min-height: 178px;
            }}

            .sq-brand-meta {{
                padding: 1.2rem 1.35rem;
                background: linear-gradient(180deg, rgba(4, 12, 24, 0.18), rgba(4, 12, 24, 0.62));
                color: white;
                min-height: 260px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            }}

            .sq-brand-panel--compact .sq-brand-meta {{
                min-height: 178px;
                padding: 1rem 1.1rem;
            }}

            .sq-brand-kicker {{
                text-transform: uppercase;
                letter-spacing: 0.26em;
                font-size: 0.72rem;
                opacity: 0.8;
                margin-bottom: 0.45rem;
            }}

            .sq-brand-title {{
                font-family: Georgia, "Times New Roman", serif !important;
                font-size: 1.95rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin: 0;
                color: white;
            }}

            .sq-brand-copy {{
                margin-top: 0.55rem;
                max-width: 28rem;
                color: rgba(255, 250, 242, 0.86);
                line-height: 1.55;
            }}

            .sq-sidebar-card {{
                margin-bottom: 1rem;
            }}

            .sq-page-banner {{
                display: flex;
                align-items: end;
                justify-content: space-between;
                gap: 1rem;
                padding: 1.35rem 1.5rem;
                border-radius: 28px;
                border: 1px solid rgba(201, 166, 107, 0.28);
                background:
                    linear-gradient(120deg, rgba(7, 22, 47, 0.95), rgba(15, 36, 74, 0.82)),
                    url("{background_uri}");
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 42px rgba(7, 22, 47, 0.22);
                margin-bottom: 1.2rem;
            }}

            .sq-page-banner__eyebrow {{
                color: rgba(255, 245, 232, 0.8);
                text-transform: uppercase;
                letter-spacing: 0.24em;
                font-size: 0.72rem;
                margin-bottom: 0.4rem;
            }}

            .sq-page-banner__title {{
                color: white;
                font-family: Georgia, "Times New Roman", serif !important;
                font-size: 2rem;
                line-height: 1.05;
                margin: 0;
            }}

            .sq-page-banner__text {{
                color: rgba(255, 245, 232, 0.82);
                margin-top: 0.45rem;
                max-width: 40rem;
                line-height: 1.55;
            }}

            .sq-page-banner__mark {{
                flex: 0 0 84px;
                height: 84px;
                border-radius: 24px;
                border: 1px solid rgba(201, 166, 107, 0.24);
                background:
                    linear-gradient(180deg, rgba(7, 22, 47, 0.16), rgba(7, 22, 47, 0.02)),
                    url("{panel_uri}");
                background-size: cover;
                background-position: center;
            }}

            @media (max-width: 900px) {{
                .block-container {{
                    padding: 1.3rem 1rem 2rem;
                    border-radius: 24px;
                }}

                .sq-page-banner__mark {{
                    display: none;
                }}

                .sq-brand-title {{
                    font-size: 1.5rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_brand() -> None:
    """Display the branded login hero panel."""
    st.markdown(
        """
        <div class="sq-login-logo">S</div>
        <div class="sq-brand-panel">
            <div class="sq-brand-meta">
                <div class="sq-brand-kicker">Luxury sales command center</div>
                <h1 class="sq-brand-title">Socksquads CRM</h1>
                <div class="sq-brand-copy">
                    Track field sales, retailer relationships, collections, and performance in a premium branded workspace.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand(user_data: dict | None) -> None:
    """Display the branded sidebar lockup."""
    name = escape((user_data or {}).get("name", "Guest"))
    role = escape(((user_data or {}).get("role", "user")).upper())

    st.markdown(
        f"""
        <div class="sq-sidebar-card sq-brand-panel sq-brand-panel--compact">
            <div class="sq-brand-meta">
                <div class="sq-brand-kicker">Socksquads</div>
                <div class="sq-brand-title" style="font-size: 1.22rem;">Business cockpit</div>
                <div class="sq-brand-copy" style="font-size: 0.92rem; margin-top: 0.35rem;">
                    {name} &middot; {role}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_banner(title: str, subtitle: str, eyebrow: str = "Socksquads CRM") -> None:
    """Display a reusable page banner with consistent branding."""
    st.markdown(
        f"""
        <div class="sq-page-banner">
            <div>
                <div class="sq-page-banner__eyebrow">{escape(eyebrow)}</div>
                <h1 class="sq-page-banner__title">{escape(title)}</h1>
                <div class="sq-page-banner__text">{escape(subtitle)}</div>
            </div>
            <div class="sq-page-banner__mark"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
