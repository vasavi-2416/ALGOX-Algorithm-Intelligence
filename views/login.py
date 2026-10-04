"""
ALGOX — Administrator Authentication View
Two-Column Split Layout:
  LEFT  (56%): Existing ALGOX project image panel ONLY (untouched)
  RIGHT (38%): Compact, premium glassmorphism Administrator Sign In card

Inputs (Strict Spec):
  - Width: 100% of login form, Height: ~50px
  - Background: rgba(255, 255, 255, 0.06), backdrop-filter: blur(12px)
  - Border: 1px solid rgba(255, 255, 255, 0.12), border-radius: 10px
  - Box-shadow: none in normal state
  - Padding: 0 16px, Font-size: 15px
  - Text color: #ffffff, Placeholder: rgba(255, 255, 255, 0.45)
  - Hover: slightly brighter glass, subtle cyan/purple border, no strong glow
  - Focus: border 1px solid rgba(0, 190, 255, 0.75), box-shadow: 0 0 0 2px rgba(0,190,255,0.08), 0 0 18px rgba(0,190,255,0.12)
  - NEVER show a red border
  - Eye icon: aligned to far right, vertically centered, subtle white/light-gray
  - No 'Press Enter to apply' helper text
  - Autocomplete: username & current-password

Credentials: admin / algox
"""
import os
from PIL import Image
import streamlit as st
from core.ui import inject_css, render_html, COLOR_PURPLE, COLOR_CYAN

IMAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "algox_login_hero.png")
)

