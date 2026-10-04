"""
ALGOX — Central True Glassmorphism Design System & UI Architecture
Translucent glass panels, backdrop blur, ambient background lighting,
and student-friendly academic DAA typography.
"""
import streamlit as st
import datetime
from typing import List, Dict, Any, Optional

# --- CORE PALETTE & GLASS TOKENS ---
COLOR_BG = "#050816"             # Deep background
COLOR_GLASS_PANEL = "rgba(12, 19, 48, 0.58)"   # Translucent glass surface
COLOR_GLASS_INPUT = "rgba(10, 15, 38, 0.65)"    # Nested glass control
COLOR_GLASS_BORDER = "rgba(139, 92, 246, 0.18)" # Soft glass border
COLOR_GLASS_BORDER_LIGHT = "rgba(255, 255, 255, 0.14)"

COLOR_PURPLE = "#7C3AED"        # Primary accent
COLOR_PURPLE_LIGHT = "#8B5CF6"
COLOR_BLUE = "#2563EB"          # Secondary electric blue
COLOR_BLUE_LIGHT = "#3B82F6"
COLOR_CYAN = "#06B6D4"          # Accent cyan
COLOR_GREEN = "#22C55E"         # Success green
COLOR_AMBER = "#F59E0B"         # Warning amber
COLOR_RED = "#EF4444"           # Error red
COLOR_TEXT = "#F1F5F9"          # Primary text
COLOR_TEXT_MUTED = "#94A3B8"    # Secondary / supporting text

def render_html(html_str: str):
    """
    Safely renders HTML without leading whitespace on any line, preventing
    CommonMark markdown parsers from treating indented HTML as <pre><code> blocks.
    """
    if not html_str:
        return
    cleaned = chr(10).join(line.strip() for line in html_str.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)

