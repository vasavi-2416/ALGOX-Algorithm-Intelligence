import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.dataset import generate_dataset
from core.benchmark import run_benchmark
from core.complexity import ALGORITHM_COMPLEXITY
from core.ui import (inject_css, render_page_header, section_header,
                     success_card, warning_card, danger_card, render_kpi_row,
                     get_plotly_layout, format_time, format_number,
                     complexity_badge, render_html)
from database.database import AlgoxDB

ALL_ALGOS = list(ALGORITHM_COMPLEXITY.keys())
SORTING_ALGOS = [a for a in ALL_ALGOS if ALGORITHM_COMPLEXITY[a].get("category") == "Sorting"]
QUADRATIC = {"Bubble Sort", "Selection Sort", "Insertion Sort"}


def render_workspace(db: AlgoxDB):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">🔬</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(37,99,235,0.9);display:block;">ALGOX · EXPERIMENT WORKSPACE</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Experiment Workspace</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Integrated scientific workbench — configure, execute, analyze, and document algorithm experiments with full persistence to SQLite.
</p>
</div>
""")

    tab_cfg, tab_exec, tab_analyze, tab_save = st.tabs([
        "1. ⚙️ Configure", "2. ▶️ Execute", "3. 📊 Analyze", "4. 💾 Save"
    ])

    # ── TAB 1: CONFIGURE ──────────────────────────────────────────────────────
    with tab_cfg:
        section_header("Experiment Configuration", icon="⚙️", subtitle="Select algorithm candidate, dataset distribution, input scale, and repetitions.")

        with st.container(border=True):
            col_a, col_b = st.columns(2, gap="medium")
            with col_a:
                algo = st.selectbox(
                    "Algorithm Candidate",
                    options=SORTING_ALGOS,
                    index=SORTING_ALGOS.index("Merge Sort") if "Merge Sort" in SORTING_ALGOS else 0,
                    key="ws_algo"
                )
                dist = st.selectbox(
                    "Dataset Distribution",
                    ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicate Heavy"],
                    key="ws_dist"
                )
            with col_b:
                n = st.slider("Input Size (N)", min_value=50, max_value=10000,
                              value=500, step=50, key="ws_n")
                reps = st.slider("Repetitions (Runs)", min_value=1, max_value=10,
                                 value=3, key="ws_reps")

            seed_v = st.number_input("Random Seed (0 = random / unseeded)", min_value=0,
                                     max_value=99999, value=42, key="ws_seed")
            seed = int(seed_v) if seed_v > 0 else None

            # Show complexity preview
            info = ALGORITHM_COMPLEXITY.get(algo, {})
            if info:
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                render_html(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px 16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-weight:700;color:#F1F5F9;font-size:0.92rem;">{algo} Theoretical Profile</span>
                        <span style="color:#06B6D4;font-size:0.75rem;font-weight:600;">{info.get('paradigm','')}</span>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;font-size:0.8rem;margin-top:8px;">
                        <div><span style="color:#94A3B8;">Best Case:</span> <b style="color:#22C55E;">{info.get('best','—')}</b></div>
                        <div><span style="color:#94A3B8;">Average Case:</span> <b style="color:#F59E0B;">{info.get('average','—')}</b></div>
                        <div><span style="color:#94A3B8;">Worst Case:</span> <b style="color:#EF4444;">{info.get('worst','—')}</b></div>
                        <div><span style="color:#94A3B8;">Aux Space:</span> <b style="color:#3B82F6;">{info.get('space','—')}</b></div>
                    </div>
                </div>
                """)

            # Safety warning
            if algo in QUADRATIC and n > 5000:
                warning_card("Performance Notice",
                              f"{algo} exhibits O(n²) complexity. N={format_number(n)} may require noticeable execution time.")

            save_cfg_btn = st.button("💾 Save & Lock Configuration", use_container_width=True, type="primary")

        if save_cfg_btn:
            st.session_state["ws_config"] = {
                "algo": algo, "dist": dist, "n": n,
                "reps": reps, "seed": seed
            }
            success_card("Configuration Saved",
                          f"Ready to execute: {algo} on {dist} distribution, N={format_number(n)}, {reps} repetition(s).")

        if st.session_state.get("ws_config"):
            cfg = st.session_state["ws_config"]
            st.info(f"✅ Active Configuration: **{cfg['algo']}** | {cfg['dist']} | N = {format_number(cfg['n'])} | {cfg['reps']} runs")

    # ── TAB 2: EXECUTE ────────────────────────────────────────────────────────
    with tab_exec:
        section_header("Execute Experiment", icon="▶️", subtitle="Execute empirical trial with timing, comparison, and memory telemetry.")

        cfg = st.session_state.get("ws_config")
        if not cfg:
            warning_card("No Configuration Active",
                          "Configure your parameters in Tab 1 (Configure) and lock the configuration before execution.")
        else:
            with st.container(border=True):
                render_html(f"""
<div style="padding:4px 6px;">
    <div style="font-size:0.75rem;color:#94A3B8;text-transform:uppercase;font-weight:700;letter-spacing:0.06em;margin-bottom:8px;">READY TO EXECUTE</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;font-size:0.9rem;color:#F1F5F9;">
        <div><span style="color:#94A3B8;font-size:0.75rem;">ALGORITHM</span><br/><b>{cfg["algo"]}</b></div>
        <div><span style="color:#94A3B8;font-size:0.75rem;">DISTRIBUTION</span><br/><b>{cfg["dist"]}</b></div>
        <div><span style="color:#94A3B8;font-size:0.75rem;">INPUT SIZE</span><br/><b>N = {format_number(cfg["n"])}</b></div>
        <div><span style="color:#94A3B8;font-size:0.75rem;">REPETITIONS</span><br/><b>{cfg["reps"]} runs</b></div>
    </div>
</div>
""")

                exec_btn = st.button("⚡ RUN EXPERIMENT TRIAL", use_container_width=True, type="primary")

            if exec_btn:
                arr = generate_dataset(cfg["n"], cfg["dist"], cfg["seed"])
                with st.spinner(f"Executing {cfg['algo']} across {cfg['reps']} runs with N={format_number(cfg['n'])}…"):
                    result = run_benchmark(cfg["algo"], arr, repetitions=cfg["reps"])
                st.session_state["ws_result"] = result
                st.session_state["ws_result_arr"] = arr

            result = st.session_state.get("ws_result")
            if result:
                is_correct = result.get("correct", False)
                status_color = "#22C55E" if is_correct else "#EF4444"
                status_text = "✅ STRICTLY SORTED & VALIDATED" if is_correct else "❌ SORTING VALIDATION FAILED"

                with st.container(border=True):
                    render_html(f"""
<div style="padding:6px 4px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <span style="font-size:0.8rem;color:#94A3B8;text-transform:uppercase;font-weight:700;letter-spacing:0.06em;">EXECUTION TELEMETRY</span>
        <span style="color:{status_color};font-weight:700;font-size:0.82rem;">{status_text}</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;text-align:center;">
        <div style="background:rgba(255,255,255,0.03);padding:10px 4px;border-radius:8px;">
            <div style="color:#94A3B8;font-size:0.72rem;font-weight:700;">AVERAGE TIME</div>
            <div style="color:#06B6D4;font-size:1.4rem;font-weight:800;margin-top:2px;">{format_time(result.get("avg_time",0))}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:10px 4px;border-radius:8px;">
            <div style="color:#94A3B8;font-size:0.72rem;font-weight:700;">COMPARISONS</div>
            <div style="color:#8B5CF6;font-size:1.4rem;font-weight:800;margin-top:2px;">{format_number(result.get("comparisons",0))}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:10px 4px;border-radius:8px;">
            <div style="color:#94A3B8;font-size:0.72rem;font-weight:700;">SWAPS / SHIFTS</div>
            <div style="color:#F59E0B;font-size:1.4rem;font-weight:800;margin-top:2px;">{format_number(result.get("swaps",0))}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:10px 4px;border-radius:8px;">
            <div style="color:#94A3B8;font-size:0.72rem;font-weight:700;">LATENCY STABILITY</div>
            <div style="color:#22C55E;font-size:1.4rem;font-weight:800;margin-top:2px;">±{format_time(result.get("std_dev",0))}</div>
        </div>
    </div>
</div>
""")

    # ── TAB 3: ANALYZE ────────────────────────────────────────────────────────
    with tab_analyze:
        section_header("Analysis & Verification", icon="📊", subtitle="Compare theoretical asymptotic bounds directly against empirical telemetry.")

        result = st.session_state.get("ws_result")
        cfg = st.session_state.get("ws_config")

        if not result or not cfg:
            warning_card("No Execution Data", "Complete the Execute step in Tab 2 to populate empirical results.")
        else:
            algo = cfg["algo"]
            info = ALGORITHM_COMPLEXITY.get(algo, {})

            # 1. Balanced Theoretical vs Empirical cards
            col_th, col_em = st.columns(2, gap="medium")
            with col_th:
                with st.container(border=True):
                    is_stable_str = "Yes" if info.get('stable') else "No"
                    is_inplace_str = "Yes" if info.get('in_place') else "No"
                    render_html(f"""
<div style="padding:4px 2px;">
    <div style="font-size:0.78rem;color:#8B5CF6;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">THEORETICAL ASYMPTOTICS</div>
    <div style="display:flex;flex-direction:column;gap:8px;font-size:0.86rem;color:#F1F5F9;">
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Best Case</span>
            <span style="color:#22C55E;font-weight:700;">{info.get('best','—')}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Average Case</span>
            <span style="color:#F59E0B;font-weight:700;">{info.get('average','—')}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Worst Case</span>
            <span style="color:#EF4444;font-weight:700;">{info.get('worst','—')}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Auxiliary Space</span>
            <span style="color:#3B82F6;font-weight:700;">{info.get('space','—')}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#94A3B8;">Stable / In-Place</span>
            <span style="font-weight:600;">{is_stable_str} / {is_inplace_str}</span>
        </div>
    </div>
</div>
""")

            with col_em:
                with st.container(border=True):
                    res_avg = format_time(result.get('avg_time', 0))
                    res_min = format_time(result.get('min_time', 0))
                    res_max = format_time(result.get('max_time', 0))
                    res_std = format_time(result.get('std_dev', 0))
                    res_comp = format_number(result.get('comparisons', 0))
                    res_n = format_number(cfg.get('n', 0))
                    render_html(f"""
<div style="padding:4px 2px;">
    <div style="font-size:0.78rem;color:#06B6D4;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">EMPIRICAL PERFORMANCE</div>
    <div style="display:flex;flex-direction:column;gap:8px;font-size:0.86rem;color:#F1F5F9;">
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Measured Avg Latency</span>
            <span style="color:#06B6D4;font-weight:700;">{res_avg}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Min / Max Latency</span>
            <span style="font-weight:600;">{res_min} / {res_max}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Total Comparisons</span>
            <span style="color:#8B5CF6;font-weight:700;">{res_comp}</span>
        </div>
        <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:5px;">
            <span style="color:#94A3B8;">Sample Size</span>
            <span style="font-weight:700;">N = {res_n}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#94A3B8;">Run Variance (Std Dev)</span>
            <span style="color:#22C55E;font-weight:600;">±{res_std}</span>
        </div>
    </div>
</div>
""")

            # 2. FULL WIDTH Execution Chart (Historical Scaling for this algorithm)
            st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
            section_header(f"Historical Scaling for {algo}", icon="📈", subtitle="Observed runtime progression across previously stored input sizes.")

            try:
                exps = db.get_experiments(limit=30, algorithm=algo)
                if exps and len(exps) > 1:
                    hist_df = pd.DataFrame([dict(e) for e in exps])
                    if "avg_time" in hist_df.columns and "input_size" in hist_df.columns:
                        hist_grouped = hist_df.groupby("input_size")["avg_time"].mean().reset_index()
                        hist_grouped = hist_grouped.sort_values("input_size")

                        fig_hist = go.Figure(go.Scatter(
                            x=hist_grouped["input_size"],
                            y=hist_grouped["avg_time"] * 1000,
                            mode="lines+markers",
                            marker=dict(color="#06B6D4", size=8),
                            line=dict(color="#06B6D4", width=2.5),
                            name=f"{algo} Empirical Latency"
                        ))
                        layout = get_plotly_layout(f"{algo} — Latency Scaling Curve",
                                                   height=300, x_title="Input Size (N)", y_title="Avg Time (ms)")
                        fig_hist.update_layout(**layout)
                        st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.caption("Execute additional trials at different input sizes to plot asymptotic growth curves.")
            except Exception as e:
                st.caption(f"Historical scaling curve unavailable: {e}")

            # 3. FULL WIDTH Academic Note
            with st.container(border=True):
                render_html("""
<div style="padding:4px 6px;">
    <div style="color:#F59E0B;font-weight:700;margin-bottom:6px;font-size:0.92rem;">📚 Academic Note: Empirical vs Asymptotic Reasoning</div>
    <div style="color:#CBD5E1;font-size:0.85rem;line-height:1.55;">
        Big-O notation describes the limiting asymptotic behavior of an algorithm as input size approaches infinity (N → ∞).
        Empirical measurements capture physical runtimes on real silicon, influenced by CPU caches, memory bus bandwidth,
        compiler optimizations, and OS process scheduling. Validating theoretical algorithmic predictions against empirical trials
        is the core objective of experimental computer science.
    </div>
</div>
""")

    # ── TAB 4: SAVE ───────────────────────────────────────────────────────────
    with tab_save:
        section_header("Save & Document Experiment", icon="💾", subtitle="Store trial telemetry in SQLite history or curate into presentation bookmarks.")

        result = st.session_state.get("ws_result")
        cfg = st.session_state.get("ws_config")

        if not result or not cfg:
            warning_card("Nothing to Save", "Execute an experiment in Tab 2 before archiving results.")
        else:
            with st.container(border=True):
                default_title = f"{cfg['algo']} — {cfg['dist']} (N={format_number(cfg['n'])})"
                title = st.text_input("Experiment Title", value=default_title)
                notes = st.text_area(
                    "Research Observations & Laboratory Notes",
                    placeholder="Document your observations, hardware conditions, and findings here…",
                    height=120
                )
                tags = st.text_input("Tags (comma-separated)", placeholder="sorting, empirical, viva-demo")

                col_h, col_s = st.columns(2, gap="medium")
                with col_h:
                    if st.button("📋 Save to Experiment History", use_container_width=True, type="primary"):
                        try:
                            full_notes = notes
                            if tags:
                                full_notes = "Tags: " + tags + "\n" + notes
                            exp_id = db.insert_experiment({
                                "algorithm": cfg["algo"],
                                "category": ALGORITHM_COMPLEXITY.get(cfg["algo"], {}).get("category", "Sorting"),
                                "dataset": cfg["dist"],
                                "input_size": cfg["n"],
                                "avg_time": result.get("avg_time", 0),
                                "min_time": result.get("min_time", 0),
                                "max_time": result.get("max_time", 0),
                                "comparisons": result.get("comparisons", 0),
                                "swaps": result.get("swaps", 0),
                                "memory_bytes": result.get("memory_estimate", 0),
                                "correct": 1 if result.get("correct") else 0,
                                "repetitions": cfg["reps"],
                                "notes": full_notes
                            })
                            st.session_state["ws_last_exp_id"] = exp_id
                            success_card("Saved to History", f"Experiment #{exp_id} successfully recorded in SQLite.")
                        except Exception as e:
                            st.error(f"Failed to record experiment: {e}")

                with col_s:
                    if st.button("⭐ Save to Curated Bookmarks", use_container_width=True):
                        exp_id = st.session_state.get("ws_last_exp_id")
                        if not exp_id:
                            # Auto-create experiment first if not done
                            try:
                                exp_id = db.insert_experiment({
                                    "algorithm": cfg["algo"],
                                    "category": ALGORITHM_COMPLEXITY.get(cfg["algo"], {}).get("category", "Sorting"),
                                    "dataset": cfg["dist"],
                                    "input_size": cfg["n"],
                                    "avg_time": result.get("avg_time", 0),
                                    "min_time": result.get("min_time", 0),
                                    "max_time": result.get("max_time", 0),
                                    "comparisons": result.get("comparisons", 0),
                                    "swaps": result.get("swaps", 0),
                                    "memory_bytes": result.get("memory_estimate", 0),
                                    "correct": 1 if result.get("correct") else 0,
                                    "repetitions": cfg["reps"],
                                    "notes": notes
                                })
                                st.session_state["ws_last_exp_id"] = exp_id
                            except Exception:
                                pass

                        if exp_id:
                            try:
                                db.save_experiment(exp_id, title, notes)
                                success_card("Curated Bookmark Saved", f"'{title}' bookmarked in Saved Experiments.")
                            except Exception as e:
                                st.error(f"Bookmark save failed: {e}")
                        else:
                            st.warning("Please save to history first.")