_CSS_TEMPLATE = """
<style>
/* ── REMOVE STREAMLIT CHROME ── */
#MainMenu, header, footer,
section[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"] {
    display: none !important;
}

/* ── VIEWPORT BACKGROUND: DEEP NAVY / PURPLE GLOW ── */
html, body {
    overflow: hidden !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stApp {
    background: #030814 !important;
    background-image:
        radial-gradient(ellipse at 78% 10%, rgba(37, 99, 235, 0.42) 0%, rgba(37, 99, 235, 0.14) 24%, transparent 45%),
        radial-gradient(ellipse at 92% 30%, rgba(124, 58, 237, 0.24) 0%, transparent 32%),
        radial-gradient(ellipse at 8% 85%, rgba(109, 40, 217, 0.20) 0%, transparent 32%),
        radial-gradient(ellipse at 50% 50%, rgba(6, 182, 212, 0.04) 0%, transparent 55%) !important;
    background-attachment: fixed !important;
    overflow: hidden !important;
    height: 100vh !important;
    min-height: 100vh !important;
}

/* Subtle cosmic micro-particles */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1.4px 1.4px at 12% 16%, rgba(147, 197, 253, 0.65) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 28% 9%, rgba(196, 181, 253, 0.50) 0%, transparent 100%),
        radial-gradient(1.6px 1.6px at 68% 6%, rgba(255, 255, 255, 0.55) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 86% 25%, rgba(147, 197, 253, 0.50) 0%, transparent 100%),
        radial-gradient(1.4px 1.4px at 42% 68%, rgba(196, 181, 253, 0.38) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 94% 64%, rgba(147, 197, 253, 0.45) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 6% 48%, rgba(255, 255, 255, 0.38) 0%, transparent 100%),
        radial-gradient(1.6px 1.6px at 58% 88%, rgba(196, 181, 253, 0.42) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 78% 74%, rgba(147, 197, 253, 0.38) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── BLOCK CONTAINER: BALANCED DESKTOP VIEWPORT ── */
.main .block-container {
    max-width: 1420px !important;
    width: 95vw !important;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: clamp(1.2rem, 3vw, 3rem) !important;
    padding-right: clamp(1.2rem, 3vw, 3rem) !important;
    margin: 0 auto !important;
    min-height: 94vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    position: relative !important;
    z-index: 1 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ── HORIZONTAL TWO-COLUMN ALIGNMENT ── */
div[data-testid="stHorizontalBlock"],
.stHorizontalBlock {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: clamp(24px, 4vw, 54px) !important;
    background: transparent !important;
    border: none !important;
}

/* ── LEFT COLUMN (56%): ALGOX HERO IMAGE PANEL ── */
div[data-testid="stColumn"]:first-child,
div[data-testid="column"]:first-child,
.stColumn:first-child {
    flex: 56 !important;
    min-width: 50% !important;
    max-width: 58% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
}

div[data-testid="stColumn"]:first-child div[data-testid="stImage"],
div[data-testid="column"]:first-child div[data-testid="stImage"],
.stColumn:first-child .stImage {
    border-radius: 20px !important;
    border: 1px solid rgba(59, 130, 246, 0.30) !important;
    box-shadow:
        0 0 0 1px rgba(37, 99, 235, 0.12),
        0 0 50px rgba(37, 99, 235, 0.22),
        0 0 100px rgba(124, 58, 237, 0.14),
        0 20px 50px rgba(0, 0, 0, 0.65) !important;
    overflow: hidden !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease !important;
}

div[data-testid="stColumn"]:first-child div[data-testid="stImage"]:hover,
.stColumn:first-child .stImage:hover {
    transform: scale(1.01) !important;
    border-color: rgba(96, 165, 250, 0.52) !important;
    box-shadow:
        0 0 0 1px rgba(37, 99, 235, 0.20),
        0 0 65px rgba(37, 99, 235, 0.32),
        0 0 120px rgba(124, 58, 237, 0.20),
        0 24px 60px rgba(0, 0, 0, 0.70) !important;
}

div[data-testid="stColumn"]:first-child img,
.stColumn:first-child img {
    border-radius: 19px !important;
    object-fit: cover !important;
    width: 100% !important;
    max-height: 560px !important;
    display: block !important;
}

/* ── RIGHT COLUMN (38%): CONTAINER RESET (NO EXTRA OUTER BOX) ── */
div[data-testid="stColumn"]:nth-child(2),
div[data-testid="column"]:nth-child(2),
.stColumn:nth-child(2) {
    flex: 38 !important;
    min-width: 380px !important;
    max-width: 440px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Strip any border or background from intermediate wrappers */
div[data-testid="stColumn"]:nth-child(2) > div,
.stColumn:nth-child(2) > div,
div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 100% !important;
    padding: 0 !important;
}

/* ── EXACTLY ONE FROSTED GLASS SIGN-IN CARD ── */
div[data-testid="stColumn"]:nth-child(2) .stVerticalBlock:has([data-testid="stTextInput"]),
div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlock"]:has([data-testid="stTextInput"]) {
    background: rgba(8, 18, 48, 0.70) !important;
    background-image: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(99, 102, 241, 0.04) 50%, rgba(6, 182, 212, 0.04) 100%) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
    border: 1.5px solid rgba(56, 189, 248, 0.40) !important;
    border-radius: 26px !important;
    padding: 36px 32px 30px 32px !important;
    box-shadow:
        0 0 0 1px rgba(56, 189, 248, 0.15),
        0 0 45px rgba(56, 189, 248, 0.25),
        0 0 90px rgba(124, 58, 237, 0.22),
        0 25px 60px rgba(0, 0, 0, 0.70),
        inset 0 1px 1px rgba(255, 255, 255, 0.25),
        inset 0 -1px 1px rgba(255, 255, 255, 0.05) !important;
    width: 100% !important;
    max-width: 420px !important;
    margin: 0 auto !important;
    position: relative !important;
    overflow: visible !important;
    display: flex !important;
    flex-direction: column !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stColumn"]:nth-child(2) .stVerticalBlock:has([data-testid="stTextInput"]):hover,
div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlock"]:has([data-testid="stTextInput"]):hover {
    border-color: rgba(56, 189, 248, 0.65) !important;
    box-shadow:
        0 0 0 1px rgba(56, 189, 248, 0.25),
        0 0 60px rgba(56, 189, 248, 0.35),
        0 0 110px rgba(124, 58, 237, 0.30),
        0 30px 70px rgba(0, 0, 0, 0.75),
        inset 0 1px 1px rgba(255, 255, 255, 0.35) !important;
}

/* ── REMOVE STREAMLIT 'PRESS ENTER TO APPLY' HELPER INSTRUCTIONS ── */
[data-testid="InputInstructions"],
div[data-testid="InputInstructions"],
span[data-testid="InputInstructions"],
.stTextInput [data-testid="InputInstructions"],
.stTextInput small,
div:has(> [data-testid="InputInstructions"]) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* ── FORM LABELS & FIELD SPACING ── */
div[data-testid="stTextInput"] {
    margin-bottom: 12px !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p {
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    margin-bottom: 8px !important;
    letter-spacing: 0.01em !important;
}

/* ── TRANSPARENT BASEWEB WRAPPERS ── */
div[data-testid="stTextInput"] div[data-baseweb="base-input"],
div[data-testid="stTextInput"] div[data-baseweb="input"] > div,
div[data-testid="stTextInput"] input {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* ── USERNAME & PASSWORD INPUT FIELDS (EXACT SPECIFICATION) ── */
div[data-testid="stTextInput"] div[data-baseweb="input"] {
    width: 100% !important;
    height: 50px !important;
    min-height: 50px !important;
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
    position: relative !important;
}

/* ── HOVER STATE ── */
div[data-testid="stTextInput"] div[data-baseweb="input"]:hover {
    background: rgba(255, 255, 255, 0.09) !important;
    border: 1px solid rgba(124, 58, 237, 0.35) !important;
    box-shadow: 0 0 10px rgba(0, 190, 255, 0.08) !important;
}

/* ── FOCUS STATE (NO RED BORDER, SOFT CYAN GLOW) ── */
div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(0, 190, 255, 0.75) !important;
    border-color: rgba(0, 190, 255, 0.75) !important;
    box-shadow: 0 0 0 2px rgba(0, 190, 255, 0.08), 0 0 18px rgba(0, 190, 255, 0.12) !important;
    outline: none !important;
}

/* Eradicate red outline/border anywhere in text inputs */
div[data-testid="stTextInput"] *,
div[data-testid="stTextInput"] *:focus,
div[data-testid="stTextInput"] *:focus-visible {
    outline: none !important;
}

/* ── INPUT TEXT & PLACEHOLDER WITH GENEROUS INNER PADDING ── */
div[data-testid="stTextInput"] input {
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
    padding-left: 20px !important;
    padding-right: 16px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin: 0 !important;
    line-height: 50px !important;
    height: 100% !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    box-sizing: border-box !important;
}

div[data-testid="stTextInput"]:has(input[type="password"]) input {
    padding-right: 44px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255, 255, 255, 0.45) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
}

/* Prevent yellow/white autofill overlay */
div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover, 
div[data-testid="stTextInput"] input:-webkit-autofill:focus {
    -webkit-text-fill-color: #FFFFFF !important;
    -webkit-box-shadow: 0 0 0px 1000px rgba(18, 28, 56, 0.98) inset !important;
    transition: background-color 5000s ease-in-out 0s !important;
}

/* ── EYE ICON BUTTON AT THE FAR RIGHT ── */
div[data-testid="stTextInput"] div[data-baseweb="input"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: rgba(255, 255, 255, 0.65) !important;
    padding: 0 !important;
    margin: 0 14px 0 6px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100% !important;
    transition: color 0.2s ease, transform 0.2s ease !important;
}

div[data-testid="stTextInput"] div[data-baseweb="input"] button:hover {
    color: rgba(0, 190, 255, 0.95) !important;
    transform: scale(1.08) !important;
}

/* ── SIGN IN BUTTON: PURPLE → BLUE → CYAN GRADIENT ── */
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #7C3AED 0%, #2563EB 50%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14.5px !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 12px !important;
    height: 50px !important;
    min-height: 50px !important;
    box-shadow: 0 6px 28px rgba(37, 99, 235, 0.50), 0 0 25px rgba(6, 182, 212, 0.35) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease !important;
    margin-top: 6px !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 38px rgba(124, 58, 237, 0.70), 0 0 35px rgba(6, 182, 212, 0.60) !important;
    filter: brightness(1.12) !important;
}

div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── AMBIENT CURSOR GLOW ── */
#algox-cursor-glow {
    position: fixed; top: 0; left: 0;
    width: 440px; height: 440px;
    margin-left: -220px; margin-top: -220px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    background: radial-gradient(circle,
        rgba(99, 102, 241, 0.10) 0%,
        rgba(37, 99, 235, 0.07) 45%,
        rgba(6, 182, 212, 0.04) 70%,
        transparent 85%);
    filter: blur(95px);
    opacity: 0;
    transition: opacity 0.35s ease;
}

/* ── RESPONSIVE MOBILE / TABLET ── */
@media (max-width: 860px) {
    html, body, .stApp { overflow: auto !important; height: auto !important; }
    div[data-testid="stHorizontalBlock"],
    .stHorizontalBlock {
        flex-direction: column !important;
        gap: 24px !important;
    }
    div[data-testid="stColumn"]:first-child,
    .stColumn:first-child {
        max-width: 100% !important;
    }
    div[data-testid="stColumn"]:nth-child(2),
    .stColumn:nth-child(2) {
        max-width: 100% !important;
    }
}
</style>

<div id="algox-cursor-glow"></div>
<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
     style="display:none;"
     onload="(function() {
         if (window.__algoxCG) return;
         window.__algoxCG = true;
         var g = document.getElementById('algox-cursor-glow');
         if (!g) return;
         var mx = -500, my = -500, cx = -500, cy = -500, t = false;
         window.addEventListener('mousemove', function(e) {
             mx = e.clientX; my = e.clientY;
             g.style.opacity = '1';
             if (!t) {
                 requestAnimationFrame(function() {
                     cx += (mx - cx) * 0.14;
                     cy += (my - cy) * 0.14;
                     g.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
                     t = false;
                 });
                 t = true;
             }
         }, {passive: true});
     })()" />
"""