def inject_css():
    """Injects comprehensive True Glassmorphism global CSS with cursor hover glow interactions."""
    render_html(f"""
<style>
    /* 1. Global Reset & Atmospheric Background Glows */
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 10% 12%, rgba(124, 58, 237, 0.25), transparent 42%),
            radial-gradient(circle at 90% 14%, rgba(37, 99, 235, 0.22), transparent 40%),
            radial-gradient(circle at 50% 88%, rgba(6, 182, 212, 0.16), transparent 46%),
            linear-gradient(135deg, #050816 0%, #080C24 50%, #050718 100%) !important;
        background-attachment: fixed !important;
        color: {COLOR_TEXT} !important;
        min-height: 100vh;
    }}

    /* 2. Hide default Streamlit chrome */
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; display: none !important; }}
    footer {{ visibility: hidden !important; display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
    }}

    /* 3. Centered Content Container with breathing room */
    .main .block-container {{
        max-width: 1440px !important;
        padding-left: 2.25rem !important;
        padding-right: 2.25rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        margin: 0 auto !important;
        position: relative !important;
        z-index: 2 !important;
    }}

    /* 4. Translucent Glass Sidebar */
    section[data-testid="stSidebar"] {{
        min-width: 265px !important;
        max-width: 265px !important;
        background: rgba(8, 12, 32, 0.65) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(110, 90, 255, 0.38) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35), 6px 0 40px rgba(110, 90, 255, 0.18) !important;
        position: relative !important;
        z-index: 10 !important;
    }}
    section[data-testid="stSidebar"] .block-container {{
        padding: 1.25rem 0.85rem !important;
    }}

    /* 5. Sidebar Navigation Items */
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {{
        width: 100% !important;
        min-height: 42px !important;
        margin-bottom: 4px !important;
        font-size: 0.86rem !important;
        border-radius: 11px !important;
        transition: all 0.2s ease-out !important;
        cursor: pointer !important;
    }}
    section[data-testid="stSidebar"] button[kind="primary"] {{
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.85), rgba(37, 99, 235, 0.78)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        box-shadow: 0 8px 24px rgba(99, 60, 255, 0.55), 0 0 22px rgba(139, 92, 246, 0.60), 0 0 42px rgba(99, 60, 255, 0.28) !important;
        font-weight: 650 !important;
    }}
    section[data-testid="stSidebar"] button[kind="primary"]:hover {{
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.92), rgba(59, 130, 246, 0.85)) !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
        box-shadow: 0 8px 28px rgba(124, 58, 237, 0.50), 0 0 20px rgba(6, 182, 212, 0.30) !important;
    }}
    section[data-testid="stSidebar"] button[kind="secondary"] {{
        background: rgba(14, 20, 48, 0.55) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(110, 90, 255, 0.18) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        font-weight: 500 !important;
    }}
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background: rgba(22, 32, 75, 0.80) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(139, 92, 246, 0.45) !important;
        box-shadow: 0 4px 18px rgba(124, 58, 237, 0.50), 0 0 12px rgba(37, 99, 235, 0.18) !important;
    }}

    /* 6. GLOBAL TRUE GLASSMORPHISM CONTAINER SYSTEM */
    div[data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlockBorderWrapper"] > div,
    .algox-glass-card,
    .glass-card,
    .algox-panel,
    .glass-panel {{
        background: linear-gradient(135deg, rgba(20, 24, 58, 0.92), rgba(8, 15, 38, 0.88)) !important;
        background-image:
            radial-gradient(circle at top right, rgba(139, 92, 246, 0.16), transparent 55%),
            linear-gradient(135deg, rgba(20, 24, 58, 0.92), rgba(8, 15, 38, 0.88)) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border: 1px solid rgba(139, 92, 246, 0.48) !important;
        border-radius: 18px !important;
        padding: 22px 26px !important;
        box-shadow:
            0 0 16px rgba(124, 58, 237, 0.42),
            0 0 32px rgba(59, 130, 246, 0.28),
            0 0 58px rgba(6, 182, 212, 0.16),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            inset 0 0 20px rgba(124, 58, 237, 0.08) !important;
        transition: transform 0.22s ease-out, border-color 0.22s ease-out, box-shadow 0.22s ease-out !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover,
    [data-testid="stVerticalBlockBorderWrapper"]:hover,
    div[data-testid="stVerticalBlockBorderWrapper"] > div:hover,
    .algox-glass-card:hover,
    .glass-card:hover,
    .algox-panel:hover,
    .glass-panel:hover {{
        border-color: rgba(168, 85, 247, 0.72) !important;
        box-shadow:
            0 12px 38px rgba(0, 0, 0, 0.45),
            0 0 22px rgba(168, 85, 247, 0.65),
            0 0 46px rgba(59, 130, 246, 0.42),
            0 0 80px rgba(6, 182, 212, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.22) !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}

    .algox-hero-card {{
        background: linear-gradient(135deg, rgba(22, 28, 68, 0.92), rgba(10, 16, 44, 0.88)) !important;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(168, 85, 247, 0.22) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.16) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.22) 0%, transparent 45%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.005) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(139, 92, 246, 0.48) !important;
        border-radius: 22px !important;
        padding: 26px 30px !important;
        box-shadow:
            0 16px 48px rgba(0, 0, 0, 0.45),
            0 0 18px rgba(168, 85, 247, 0.55),
            0 0 40px rgba(59, 130, 246, 0.38),
            0 0 70px rgba(6, 182, 212, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.22),
            inset 0 0 30px rgba(124, 58, 237, 0.14) !important;
    }}

    /* REUSABLE GLOWING KPI CARDS WITH MULTI-LAYER NEON BOX-SHADOWS */
    .algox-kpi-card {{
        background: linear-gradient(135deg, rgba(20, 25, 62, 0.92), rgba(8, 14, 38, 0.88)) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border-radius: 18px !important;
        padding: 22px 24px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: 134px !important;
        transition: transform 0.22s ease-out, border-color 0.22s ease-out, box-shadow 0.22s ease-out !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    .algox-kpi-card:hover {{
        transform: translateY(-2px) !important;
    }}

    /* 1. Purple Glow (Algorithms) */
    .algox-kpi-card.purple, .glass-card-purple {{
        background-image:
            radial-gradient(circle at top right, rgba(168, 85, 247, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(168, 85, 247, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(168, 85, 247, 0.48) !important;
        box-shadow:
            0 0 10px rgba(168, 85, 247, 0.38),
            0 0 25px rgba(168, 85, 247, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(168, 85, 247, 0.08) !important;
    }}
    .algox-kpi-card.purple:hover, .glass-card-purple:hover {{
        border-color: rgba(168, 85, 247, 0.70) !important;
        box-shadow:
            0 0 16px rgba(168, 85, 247, 0.55),
            0 0 35px rgba(168, 85, 247, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* 2. Blue Glow (Experiments) */
    .algox-kpi-card.blue, .glass-card-blue {{
        background-image:
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(59, 130, 246, 0.48) !important;
        box-shadow:
            0 0 10px rgba(59, 130, 246, 0.38),
            0 0 25px rgba(59, 130, 246, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(59, 130, 246, 0.08) !important;
    }}
    .algox-kpi-card.blue:hover, .glass-card-blue:hover {{
        border-color: rgba(59, 130, 246, 0.70) !important;
        box-shadow:
            0 0 16px rgba(59, 130, 246, 0.55),
            0 0 35px rgba(59, 130, 246, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* 3. Cyan Glow (Fastest Measured) */
    .algox-kpi-card.cyan, .glass-card-cyan {{
        background-image:
            radial-gradient(circle at top right, rgba(6, 182, 212, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(6, 182, 212, 0.48) !important;
        box-shadow:
            0 0 10px rgba(6, 182, 212, 0.38),
            0 0 25px rgba(6, 182, 212, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(6, 182, 212, 0.08) !important;
    }}
    .algox-kpi-card.cyan:hover, .glass-card-cyan:hover {{
        border-color: rgba(6, 182, 212, 0.70) !important;
        box-shadow:
            0 0 16px rgba(6, 182, 212, 0.55),
            0 0 35px rgba(6, 182, 212, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* 4. Amber Glow (Average Time) */
    .algox-kpi-card.amber, .glass-card-amber {{
        background-image:
            radial-gradient(circle at top right, rgba(245, 158, 11, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.48) !important;
        box-shadow:
            0 0 10px rgba(245, 158, 11, 0.38),
            0 0 25px rgba(245, 158, 11, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(245, 158, 11, 0.08) !important;
    }}
    .algox-kpi-card.amber:hover, .glass-card-amber:hover {{
        border-color: rgba(245, 158, 11, 0.70) !important;
        box-shadow:
            0 0 16px rgba(245, 158, 11, 0.55),
            0 0 35px rgba(245, 158, 11, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* 5. Green Glow (Total Datasets) */
    .algox-kpi-card.green, .glass-card-green {{
        background-image:
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(34, 197, 94, 0.48) !important;
        box-shadow:
            0 0 10px rgba(34, 197, 94, 0.38),
            0 0 25px rgba(34, 197, 94, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(34, 197, 94, 0.08) !important;
    }}
    .algox-kpi-card.green:hover, .glass-card-green:hover {{
        border-color: rgba(34, 197, 94, 0.70) !important;
        box-shadow:
            0 0 16px rgba(34, 197, 94, 0.55),
            0 0 35px rgba(34, 197, 94, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* 6. Pink Glow (Recommendations) */
    .algox-kpi-card.pink, .glass-card-pink {{
        background-image:
            radial-gradient(circle at top right, rgba(236, 72, 153, 0.22), transparent 55%),
            linear-gradient(135deg, rgba(236, 72, 153, 0.12) 0%, rgba(10, 18, 45, 0.80) 45%, rgba(5, 10, 28, 0.92) 100%) !important;
        border: 1px solid rgba(236, 72, 153, 0.48) !important;
        box-shadow:
            0 0 10px rgba(236, 72, 153, 0.38),
            0 0 25px rgba(236, 72, 153, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.18),
            inset 0 0 20px rgba(236, 72, 153, 0.08) !important;
    }}
    .algox-kpi-card.pink:hover, .glass-card-pink:hover {{
        border-color: rgba(236, 72, 153, 0.70) !important;
        box-shadow:
            0 0 16px rgba(236, 72, 153, 0.55),
            0 0 35px rgba(236, 72, 153, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}

    /* ILLUMINATED ICON CONTAINERS */
    .algox-neon-icon {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 9px !important;
        font-size: 1.05rem !important;
        transition: all 0.22s ease-out !important;
    }}
    .algox-neon-icon-purple {{
        background: rgba(168, 85, 247, 0.22) !important;
        border: 1px solid rgba(168, 85, 247, 0.55) !important;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.50) !important;
    }}
    .algox-neon-icon-blue {{
        background: rgba(59, 130, 246, 0.22) !important;
        border: 1px solid rgba(59, 130, 246, 0.55) !important;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.50) !important;
    }}
    .algox-neon-icon-cyan {{
        background: rgba(6, 182, 212, 0.22) !important;
        border: 1px solid rgba(6, 182, 212, 0.55) !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.50) !important;
    }}
    .algox-neon-icon-amber {{
        background: rgba(245, 158, 11, 0.22) !important;
        border: 1px solid rgba(245, 158, 11, 0.55) !important;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.50) !important;
    }}
    .algox-neon-icon-green {{
        background: rgba(34, 197, 94, 0.22) !important;
        border: 1px solid rgba(34, 197, 94, 0.55) !important;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.50) !important;
    }}
    .algox-neon-icon-pink {{
        background: rgba(236, 72, 153, 0.22) !important;
        border: 1px solid rgba(236, 72, 153, 0.55) !important;
        box-shadow: 0 0 12px rgba(236, 72, 153, 0.50) !important;
    }}

    /* GLOWING STAT CARDS (Dataset Lab, History, Complexity) */
    .algox-stat-card {{
        background: linear-gradient(145deg, rgba(16, 22, 54, 0.90), rgba(8, 14, 36, 0.85)) !important;
        background-image:
            radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.14) 0%, transparent 60%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.005) 100%) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border: 1px solid rgba(6, 182, 212, 0.35) !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        text-align: center !important;
        min-height: 104px !important;
        min-width: 130px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow:
            0 8px 26px rgba(0, 0, 0, 0.35),
            0 0 18px rgba(6, 182, 212, 0.42),
            0 0 38px rgba(6, 182, 212, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
        transition: transform 0.2s ease-out, border-color 0.2s ease-out, box-shadow 0.2s ease-out !important;
    }}
    .algox-stat-card:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(6, 182, 212, 0.65) !important;
        box-shadow:
            0 12px 34px rgba(0, 0, 0, 0.42),
            0 0 20px rgba(6, 182, 212, 0.55),
            0 0 52px rgba(6, 182, 212, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.22) !important;
    }}

    /* QUICK ACTION CARDS WITH DISTINCT NEON BORDER GLOWS */
    .algox-action-card {{
        background: linear-gradient(135deg, rgba(16, 22, 54, 0.90), rgba(8, 14, 36, 0.85)) !important;
        border-radius: 16px !important;
        padding: 20px 22px !important;
        transition: all 0.22s ease-out !important;
        backdrop-filter: blur(18px) !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    .algox-action-purple {{
        border: 1px solid rgba(168, 85, 247, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(168, 85, 247, 0.45), 0 0 38px rgba(168, 85, 247, 0.22) !important;
    }}
    .algox-action-purple:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(168, 85, 247, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(168, 85, 247, 0.62) !important;
    }}
    .algox-action-blue {{
        border: 1px solid rgba(59, 130, 246, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(59, 130, 246, 0.45), 0 0 38px rgba(59, 130, 246, 0.22) !important;
    }}
    .algox-action-blue:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(59, 130, 246, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(59, 130, 246, 0.62) !important;
    }}
    .algox-action-cyan {{
        border: 1px solid rgba(6, 182, 212, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(6, 182, 212, 0.45), 0 0 38px rgba(6, 182, 212, 0.22) !important;
    }}
    .algox-action-cyan:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(6, 182, 212, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(6, 182, 212, 0.62) !important;
    }}
    .algox-action-amber {{
        border: 1px solid rgba(245, 158, 11, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(245, 158, 11, 0.45), 0 0 38px rgba(245, 158, 11, 0.22) !important;
    }}
    .algox-action-amber:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(245, 158, 11, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(245, 158, 11, 0.62) !important;
    }}
    .algox-action-green {{
        border: 1px solid rgba(34, 197, 94, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(34, 197, 94, 0.45), 0 0 38px rgba(34, 197, 94, 0.22) !important;
    }}
    .algox-action-green:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(34, 197, 94, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(34, 197, 94, 0.62) !important;
    }}
    .algox-action-pink {{
        border: 1px solid rgba(236, 72, 153, 0.40) !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35), 0 0 18px rgba(236, 72, 153, 0.45), 0 0 38px rgba(236, 72, 153, 0.22) !important;
    }}
    .algox-action-pink:hover {{
        transform: translateY(-2px) !important;
        border-color: rgba(236, 72, 153, 0.68) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 22px rgba(236, 72, 153, 0.62) !important;
    }}

    /* 7. GLASS BUTTONS WITH BALANCED NEON GLOW */
    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stDownloadButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.90), rgba(37, 99, 235, 0.90)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(168, 85, 247, 0.50) !important;
        border-radius: 11px !important;
        font-weight: 650 !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 0 14px rgba(110, 70, 255, 0.55), 0 0 35px rgba(50, 120, 255, 0.35), 0 0 60px rgba(110, 70, 255, 0.18) !important;
        padding: 0.55rem 1.4rem !important;
        transition: transform 0.2s ease-out, box-shadow 0.2s ease-out, background 0.2s ease-out, border-color 0.2s ease-out !important;
        cursor: pointer !important;
    }}
    div[data-testid="stButton"] > button[kind="primary"]:hover,
    div[data-testid="stDownloadButton"] > button[kind="primary"]:hover {{
        transform: translateY(-1.5px) !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.98), rgba(59, 130, 246, 0.98)) !important;
        box-shadow: 0 0 20px rgba(130, 80, 255, 0.72), 0 0 45px rgba(60, 130, 255, 0.45), 0 0 70px rgba(110, 70, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.40) !important;
        color: #FFFFFF !important;
    }}
    div[data-testid="stButton"] > button[kind="primary"]:active,
    div[data-testid="stDownloadButton"] > button[kind="primary"]:active {{
        box-shadow: inset 0 0 14px rgba(255, 255, 255, 0.25), 0 0 12px rgba(110, 70, 255, 0.40) !important;
    }}
    div[data-testid="stButton"] > button[kind="secondary"],
    div[data-testid="stDownloadButton"] > button[kind="secondary"] {{
        background: rgba(14, 20, 48, 0.65) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(110, 90, 255, 0.28) !important;
        border-radius: 11px !important;
        font-weight: 550 !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 0 14px rgba(124, 58, 237, 0.38), 0 0 28px rgba(59, 130, 246, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.10) !important;
        padding: 0.55rem 1.4rem !important;
        transition: transform 0.2s ease-out, box-shadow 0.2s ease-out, background 0.2s ease-out, border-color 0.2s ease-out, color 0.2s ease-out !important;
        cursor: pointer !important;
    }}
    div[data-testid="stButton"] > button[kind="secondary"]:hover,
    div[data-testid="stDownloadButton"] > button[kind="secondary"]:hover {{
        transform: translateY(-1px) !important;
        background: rgba(22, 30, 70, 0.85) !important;
        border-color: rgba(139, 92, 246, 0.55) !important;
        box-shadow: 0 0 18px rgba(124, 58, 237, 0.52), 0 0 35px rgba(37, 99, 235, 0.35), 0 0 55px rgba(124, 58, 237, 0.18) !important;
        color: #FFFFFF !important;
    }}

    /* 8. GLASS FORM INPUTS & SELECTBOXES */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea {{
        background-color: rgba(10, 16, 42, 0.78) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(90, 110, 255, 0.35) !important;
        box-shadow: inset 0 0 12px rgba(50, 80, 255, 0.12), 0 0 14px rgba(70, 80, 255, 0.28), 0 0 28px rgba(90, 90, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #F1F5F9 !important;
        transition: border-color 0.2s ease-out, box-shadow 0.2s ease-out, background-color 0.2s ease-out !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] input:hover,
    div[data-testid="stTextInput"] input:hover,
    div[data-testid="stNumberInput"] input:hover,
    div[data-testid="stTextArea"] textarea:hover {{
        border-color: rgba(139, 92, 246, 0.55) !important;
        box-shadow: inset 0 0 12px rgba(50, 80, 255, 0.12), 0 0 14px rgba(90, 110, 255, 0.42) !important;
        background-color: rgba(12, 18, 48, 0.85) !important;
    }}
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] input:focus,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {{
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 12px rgba(80, 180, 255, 0.55), 0 0 30px rgba(100, 70, 255, 0.40), 0 0 55px rgba(80, 120, 255, 0.22), inset 0 0 14px rgba(80, 120, 255, 0.12) !important;
        background-color: rgba(14, 22, 54, 0.92) !important;
        outline: none !important;
    }}

    /* Popover dropdowns for selectbox options */
    div[data-baseweb="popover"] > div, ul[role="listbox"] {{
        background: rgba(10, 16, 42, 0.96) !important;
        border: 1px solid rgba(139, 92, 246, 0.45) !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), 0 0 22px rgba(124, 58, 237, 0.50) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 12px !important;
    }}
    li[role="option"] {{
        color: #E2E8F0 !important;
        transition: background 0.15s ease-out !important;
    }}
    li[role="option"]:hover, li[aria-selected="true"] {{
        background: rgba(124, 58, 237, 0.25) !important;
        color: #FFFFFF !important;
    }}

    /* 9. PLOTLY CHART RESEARCH PANELS */
    div[data-testid="stPlotlyChart"] {{
        background: linear-gradient(145deg, rgba(14, 20, 50, 0.85), rgba(6, 12, 30, 0.80)) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(110, 90, 255, 0.32) !important;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.35),
            0 0 22px rgba(90, 70, 255, 0.38),
            0 0 45px rgba(6, 182, 212, 0.25),
            0 0 75px rgba(90, 70, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.10) !important;
        margin: 8px 0 !important;
        overflow: hidden !important;
        transition: box-shadow 0.25s ease-out, border-color 0.25s ease-out !important;
    }}
    div[data-testid="stPlotlyChart"]:hover {{
        border-color: rgba(139, 92, 246, 0.52) !important;
        box-shadow:
            0 14px 40px rgba(0, 0, 0, 0.42),
            0 0 35px rgba(139, 92, 246, 0.52),
            0 0 65px rgba(6, 182, 212, 0.38),
            0 0 95px rgba(90, 70, 255, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
    }}

    /* 10. GLASS DATA TERMINALS (TABLES & DATAFRAMES) */
    div[data-testid="stDataFrame"] {{
        border-radius: 14px !important;
        border: 1px solid rgba(110, 90, 255, 0.35) !important;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.40), 0 0 16px rgba(110, 90, 255, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        background: linear-gradient(145deg, rgba(12, 18, 46, 0.88), rgba(6, 10, 28, 0.84)) !important;
        overflow: hidden !important;
    }}
    div[data-testid="stDataFrame"] div[data-testid="glide-cell"] {{
        white-space: nowrap !important;
    }}

    /* 11. STREAMLIT EXPANDERS — GLASS PANELS */
    details[data-testid="stExpander"] {{
        background: linear-gradient(135deg, rgba(16, 22, 54, 0.85), rgba(8, 14, 36, 0.80)) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(110, 90, 255, 0.35) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.30), 0 0 12px rgba(110, 90, 255, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transition: border-color 0.2s ease-out, box-shadow 0.2s ease-out !important;
        overflow: hidden !important;
    }}
    details[data-testid="stExpander"]:hover {{
        border-color: rgba(139, 92, 246, 0.58) !important;
        box-shadow: 0 6px 26px rgba(0, 0, 0, 0.36), 0 0 20px rgba(139, 92, 246, 0.50) !important;
    }}
    details[data-testid="stExpander"] summary {{
        color: #F1F5F9 !important;
        font-weight: 650 !important;
        font-size: 0.90rem !important;
    }}
    details[data-testid="stExpander"] summary:hover {{
        color: #FFFFFF !important;
    }}

    /* 12. SLIDERS — CYBER ACCENT & GLOWING THUMB */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {{
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 4px !important;
    }}
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div > div:first-child {{
        background: linear-gradient(90deg, #7C3AED, #3B82F6, #06B6D4) !important;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.35) !important;
        border-radius: 4px !important;
    }}
    div[data-testid="stSlider"] [role="slider"] {{
        background: linear-gradient(135deg, #A855F7, #06B6D4) !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.60), 0 0 22px rgba(124, 58, 237, 0.45) !important;
        width: 18px !important;
        height: 18px !important;
        transition: transform 0.15s ease-out, box-shadow 0.15s ease-out !important;
    }}
    div[data-testid="stSlider"] [role="slider"]:hover {{
        box-shadow: 0 0 16px rgba(6, 182, 212, 0.85), 0 0 28px rgba(124, 58, 237, 0.65) !important;
        transform: scale(1.1) !important;
    }}
    div[data-testid="stSlider"] div[data-testid="stThumbValue"] {{
        color: #06B6D4 !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        text-shadow: 0 0 8px rgba(6, 182, 212, 0.5) !important;
    }}

    /* 13. STREAMLIT METRICS */
    div[data-testid="stMetric"] {{
        background: linear-gradient(145deg, rgba(16, 22, 56, 0.88), rgba(8, 14, 38, 0.80)) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(6, 182, 212, 0.35) !important;
        border-radius: 14px !important;
        padding: 16px 18px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.32), 0 0 18px rgba(6, 182, 212, 0.42), 0 0 40px rgba(6, 182, 212, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.10) !important;
        transition: border-color 0.2s ease-out, box-shadow 0.2s ease-out !important;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: rgba(6, 182, 212, 0.60) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.40), 0 0 22px rgba(6, 182, 212, 0.55) !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-shadow: 0 0 12px rgba(255, 255, 255, 0.25) !important;
    }}
    div[data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.08em !important;
    }}

    /* 14. STREAMLIT TABS — NEON UNDERLINE GLOW */
    div[data-testid="stTabs"] button[data-baseweb="tab"] {{
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-bottom: 2px solid transparent !important;
        transition: color 0.2s ease-out, border-color 0.2s ease-out, text-shadow 0.2s ease-out !important;
        padding: 8px 16px 10px 16px !important;
        margin-right: 8px !important;
        background: transparent !important;
    }}
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {{
        color: #C4B5FD !important;
        border-bottom: 2px solid rgba(139, 92, 246, 0.45) !important;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: #FFFFFF !important;
        border-bottom: 2px solid #8B5CF6 !important;
        text-shadow: 0 0 12px rgba(139, 92, 246, 0.65) !important;
    }}
    div[data-testid="stTabs"] [role="tablist"] {{
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 16px !important;
    }}

    /* 15. MULTISELECT TAG PILLS */
    span[data-baseweb="tag"] {{
        background: rgba(124, 58, 237, 0.25) !important;
        border: 1px solid rgba(139, 92, 246, 0.50) !important;
        color: #C4B5FD !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        box-shadow: 0 0 10px rgba(124, 58, 237, 0.42) !important;
    }}
    span[data-baseweb="tag"]:hover {{
        background: rgba(124, 58, 237, 0.35) !important;
        border-color: rgba(139, 92, 246, 0.70) !important;
    }}
    span[data-baseweb="tag"] span[role="presentation"] {{
        color: #C4B5FD !important;
    }}

    /* 16. RADIO & CHECKBOX ACCENTS */
    div[data-testid="stRadio"] label:hover,
    div[data-testid="stCheckbox"] label:hover {{
        color: #FFFFFF !important;
    }}
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stCheckbox"] label[data-checked="true"] {{
        color: #E2E8F0 !important;
        text-shadow: 0 0 8px rgba(139, 92, 246, 0.30) !important;
    }}

    /* 17. INFO / WARNING / SUCCESS / DANGER CARD BASE */
    .algox-info-card {{
        background: linear-gradient(135deg, rgba(16, 22, 54, 0.88), rgba(8, 14, 38, 0.82)) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(139, 92, 246, 0.28) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.28), 0 0 10px rgba(139, 92, 246, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }}

    /* 18. ALERT TOASTS WITH AMBIENT GLOW */
    div[data-testid="stAlert"] {{
        border-radius: 12px !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.32) !important;
    }}

    /* 19. Anti-Fragmentation & Anti-Wrap Rules */
    .algox-kpi-value, .algox-stat-value, .algox-glass-kpi-value,
    div[data-testid="stMetricValue"], .kpi-number {{
        white-space: nowrap !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        hyphens: none !important;
        letter-spacing: -0.01em !important;
    }}

    /* 20. Compact Glass Status Badges (Pills) with Subtle Semantic Glow */
    .algox-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 650;
        backdrop-filter: blur(10px);
        white-space: nowrap;
    }}
    .algox-badge-purple {{
        background: rgba(124, 58, 237, 0.18);
        border: 1px solid rgba(124, 58, 237, 0.45);
        color: #C4B5FD;
        box-shadow: 0 0 12px rgba(124, 58, 237, 0.52), 0 0 24px rgba(124, 58, 237, 0.28);
    }}
    .algox-badge-blue {{
        background: rgba(37, 99, 235, 0.18);
        border: 1px solid rgba(37, 99, 235, 0.45);
        color: #93C5FD;
        box-shadow: 0 0 12px rgba(37, 99, 235, 0.52), 0 0 24px rgba(37, 99, 235, 0.28);
    }}
    .algox-badge-cyan {{
        background: rgba(6, 182, 212, 0.18);
        border: 1px solid rgba(6, 182, 212, 0.45);
        color: #67E8F9;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.52), 0 0 24px rgba(6, 182, 212, 0.28);
    }}
    .algox-badge-green {{
        background: rgba(34, 197, 94, 0.18);
        border: 1px solid rgba(34, 197, 94, 0.45);
        color: #86EFAC;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.52), 0 0 24px rgba(34, 197, 94, 0.28);
    }}
    .algox-badge-amber {{
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #FCD34D;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.52), 0 0 24px rgba(245, 158, 11, 0.28);
    }}
    .algox-badge-red {{
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid rgba(239, 68, 68, 0.45);
        color: #FCA5A5;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.52), 0 0 24px rgba(239, 68, 68, 0.28);
    }}

    /* 21. Responsive Media Adjustments */
    @media screen and (max-width: 1200px) {{
        .main .block-container {{
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }}
    }}
    @media screen and (max-width: 900px) {{
        .main .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}

    /* Scrollbars */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(124, 58, 237, 0.35); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(6, 182, 212, 0.6); }}

    .algox-footer {{
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 3.5rem;
        padding-top: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.76rem;
        color: {COLOR_TEXT_MUTED};
        flex-wrap: wrap;
        gap: 10px;
    }}
</style>

<!-- Subtle Ambient Cursor Light Source (Behind Glass, 0 Reruns) -->
<div id="algox-cursor-glow" style="position:fixed;top:0;left:0;width:550px;height:550px;margin-left:-275px;margin-top:-275px;border-radius:50%;background:radial-gradient(circle, rgba(124,58,237,0.08) 0%, rgba(37,99,235,0.04) 40%, transparent 70%);pointer-events:none;z-index:1;opacity:0;transition:opacity 0.4s ease;transform:translate3d(-1000px,-1000px,0);will-change:transform;"></div>
<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" style="display:none;" onload="
(function() {{
    if (window.__algoxCursorGlowInit) return;
    window.__algoxCursorGlowInit = true;
    var glow = document.getElementById('algox-cursor-glow');
    if (!glow) {{
        glow = document.createElement('div');
        glow.id = 'algox-cursor-glow';
        glow.style.cssText = 'position:fixed;top:0;left:0;width:550px;height:550px;margin-left:-275px;margin-top:-275px;border-radius:50%;background:radial-gradient(circle, rgba(124,58,237,0.08) 0%, rgba(37,99,235,0.04) 40%, transparent 70%);pointer-events:none;z-index:1;opacity:0;transition:opacity 0.4s ease;transform:translate3d(-1000px,-1000px,0);will-change:transform;';
        document.body.appendChild(glow);
    }}
    var scheduled = false;
    var mx = -1000, my = -1000;
    window.addEventListener('mousemove', function(e) {{
        mx = e.clientX;
        my = e.clientY;
        if (!scheduled) {{
            scheduled = true;
            requestAnimationFrame(function() {{
                if (glow) {{
                    glow.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)';
                    if (glow.style.opacity === '0') glow.style.opacity = '1';
                }}
                scheduled = false;
            }});
        }}
    }}, {{ passive: true }});
    window.addEventListener('mouseleave', function() {{
        if (glow) glow.style.opacity = '0';
    }});
}})();
" />
""")

