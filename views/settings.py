"""
ALGOX — Application Settings Module
Persistent configuration interface stored directly in SQLite settings table.
Includes safe data management actions with explicit safety confirmations.
"""
import streamlit as st
import pandas as pd
from core.benchmark import run_full_verification_suite
from core.ui import (
    render_html,
    section_header,
    warning_card,
    danger_card,
    success_card,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_RED,
    COLOR_TEXT_MUTED
,
    render_footer
)

def render_settings(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">⚙️</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(94,234,212,0.85);display:block;">ALGOX · SETTINGS</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Application Settings</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Persistent configuration interface. Benchmark defaults, visualizer preferences, and data management — all stored directly in the SQLite settings table.
</p>
</div>
""")

    all_settings = db.get_all_settings()

    # 1. Benchmark Defaults
    section_header("Benchmark Defaults")
    with st.container(border=True):
        b1, b2, b3 = st.columns(3)
        with b1:
            cur_def_size = int(all_settings.get('default_dataset_size', 500))
            new_def_size = st.number_input("Default Benchmark N", min_value=50, max_value=20000, value=cur_def_size, step=100, key="set_def_size")
        with b2:
            cur_reps = int(all_settings.get('default_repetitions', 3))
            new_reps = st.slider("Default Repetitions", min_value=1, max_value=10, value=cur_reps, key="set_reps")
        with b3:
            cur_safe_n = int(all_settings.get('max_safe_n_quadratic', 5000))
            new_safe_n = st.number_input("Max Safe N (Quadratic)", min_value=500, max_value=20000, value=cur_safe_n, step=500, key="set_safe_n")

    # 2. Visualizer Settings
    section_header("Visualizer Preferences")
    with st.container(border=True):
        v1, v2 = st.columns(2)
        with v1:
            cur_viz_n = int(all_settings.get('visualizer_array_size', 25))
            new_viz_n = st.slider("Default Visualizer Array Size", min_value=8, max_value=50, value=cur_viz_n, step=1, key="set_viz_n")
        with v2:
            cur_speed = int(all_settings.get('animation_speed_ms', 50))
            new_speed = st.slider("Step Delay (ms)", min_value=10, max_value=500, value=cur_speed, step=10, key="set_anim_speed")

    # Save Settings Button
    if st.button("Save Configuration", use_container_width=True, key="set_save_btn"):
        db.set_setting('default_dataset_size', str(new_def_size))
        db.set_setting('default_repetitions', str(new_reps))
        db.set_setting('max_safe_n_quadratic', str(new_safe_n))
        db.set_setting('visualizer_array_size', str(new_viz_n))
        db.set_setting('animation_speed_ms', str(new_speed))
        success_card("Settings Persisted", "Configuration values successfully saved to SQLite settings table.")

    # 3. Formal Algorithm Verification Suite (Phase 23)
    section_header("Algorithm Verification & Health Suite", icon="🧪", subtitle="Run automated correctness tests against all 13 algorithms across edge cases.")
    with st.container(border=True):
        st.markdown(
            "<div style='font-size:0.85rem; color:#94A3B8; margin-bottom:12px;'>"
            "Executes real edge cases (empty array, single element, duplicates, sorted, reverse sorted, negative values, boundary searches, disconnected graphs) "
            "and verifies against mathematical ground truth."
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("▶ Run Formal Verification Suite (All 13 Algorithms)", key="set_run_diag_btn", type="primary", use_container_width=True):
            with st.spinner("Executing rigorous invariant checks across 75 test configurations..."):
                diag_res = run_full_verification_suite()
                st.session_state['latest_diag_res'] = diag_res

        diag = st.session_state.get('latest_diag_res')
        if diag:
            d_c1, d_c2, d_c3, d_c4 = st.columns(4, gap="medium")
            with d_c1:
                render_html(f"""
                <div class="algox-stat-card">
                    <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">TOTAL TESTS</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">{diag['total_tests']}</div>
                </div>
                """)
            with d_c2:
                render_html(f"""
                <div class="algox-stat-card">
                    <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">PASSED</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#22C55E;">{diag['passed']}</div>
                </div>
                """)
            with d_c3:
                fail_color = "#EF4444" if diag['failed'] > 0 else "#94A3B8"
                render_html(f"""
                <div class="algox-stat-card">
                    <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">FAILED</div>
                    <div style="font-size:1.6rem; font-weight:800; color:{fail_color};">{diag['failed']}</div>
                </div>
                """)
            with d_c4:
                render_html(f"""
                <div class="algox-stat-card">
                    <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">VERIFICATION RATE</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#06B6D4;">{diag['rate']:.1f}%</div>
                </div>
                """)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            df_diag = pd.DataFrame(diag['details'])
            st.dataframe(df_diag, use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 4. Data Management & Dangerous Actions
    section_header("Data Management")
    with st.container(border=True):
        render_html(f"""
        <div style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem; margin-bottom: 0.5rem;">
            SQLite Diagnostic Telemetry
        </div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;">
            <div>• <b>Storage Path:</b> <code>{db.db_path}</code></div>
            <div>• <b>Total Experiments Stored:</b> {db.get_experiment_count():,} records</div>
            <div>• <b>Curated Saved Experiments:</b> {len(db.get_saved_experiments()):,} records</div>
            <div>• <b>Generated Datasets:</b> {db.get_dataset_count():,} records</div>
        </div>
        """)

    with st.expander("⚠️ Danger Zone — Purge Database History"):
        danger_card("Destructive Action", "Clearing history permanently drops all logged benchmark records and saved experiments from the SQLite database.")
        confirm_text = st.text_input("Type 'DELETE' to confirm permanent purge", key="set_purge_confirm")
        if st.button("🚨 PERMANENTLY PURGE EXPERIMENT HISTORY", disabled=(confirm_text != "DELETE"), key="set_purge_btn"):
            db.clear_history()
            st.success("All experiment records successfully purged from database.")
            st.rerun()

    with st.expander("🔄 Reset All Settings to Factory Defaults"):
        if st.button("Reset Settings to Defaults", key="set_reset_btn"):
            db.reset_settings()
            st.success("Platform settings restored to default values.")
            st.rerun()

    render_footer()