def render_login() -> bool:
    inject_css()

    # Inject CSS
    render_html(_CSS_TEMPLATE)

    # ── TWO-COLUMN SPLIT: 56% LEFT (IMAGE) / 38% RIGHT (COMPACT CARD) ──
    left_col, right_col = st.columns([56, 38], gap="large")

    # ════════════════════════════════════════════════════════════════
    # LEFT COLUMN: ALGOX HERO IMAGE PANEL ONLY
    # ════════════════════════════════════════════════════════════════
    with left_col:
        if os.path.exists(IMAGE_PATH):
            img = Image.open(IMAGE_PATH)
            st.image(img, width="stretch")
        else:
            st.warning(f"ALGOX hero image not found: {IMAGE_PATH}")

    # ════════════════════════════════════════════════════════════════
    # RIGHT COLUMN: EXACTLY ONE COMPACT GLASSMORPHISM SIGN-IN CARD
    # ════════════════════════════════════════════════════════════════
    with right_col:
        # Card Header: Logo badge + ALGOX title + Administrator Sign In
        render_html(f"""
<!-- ALGOX Logo Icon + ALGOX + Subtitle -->
<div style="text-align:center; margin-bottom:0.9rem; position:relative;">
    <div style="display:inline-flex; align-items:center; justify-content:center;
        width:48px; height:48px; border-radius:14px;
        background:linear-gradient(135deg,{COLOR_PURPLE} 0%,#2563EB 55%,{COLOR_CYAN} 100%);
        font-size:1.75rem; color:#FFFFFF; font-weight:900;
        box-shadow:0 0 28px rgba(124,58,237,0.70), 0 0 16px rgba(6,182,212,0.40);
        margin-bottom:0.4rem;">A</div>
    <div style="font-size:23px; font-weight:800; letter-spacing:0.09em; color:#FFFFFF; line-height:1.1;">ALGOX</div>
    <div style="font-size:10px; color:#38BDF8; font-weight:700; text-transform:uppercase; letter-spacing:1.8px; margin-top:3px;">ALGORITHM INTELLIGENCE PLATFORM</div>
</div>

<!-- Administrator Sign In + Subtitle -->
<div style="text-align:center; margin-bottom:1.2rem; position:relative;">
    <div style="font-size:26px; font-weight:800; color:#FFFFFF; letter-spacing:-0.015em; margin-bottom:0.3rem;">Administrator Sign In</div>
    <div style="font-size:13px; color:#94A3B8; line-height:1.5; max-width:290px; margin:0 auto;">
        Sign in to access the ALGOX Algorithm Intelligence &amp;<br>Benchmarking Platform.
    </div>
</div>
""")

        # Form Inputs with appropriate autocomplete behavior
        username = st.text_input(
            "Username",
            value="",
            placeholder="Enter username",
            autocomplete="username",
            key="login_username"
        )
        password = st.text_input(
            "Password",
            value="",
            type="password",
            placeholder="Enter password",
            autocomplete="current-password",
            key="login_password"
        )

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        # Gradient Action Button
        login_btn = st.button(
            "SIGN IN TO ALGOX  →",
            width="stretch",
            type="primary",
            key="login_btn"
        )

        if login_btn:
            if username.strip() == "admin" and password.strip() == "algox":
                st.session_state["authenticated"] = True
                st.session_state["current_page"] = "Dashboard"
                st.rerun()
            else:
                st.markdown(
                    """<div style="background:rgba(239,68,68,0.12);
                        border:1px solid rgba(248,113,113,0.38);
                        border-radius:10px; padding:9px 12px;
                        font-size:12.5px; color:rgba(248,113,113,0.95);
                        margin-top:8px; text-align:center;">
                        Invalid username or password.
                    </div>""",
                    unsafe_allow_html=True,
                )

        # Divider + Secure Authentication + Project Environment
        render_html("""
<div style="border-top:1px solid rgba(56,189,248,0.22); margin:1.3rem 0 0.75rem;"></div>
<div style="text-align:center; padding-bottom:4px;">
    <div style="display:inline-flex; align-items:center; gap:7px;
        font-size:13px; color:#22C55E; font-weight:600; margin-bottom:4px;">
        <span style="display:inline-block; width:7px; height:7px; border-radius:50%;
            background:#22C55E; box-shadow:0 0 10px rgba(34,197,94,0.90);"></span>
        Secure Authentication
    </div>
    <div style="font-size:11.5px; color:#94A3B8;">
        ALGOX Academic Project Environment
    </div>
</div>
""")

    return st.session_state.get("authenticated", False)