def render_page_header(title: str, subtitle: str = "", db = None):
    """
    Floating translucent header with clean academic status pills.
    """
    now_dt = datetime.datetime.now()
    date_str = now_dt.strftime("%A, %d %b %Y")
    time_str = now_dt.strftime("%I:%M %p")

    # Top Utility Bar with translucent glass pills
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 1.25rem; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 0.76rem; font-weight: 700; color: #C4B5FD; letter-spacing: 0.08em; text-transform: uppercase;">
                ALGOX COMMAND CENTER
            </span>
            <span style="color: #475569;">&bull;</span>
            <span style="font-size: 0.74rem; color: {COLOR_TEXT_MUTED};">
                DAA Research Suite
            </span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.65rem;">
            <span class="algox-badge algox-badge-green">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: {COLOR_GREEN}; box-shadow: 0 0 6px {COLOR_GREEN};"></span>
                System Status: Operational
            </span>
            <span style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.09); padding: 0.25rem 0.65rem; border-radius: 8px; font-size: 0.74rem; color: #E2E8F0; backdrop-filter: blur(10px);">
                📅 {date_str}
            </span>
            <span style="background: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.25); padding: 0.25rem 0.65rem; border-radius: 8px; font-size: 0.74rem; color: #93C5FD; font-weight: 600; backdrop-filter: blur(10px);">
                ◷ {time_str}
            </span>
            <span class="algox-badge algox-badge-purple">
                Administrator
            </span>
        </div>
    </div>
    """)

    # Main Page Heading
    render_html(f"""
    <div style="padding-bottom: 0.35rem;">
        <h1 style="font-size: 2.15rem; font-weight: 800; margin: 0; color: #F8FAFC; line-height: 1.2; letter-spacing: -0.02em;">
            {title}
        </h1>
        <p style="color: {COLOR_TEXT_MUTED}; font-size: 0.92rem; margin: 6px 0 0 0; line-height: 1.45;">
            {subtitle}
        </p>
    </div>
    <div style="margin-bottom: 1.25rem;"></div>
    """)

def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Legacy alias: no-op since header is centrally rendered by app.py."""
    pass

