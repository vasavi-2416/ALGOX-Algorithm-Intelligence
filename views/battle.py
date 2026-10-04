"""
ALGOX — Algorithm Battle Arena Module
Head-to-head empirical algorithm performance confrontation under identical experimental conditions.
Restructured into 3 connected workspace tiers: Configuration -> Results -> Analysis.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.dataset import generate_dataset
from core.benchmark import benchmark_multiple
from core.complexity import ALGORITHM_COMPLEXITY
from core.ui import (render_html, section_header, success_card, warning_card,
                     danger_card, get_plotly_layout, format_time, format_number,
                     render_footer, COLOR_PURPLE, COLOR_BLUE, COLOR_CYAN,
                     COLOR_GREEN, COLOR_AMBER, COLOR_RED, COLOR_TEXT_MUTED)
from database.database import AlgoxDB

BATTLE_ALGORITHMS = [
    "Bubble Sort", "Selection Sort", "Insertion Sort",
    "Merge Sort", "Quick Sort", "Heap Sort"
]

QUADRATIC = {"Bubble Sort", "Selection Sort", "Insertion Sort"}


def render_battle(db: AlgoxDB):
    # Hero Banner
    render_html("""
    <div class="algox-hero-card" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <span class="algox-badge algox-badge-purple" style="margin-bottom: 6px; box-shadow: 0 0 10px rgba(168,85,247,0.3);">⚡ BATTLE ARENA</span>
                <h1 style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; margin: 4px 0 0 0;">
                    Algorithm Battle Arena
                </h1>
                <div style="font-size: 0.88rem; color: #CBD5E1; margin-top: 4px;">
                    Empirical head-to-head algorithm confrontation under strictly identical experimental conditions.
                </div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="algox-badge algox-badge-cyan">Synchronous Execution</span>
                <span class="algox-badge algox-badge-green">SQLite Auto-Persist</span>
            </div>
        </div>
    </div>
    """)

    # Populate default results on initial visit to ensure the arena is never an empty void
    if "battle_results" not in st.session_state:
        init_algos = ["Merge Sort", "Quick Sort", "Heap Sort"]
        init_arr = generate_dataset(500, "Random", 42)
        init_res = benchmark_multiple(init_algos, init_arr, repetitions=3)
        if init_res:
            st.session_state["battle_results"] = sorted(init_res, key=lambda x: x.get("avg_time", float("inf")))
            st.session_state["battle_config"] = {
                "dist": "Random", "n": 500, "reps": 3, "seed": 42,
                "algos": init_algos
            }

    # =========================================================================
    # TIER 1: BATTLE CONFIGURATION (Balanced Full-Width Panel)
    # =========================================================================
    section_header("Battle Configuration", icon="⚙️", subtitle="Select candidate contenders and experimental input parameters.")
    
    with st.container(border=True):
        selected_algos = st.multiselect(
            "Select Contender Algorithms",
            options=BATTLE_ALGORITHMS,
            default=st.session_state.get("battle_config", {}).get("algos", ["Merge Sort", "Quick Sort", "Heap Sort"]),
            help="Choose at least 2 algorithms to compete head-to-head.",
            key="battle_algo_multi"
        )

        col_d, col_n, col_r = st.columns([1.2, 1.2, 1.6], gap="medium")
        with col_d:
            cur_dist = st.session_state.get("battle_config", {}).get("dist", "Random")
            dist_options = ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicate Heavy"]
            dist_idx = dist_options.index(cur_dist) if cur_dist in dist_options else 0
            dist = st.selectbox(
                "Dataset Distribution",
                dist_options,
                index=dist_idx,
                key="battle_dist_select"
            )

        with col_n:
            cur_n = st.session_state.get("battle_config", {}).get("n", 500)
            n = st.slider("Input Size (N)", min_value=50, max_value=10000, value=cur_n, step=50, key="battle_n_slider")

        with col_r:
            c_reps, c_seed = st.columns(2, gap="small")
            with c_reps:
                cur_reps = st.session_state.get("battle_config", {}).get("reps", 3)
                reps = st.slider("Repetitions", min_value=1, max_value=10, value=cur_reps, key="battle_reps_slider")
            with c_seed:
                cur_seed = st.session_state.get("battle_config", {}).get("seed", 42)
                seed_val = st.number_input("Random Seed", min_value=0, max_value=99999, value=cur_seed if cur_seed else 0, key="battle_seed_input")
                seed = int(seed_val) if seed_val > 0 else None

        # Safety check for quadratic algorithms at large N
        has_quadratic = any(a in QUADRATIC for a in selected_algos)
        safe_to_run = True

        if has_quadratic and n > 10000:
            danger_card("Blocked Execution", "Quadratic algorithms are blocked at N > 10,000 to prevent interface latency.")
            safe_to_run = False
        elif has_quadratic and n > 5000:
            warning_card("Complexity Notice", f"Quadratic sorts at N={n:,} may take several seconds.")

        if len(selected_algos) < 2:
            st.caption("⚠️ Select at least 2 algorithms to begin.")

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        run_btn = st.button("⚡ START BATTLE", use_container_width=True, type="primary",
                            disabled=(len(selected_algos) < 2 or not safe_to_run), key="battle_run_btn")

    if run_btn and len(selected_algos) >= 2 and safe_to_run:
        arr = generate_dataset(n, dist, seed)
        with st.spinner(f"Executing head-to-head confrontation (N={format_number(n)}, {dist})…"):
            results = benchmark_multiple(selected_algos, arr, repetitions=reps)

        if results:
            results_sorted = sorted(results, key=lambda x: x.get("avg_time", float("inf")))
            st.session_state["battle_results"] = results_sorted
            st.session_state["battle_config"] = {
                "dist": dist, "n": n, "reps": reps, "seed": seed,
                "algos": selected_algos
            }

            # Auto-save each contender to SQLite
            for r in results_sorted:
                try:
                    db.insert_experiment({
                        "algorithm": r["algorithm"],
                        "category": "Sorting",
                        "dataset": dist,
                        "input_size": n,
                        "avg_time": r.get("avg_time", 0),
                        "min_time": r.get("min_time", 0),
                        "max_time": r.get("max_time", 0),
                        "std_dev": r.get("std_dev", 0.0),
                        "seed": seed,
                        "comparisons": r.get("comparisons", 0),
                        "swaps": r.get("swaps", 0),
                        "memory_bytes": r.get("memory_estimate", 0),
                        "correct": 1 if r.get("correct") else 0,
                        "repetitions": reps,
                        "notes": f"Battle Arena — {dist} N={n}"
                    })
                except Exception:
                    pass
            st.rerun()

    # =========================================================================
    # TIER 2: BATTLE RESULTS & LEADERBOARD (Full Width with Side-by-Side Charts)
    # =========================================================================
    results_sorted = st.session_state.get("battle_results")
    cfg = st.session_state.get("battle_config", {})

    if results_sorted:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        section_header("Battle Leaderboard & Results", icon="🏆",
                       subtitle=f"Empirically verified ranking for {cfg.get('dist')} (N={format_number(cfg.get('n',0))}, {cfg.get('reps', 3)} runs).")
        
        # Winner Banner (Full width)
        winner_name = results_sorted[0]["algorithm"]
        winner_time = format_time(results_sorted[0].get("avg_time", 0))
        render_html(f"""
        <div class="algox-glass-card" style="border: 1px solid rgba(34,197,94,0.45); box-shadow: 0 0 25px rgba(34,197,94,0.20); margin-bottom: 20px; padding: 20px 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 0.74rem; font-weight: 700; color: #86EFAC; text-transform: uppercase; letter-spacing: 0.08em;">🥇 LOWEST MEASURED EXECUTION TIME</div>
                    <div style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; margin-top: 2px;">{winner_name}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">LOWEST AVERAGE EXECUTION TIME (THIS EXPERIMENT)</div>
                    <div style="font-size: 1.55rem; font-weight: 800; color: #4ADE80;">{winner_time}</div>
                </div>
            </div>
        </div>
        """)

        # Leaderboard Table
        medals = ["🥇", "🥈", "🥉"] + ["  " for _ in range(10)]
        rows = []
        for i, r in enumerate(results_sorted):
            std_dev_val = r.get("std_dev", 0) or 0
            rows.append({
                "Rank": f"{medals[i]} #{i+1}",
                "Algorithm": r["algorithm"],
                "Avg Time": format_time(r.get("avg_time", 0)),
                "Std Dev": f"±{std_dev_val*1000:.3f} ms" if std_dev_val > 0 else "—",
                "Comparisons": format_number(r.get("comparisons", 0)),
                "Swaps / Shifts": format_number(r.get("swaps", 0)),
                "Correctness": "✅ Validated" if r.get("correct") else "❌ FAILED"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        # Charts: Side by Side in 2 Columns inside Glass Panels
        c_chart1, c_chart2 = st.columns(2, gap="medium")

        algos = [r["algorithm"] for r in results_sorted]
        avg_times = [r.get("avg_time", 0) * 1000 for r in results_sorted]
        colors = ["#22C55E" if i == 0 else "#F59E0B" if i == 1 else "#EF4444" if i == len(results_sorted)-1 else "#3B82F6"
                  for i in range(len(results_sorted))]

        with c_chart1:
            with st.container(border=True):
                render_html("""
                <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                    EXECUTION LATENCY (MS)
                </div>
                """)
                fig_time = go.Figure(go.Bar(
                    x=algos, y=avg_times,
                    marker_color=colors,
                    text=[format_time(r.get("avg_time", 0)) for r in results_sorted],
                    textposition="outside"
                ))
                layout = get_plotly_layout("", height=280, x_title="Contender", y_title="Latency (ms)")
                layout["margin"] = dict(l=10, r=10, t=20, b=10)
                fig_time.update_layout(**layout)
                st.plotly_chart(fig_time, use_container_width=True)

        with c_chart2:
            with st.container(border=True):
                render_html("""
                <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                    OPERATIONS COUNT (COMPARISONS & SWAPS)
                </div>
                """)
                comps = [r.get("comparisons", 0) for r in results_sorted]
                swaps = [r.get("swaps", 0) for r in results_sorted]

                fig_ops = go.Figure()
                fig_ops.add_trace(go.Bar(name="Comparisons", x=algos, y=comps, marker_color="#3B82F6"))
                fig_ops.add_trace(go.Bar(name="Swaps / Shifts", x=algos, y=swaps, marker_color="#8B5CF6"))
                ops_layout = get_plotly_layout("", height=280, x_title="Contender", y_title="Count")
                ops_layout["margin"] = dict(l=10, r=10, t=20, b=10)
                ops_layout["barmode"] = "group"
                fig_ops.update_layout(**ops_layout)
                st.plotly_chart(fig_ops, use_container_width=True)

        # =========================================================================
        # TIER 3: EMPIRICAL ANALYSIS & ARCHIVING
        # =========================================================================
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        section_header("Empirical Analysis & Archive", icon="🔬",
                       subtitle="Computational performance findings and curated experiment persistence.")
        
        loser_name = results_sorted[-1]["algorithm"]
        ratio = (results_sorted[-1].get("avg_time", 1) / max(results_sorted[0].get("avg_time", 1e-9), 1e-9))
        
        with st.container(border=True):
            render_html(f"""
            <div style="padding: 4px 6px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #86EFAC; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">⚡ COMPUTATIONAL ADVANTAGE</div>
                <div style="color: #F1F5F9; font-size: 1.05rem; line-height: 1.5;">
                    <b>{winner_name}</b> recorded the <b style="color: #4ADE80;">lowest average execution time</b> ({ratio:.1f}× faster than {loser_name}) on <b>{cfg.get("dist")}</b> data at N={format_number(cfg.get("n",0))}.<br><span style="font-size:0.78rem;color:#94A3B8;">⚠️ Results are specific to this experiment configuration. Theoretical complexity determines asymptotic behaviour at scale.</span>
                </div>
            </div>
            """)

            st.markdown("<div style='border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0;'></div>", unsafe_allow_html=True)

            with st.expander("💾 Save Battle Result to Curated Experiments"):
                _btitle = f"Battle: {' vs '.join(algos[:3])} (N={cfg.get('n',0)})"
                title = st.text_input("Battle Title", value=_btitle, key="battle_save_title")
                notes = st.text_area("Observations", value=f"Distribution: {cfg.get('dist')}, Winner: {winner_name}", key="battle_save_notes")
                if st.button("Save to Saved Experiments", use_container_width=True, type="primary", key="battle_save_commit"):
                    try:
                        exp_id = db.insert_experiment({
                            "algorithm": winner_name,
                            "category": "Sorting",
                            "dataset": cfg.get("dist", ""),
                            "input_size": cfg.get("n", 0),
                            "avg_time": results_sorted[0].get("avg_time", 0),
                            "min_time": results_sorted[0].get("min_time", 0),
                            "max_time": results_sorted[0].get("max_time", 0),
                            "comparisons": results_sorted[0].get("comparisons", 0),
                            "swaps": results_sorted[0].get("swaps", 0),
                            "memory_bytes": results_sorted[0].get("memory_estimate", 0),
                            "correct": 1,
                            "repetitions": cfg.get("reps", 3),
                            "notes": notes
                        })
                        db.save_experiment(exp_id, title, notes)
                        success_card("Saved Successfully", f"Battle result '{title}' saved to Curated Collection.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")

    render_footer()