def render_kpi_row(kpis: List[Dict[str, str]]):
    """
    Renders equal-width floating glass tiles with generous spacing and anti-wrap values.
    """
    cols = st.columns(len(kpis), gap="medium")
    for i, (col, k) in enumerate(zip(cols, kpis)):
        label = k.get('label', '')
        val = k.get('value', '—')
        sub = k.get('subtext', '')
        accent = k.get('color', COLOR_CYAN)

        with col:
            render_html(f"""
            <div class="algox-kpi-card">
                <div style="font-size: 0.72rem; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; font-weight: 700; letter-spacing: 0.06em;">{label}</div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; margin: 4px 0 6px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{val}</div>
                <div style="font-size: 0.75rem; color: {accent}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;">{sub}</div>
            </div>
            """)

def section_header(text: str, icon: str = "", subtitle: str = ""):
    """Renders clean section heading with soft gradient accent bar."""
    subtitle_html = f"<div style='font-size: 0.82rem; color: {COLOR_TEXT_MUTED}; margin-top: 0.25rem; font-weight: 400;'>{subtitle}</div>" if subtitle else ""
    render_html(f"""
    <div style="margin: 0 0 1.05rem 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 3.5px; height: 18px; background: linear-gradient(180deg, {COLOR_PURPLE}, {COLOR_CYAN}); border-radius: 2px;"></div>
            <h3 style="font-size: 1.18rem; font-weight: 700; color: #F8FAFC; margin: 0; letter-spacing: -0.01em;">
                {text}
            </h3>
        </div>
        {subtitle_html}
    </div>
    """)

def empty_state(icon: str, title: str, message: str, button_label: str = "", target_page: str = ""):
    """Renders compact translucent empty state with clear hierarchy and bounded height."""
    btn_id = f"empty_btn_{title.replace(' ', '_').lower()}"
    with st.container(border=True):
        render_html(f"""
        <div style="text-align: center; padding: 2rem 1rem;">
            <div style="font-size: 2.2rem; margin-bottom: 0.45rem;">{icon}</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">{title}</div>
            <div style="color: {COLOR_TEXT_MUTED}; font-size: 0.86rem; margin: 0 auto; max-width: 440px; line-height: 1.5;">{message}</div>
        </div>
        """)
        if button_label and target_page:
            c1, c2, c3 = st.columns([1, 1.6, 1])
            with c2:
                if st.button(button_label, use_container_width=True, key=btn_id, type="primary"):
                    st.session_state['current_page'] = target_page
                    st.rerun()

def info_card(title: str, content: str):
    render_html(f"""
    <div class="algox-info-card" style="border-left: 4px solid {COLOR_CYAN}; margin: 8px 0;">
        <div style="font-weight: 700; font-size: 0.92rem; color: #E0F2FE; margin-bottom: 4px;">{title}</div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.55;">{content}</div>
    </div>
    """)

def warning_card(title: str, content: str):
    render_html(f"""
    <div class="algox-info-card" style="border-left: 4px solid {COLOR_AMBER}; margin: 8px 0; background: rgba(245,158,11,0.06);">
        <div style="font-weight: 700; font-size: 0.92rem; color: #FEF3C7; margin-bottom: 4px;">⚠️ {title}</div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.55;">{content}</div>
    </div>
    """)

def success_card(title: str, content: str):
    render_html(f"""
    <div class="algox-info-card" style="border-left: 4px solid {COLOR_GREEN}; margin: 8px 0; background: rgba(34,197,94,0.06);">
        <div style="font-weight: 700; font-size: 0.92rem; color: #DCFCE7; margin-bottom: 4px;">✅ {title}</div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.55;">{content}</div>
    </div>
    """)

def danger_card(title: str, content: str):
    render_html(f"""
    <div class="algox-info-card" style="border-left: 4px solid {COLOR_RED}; margin: 8px 0; background: rgba(239,68,68,0.06);">
        <div style="font-weight: 700; font-size: 0.92rem; color: #FEE2E2; margin-bottom: 4px;">⛔ {title}</div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.55;">{content}</div>
    </div>
    """)

def complexity_badge(complexity: str) -> str:
    c = complexity.lower().replace(" ", "")
    if "o(1)" in c:
        bg, text = "rgba(34, 197, 94, 0.15)", "#4ADE80"
    elif "o(logn)" in c:
        bg, text = "rgba(6, 182, 212, 0.15)", "#22D3EE"
    elif "o(nlogn)" in c:
        bg, text = "rgba(245, 158, 11, 0.15)", "#FBBF24"
    elif "o(n²)" in c or "o(n^2)" in c:
        bg, text = "rgba(239, 68, 68, 0.15)", "#F87171"
    elif "o(n)" in c:
        bg, text = "rgba(37, 99, 235, 0.15)", "#60A5FA"
    else:
        bg, text = "rgba(124, 58, 237, 0.15)", "#C4B5FD"
    return f"<span style='background:{bg}; color:{text}; font-size:0.75rem; font-weight:700; padding:3px 9px; border-radius:6px; font-family:monospace; border:1px solid rgba(255,255,255,0.06);'>{complexity}</span>"

def status_badge(label: str, status: str = 'info') -> str:
    color_map = {
        'success': ('rgba(34,197,94,0.15)', '#86EFAC', 'rgba(34,197,94,0.3)'),
        'warning': ('rgba(245,158,11,0.15)', '#FCD34D', 'rgba(245,158,11,0.3)'),
        'danger': ('rgba(239,68,68,0.15)', '#FCA5A5', 'rgba(239,68,68,0.3)'),
        'info': ('rgba(6,182,212,0.15)', '#67E8F9', 'rgba(6,182,212,0.3)')
    }
    bg, fg, border = color_map.get(status, color_map['info'])
    return f"<span style='background:{bg}; color:{fg}; border:1px solid {border}; font-size:0.74rem; font-weight:600; padding:2px 8px; border-radius:9999px; backdrop-filter:blur(8px);'>{label}</span>"

def format_time(seconds: float) -> str:
    if seconds is None:
        return "—"
    if seconds <= 0:
        return "<0.01 ms"
    ms = seconds * 1000.0
    if ms < 0.01:
        return "<0.01 ms"
    elif ms < 1.0:
        return f"{ms:.2f} ms"
    elif seconds < 1.0:
        return f"{ms:.2f} ms"
    else:
        return f"{seconds:.3f} s"

def format_number(n: int) -> str:
    if n is None:
        return "0"
    return f"{n:,}"

def get_plotly_layout(title: str = "", height: int = 340, x_title: str = "", y_title: str = "") -> dict:
    return dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(color=COLOR_TEXT, size=13, family="-apple-system, sans-serif"),
            x=0.01
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(10, 15, 38, 0.35)",
        font=dict(color=COLOR_TEXT_MUTED, size=11),
        margin=dict(l=45, r=25, t=45, b=40),
        height=height,
        xaxis=dict(
            title=dict(text=x_title, font=dict(color=COLOR_TEXT_MUTED, size=11)),
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color=COLOR_TEXT_MUTED, size=10)
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color=COLOR_TEXT_MUTED, size=11)),
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color=COLOR_TEXT_MUTED, size=10)
        ),
        legend=dict(
            bgcolor="rgba(10, 15, 36, 0.65)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            font=dict(color=COLOR_TEXT, size=10)
        ),
        hoverlabel=dict(
            bgcolor="#0E1430",
            font_size=11,
            font_color=COLOR_TEXT,
            bordercolor=COLOR_PURPLE
        ),
        autosize=True
    )

def render_footer():
    """Renders standard academic platform footer."""
    render_html(f"""
    <div class="algox-footer">
        <div>
            <b>ALGOX</b> &mdash; Algorithm Intelligence & Benchmarking Platform
        </div>
        <div>
            Design & Analysis of Algorithms Academic Platform &bull; Computer Science & Engineering
        </div>
    </div>
    """)

def render_sidebar(db) -> str:
    """
    Renders the translucent glass sidebar with glowing active pill.
    """
    current_page = st.session_state.get('current_page', 'Dashboard')

    with st.sidebar:
        # ALGOX Brand Logo block
        render_html(f"""
        <div style="padding: 0.4rem 0.25rem 1rem 0.25rem; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 0.85rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, {COLOR_PURPLE}, {COLOR_CYAN}); display: flex; align-items: center; justify-content: center; font-weight: 850; font-size: 1.2rem; color: #FFFFFF; box-shadow: 0 0 16px rgba(124, 58, 237, 0.45);">
                    A
                </div>
                <div>
                    <div style="font-size: 1.3rem; font-weight: 800; letter-spacing: 0.06em; color: #FFFFFF; line-height: 1.1;">
                        ALGOX
                    </div>
                    <div style="font-size: 0.64rem; color: {COLOR_CYAN}; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;">
                        Algorithm Intelligence Platform
                    </div>
                </div>
            </div>
        </div>
        """)

        # GROUP 1: LAB WORKBENCH
        render_html(f"<div style='font-size: 0.68rem; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.08em; margin: 0.35rem 0.25rem 0.25rem 0.25rem;'>LAB WORKBENCH</div>")
        nav_workbench = [
            ("Dashboard", ":material/home:"),
            ("Visualizer", ":material/visibility:"),
            ("Algorithms", ":material/account_tree:"),
            ("Benchmark Lab", ":material/science:"),
            ("Comparison", ":material/compare_arrows:"),
            ("Algorithm Battle", ":material/bolt:")
        ]
        for page_name, icon_spec in nav_workbench:
            is_active = (current_page == page_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(page_name, icon=icon_spec, type=btn_type, key=f"sb_{page_name}", use_container_width=True):
                st.session_state['current_page'] = page_name
                st.rerun()

        # GROUP 2: DATA & EXPERIMENTS
        render_html(f"<div style='border-top: 1px solid rgba(255,255,255,0.07); margin: 0.65rem 0.25rem 0.35rem 0.25rem;'></div>")
        render_html(f"<div style='font-size: 0.68rem; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.08em; margin: 0.2rem 0.25rem 0.25rem 0.25rem;'>DATA & EXPERIMENTS</div>")
        nav_data = [
            ("Dataset Lab", ":material/dataset:"),
            ("Experiment Workspace", ":material/biotech:"),
            ("History", ":material/history:"),
            ("Saved Experiments", ":material/bookmark:"),
            ("Reports", ":material/description:")
        ]
        for page_name, icon_spec in nav_data:
            is_active = (current_page == page_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(page_name, icon=icon_spec, type=btn_type, key=f"sb_{page_name}", use_container_width=True):
                st.session_state['current_page'] = page_name
                st.rerun()

        # GROUP 3: ANALYSIS
        render_html(f"<div style='border-top: 1px solid rgba(255,255,255,0.07); margin: 0.65rem 0.25rem 0.35rem 0.25rem;'></div>")
        render_html(f"<div style='font-size: 0.68rem; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.08em; margin: 0.2rem 0.25rem 0.25rem 0.25rem;'>ANALYSIS</div>")
        nav_analysis = [
            ("Recommendation", ":material/lightbulb:"),
            ("Complexity Analyzer", ":material/functions:"),
            ("Graph Algorithms", ":material/hub:")
        ]
        for page_name, icon_spec in nav_analysis:
            is_active = (current_page == page_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(page_name, icon=icon_spec, type=btn_type, key=f"sb_{page_name}", use_container_width=True):
                st.session_state['current_page'] = page_name
                st.rerun()

        # GROUP 4: SYSTEM
        render_html(f"<div style='border-top: 1px solid rgba(255,255,255,0.07); margin: 0.65rem 0.25rem 0.35rem 0.25rem;'></div>")
        render_html(f"<div style='font-size: 0.68rem; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.08em; margin: 0.2rem 0.25rem 0.25rem 0.25rem;'>SYSTEM</div>")
        nav_system = [
            ("Settings", ":material/settings:"),
            ("About", ":material/info:")
        ]
        for page_name, icon_spec in nav_system:
            is_active = (current_page == page_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(page_name, icon=icon_spec, type=btn_type, key=f"sb_{page_name}", use_container_width=True):
                st.session_state['current_page'] = page_name
                st.rerun()

        # Bottom System Monitor Telemetry
        render_html(f"""
        <div style="margin-top: 1.5rem; padding: 0.85rem; border-radius: 12px; background: rgba(5, 8, 22, 0.45); border: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-size: 0.68rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">SYSTEM MONITOR</span>
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {COLOR_GREEN}; box-shadow: 0 0 6px {COLOR_GREEN};"></span>
            </div>
            <div style="font-size: 0.76rem; color: #E2E8F0; font-weight: 600;">
                Core: <span style="color: {COLOR_CYAN};">13 Active</span> &bull; DB: <span style="color: {COLOR_GREEN};">SQLite Online</span>
            </div>
            <div style="font-size: 0.68rem; color: #94A3B8; margin-top: 3px;">
                DAA Intelligence & Benchmarking
            </div>
        </div>
        """)

    return current_page
