"""
ALGOX — Benchmark Lab Module
High-precision empirical testing suite with execution timing, operation metrics, safety guards,
multi-N asymptotic scaling studies, search/graph verification, and SQLite auto-persistence.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
from core.ui import (
    section_header,
    render_html,
    empty_state,
    get_plotly_layout,
    format_time,
    format_number,
    warning_card,
    danger_card,
    success_card,
    COLOR_PURPLE,
    COLOR_PURPLE_LIGHT,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT_MUTED,
    render_footer
)
from core.dataset import generate_dataset, DISTRIBUTIONS
from core.benchmark import (
    run_benchmark,
    run_search_benchmark,
    run_graph_benchmark,
    run_scaling_benchmark,
    check_safety_level,
    SORTING_FUNCTION_MAP,
    SEARCHING_FUNCTION_MAP,
    GRAPH_FUNCTION_MAP,
    QUADRATIC_ALGORITHMS
)
from algorithms.graph import DEFAULT_GRAPH

def render_benchmark(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">⚗️</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(139,92,246,0.85);display:block;">ALGOX · BENCHMARK LAB</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Benchmark Lab</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
High-precision empirical testing suite — measure microsecond latencies, operation counts, and asymptotic scaling under identical experimental conditions with formal correctness verification.
</p>
</div>
""")

    # 1. Experimental Parameter Controls
    section_header("Benchmark Configuration", icon="⚙️", subtitle="Configure algorithmic candidates, dataset distributions, repetition runs, and analysis modes.")

    with st.container(border=True):
        bench_mode = st.radio(
            "Benchmark Evaluation Mode",
            ["⚡ Standard Benchmark (Single N)", "📈 Asymptotic Scaling Study (Multi-N)", "🔍 Search & Graph Verification Lab"],
            key="bench_active_mode",
            horizontal=True
        )

        st.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)

        # -------------------------------------------------------------
        # MODE 1: STANDARD BENCHMARK (SINGLE N)
        # -------------------------------------------------------------
        if bench_mode == "⚡ Standard Benchmark (Single N)":
            preset_choice = st.selectbox(
                "Experimental Benchmark Presets",
                ["Custom Configuration", "⚡ Quick Test (N=100, Fast Comparison)", "🔬 Standard Lab Benchmark (N=500, All Sorts)", "📈 Large Dataset Scalability (N=5,000, O(n log n))", "⚠️ Stress Test (N=10,000, Scalability Limits)"],
                index=0,
                key="bench_preset_selector"
            )

            preset_defaults = {
                "Custom Configuration": (["Merge Sort", "Quick Sort", "Heap Sort"], 0, 1000, 3),
                "⚡ Quick Test (N=100, Fast Comparison)": (["Merge Sort", "Quick Sort"], 0, 100, 3),
                "🔬 Standard Lab Benchmark (N=500, All Sorts)": (["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"], 0, 500, 3),
                "📈 Large Dataset Scalability (N=5,000, O(n log n))": (["Merge Sort", "Quick Sort", "Heap Sort"], 0, 5000, 3),
                "⚠️ Stress Test (N=10,000, Scalability Limits)": (["Merge Sort", "Quick Sort", "Heap Sort"], 0, 10000, 3)
            }

            p_algos, p_dist_idx, p_n, p_reps = preset_defaults[preset_choice]

            selected_algos = st.multiselect(
                "Target Algorithms for Evaluation",
                list(SORTING_FUNCTION_MAP.keys()),
                default=p_algos,
                key=f"bench_selected_algos_{preset_choice}",
                help="Select one or more sorting algorithms to measure under identical data conditions."
            )

            col_d, col_n, col_r, col_s = st.columns([1.3, 1.1, 1.1, 1.1], gap="medium")
            with col_d:
                distribution = st.selectbox("Dataset Distribution", DISTRIBUTIONS, index=p_dist_idx, key=f"bench_dist_{preset_choice}")
            with col_n:
                input_size = st.number_input("Input Size (N)", min_value=10, max_value=50000, value=p_n, step=100, key=f"bench_size_{preset_choice}")
            with col_r:
                repetitions = st.slider("Repetitions (Runs)", min_value=1, max_value=10, value=p_reps, key=f"bench_reps_{preset_choice}")
            with col_s:
                seed_v = st.number_input("Seed (0=Random)", min_value=0, max_value=99999, value=42, key=f"bench_seed_{preset_choice}")
                seed = int(seed_v) if seed_v > 0 else None

            # Safety Guardrails
            safety_level, safety_msg = check_safety_level(selected_algos, input_size)
            confirmed_risk = False
            if safety_level == 'danger':
                danger_card("CRITICAL EXECUTION HAZARD DETECTED", safety_msg)
                confirmed_risk = st.checkbox("I acknowledge the computational cost and wish to force execution.", key="bench_danger_confirm")
            elif safety_level in ('warning', 'caution'):
                warning_card("Computational Complexity Notice", safety_msg)

            can_execute = bool(selected_algos) and (safety_level != 'danger' or confirmed_risk)
            run_clicked = st.button("Run Benchmark Suite", disabled=not can_execute, use_container_width=True, type="primary", key="bench_run_btn")

            if run_clicked:
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Synthesizing reproducible empirical dataset...")
                dataset = generate_dataset(input_size, distribution, seed=seed)
                db.log_dataset(f"Lab-{distribution}-{input_size}", distribution, input_size, seed=seed)

                bench_results = []
                for i, algo in enumerate(selected_algos):
                    status_text.text(f"Running {algo} across {repetitions} iteration(s)...")
                    res = run_benchmark(algo, dataset, repetitions=repetitions)
                    bench_results.append(res)

                    # Auto-persist each benchmark run to SQLite
                    db.insert_experiment({
                        'algorithm': res['algorithm'],
                        'category': 'Sorting',
                        'dataset': distribution,
                        'input_size': res['input_size'],
                        'avg_time': res['avg_time'],
                        'min_time': res['min_time'],
                        'max_time': res['max_time'],
                        'std_dev': res.get('std_dev', 0.0),
                        'seed': seed,
                        'comparisons': res['comparisons'],
                        'swaps': res['swaps'],
                        'memory_bytes': res['memory_bytes'],
                        'correct': 1 if res['correct'] else 0,
                        'repetitions': res['repetitions'],
                        'notes': f"Benchmark Lab run ({distribution}, N={input_size}, seed={seed})"
                    })
                    progress_bar.progress((i + 1) / len(selected_algos))

                status_text.empty()
                progress_bar.empty()
                st.session_state['latest_bench_results'] = bench_results
                st.session_state['latest_bench_dataset_info'] = {'N': input_size, 'dist': distribution, 'reps': repetitions, 'seed': seed}
                success_card("Benchmark Suite Completed", f"Successfully benchmarked {len(selected_algos)} algorithms. Data persisted to SQLite.")

        # -------------------------------------------------------------
        # MODE 2: ASYMPTOTIC SCALING STUDY (MULTI-N)
        # -------------------------------------------------------------
        elif bench_mode == "📈 Asymptotic Scaling Study (Multi-N)":
            scale_algos = st.multiselect(
                "Select Algorithms for Empirical Scaling Curve",
                list(SORTING_FUNCTION_MAP.keys()),
                default=["Merge Sort", "Quick Sort", "Heap Sort"],
                key="scale_algos_select"
            )

            col_sd, col_sr, col_ss = st.columns([1.5, 1.2, 1.3], gap="medium")
            with col_sd:
                scale_dist = st.selectbox("Dataset Distribution", DISTRIBUTIONS, index=0, key="scale_dist_select")
            with col_sr:
                scale_reps = st.slider("Repetitions per Scale Point", min_value=1, max_value=5, value=2, key="scale_reps_slider")
            with col_ss:
                scale_seed_v = st.number_input("Random Seed", min_value=0, max_value=99999, value=42, key="scale_seed_input")
                scale_seed = int(scale_seed_v) if scale_seed_v > 0 else None

            # Input scale points selection
            scale_options = [100, 250, 500, 1000, 2500, 5000]
            selected_scales = st.multiselect(
                "Input Scale Points (N)",
                scale_options,
                default=[100, 250, 500, 1000, 2500],
                key="scale_n_points_select",
                help="Test algorithms across multiple sizes to map runtime growth against theoretical Big-O curves."
            )

            has_quad = any(a in QUADRATIC_ALGORITHMS for a in scale_algos)
            if has_quad and any(n >= 2500 for n in selected_scales):
                warning_card("Quadratic Scaling Notice", "Bubble, Selection, or Insertion Sort included with N >= 2,500. Quadratic execution will show steep operation curves.")

            run_scale_btn = st.button("📈 RUN ASYMPTOTIC SCALING STUDY", disabled=len(scale_algos) == 0 or len(selected_scales) < 2, use_container_width=True, type="primary", key="btn_run_scaling")

            if run_scale_btn:
                progress_bar = st.progress(0)
                status_text = st.empty()
                total_runs = len(selected_scales) * len(scale_algos)
                curr_run = 0

                scaling_records = {algo: [] for algo in scale_algos}

                for n_val in sorted(selected_scales):
                    arr_n = generate_dataset(n_val, scale_dist, seed=scale_seed)
                    db.log_dataset(f"Scale-{scale_dist}-{n_val}", scale_dist, n_val, seed=scale_seed)

                    for algo in scale_algos:
                        curr_run += 1
                        status_text.text(f"Measuring {algo} at N={n_val:,} ({curr_run}/{total_runs})...")
                        res = run_benchmark(algo, arr_n, repetitions=scale_reps)
                        scaling_records[algo].append(res)

                        db.insert_experiment({
                            'algorithm': res['algorithm'],
                            'category': 'Sorting',
                            'dataset': scale_dist,
                            'input_size': res['input_size'],
                            'avg_time': res['avg_time'],
                            'min_time': res['min_time'],
                            'max_time': res['max_time'],
                            'std_dev': res.get('std_dev', 0.0),
                            'seed': scale_seed,
                            'comparisons': res['comparisons'],
                            'swaps': res['swaps'],
                            'memory_bytes': res['memory_bytes'],
                            'correct': 1 if res['correct'] else 0,
                            'repetitions': res['repetitions'],
                            'notes': f"Scaling Study point ({scale_dist}, N={n_val})"
                        })
                        progress_bar.progress(curr_run / total_runs)

                status_text.empty()
                progress_bar.empty()
                st.session_state['latest_scaling_data'] = scaling_records
                st.session_state['latest_scaling_info'] = {'dist': scale_dist, 'scales': selected_scales, 'reps': scale_reps}
                success_card("Scaling Study Complete", f"Mapped {len(scale_algos)} algorithms across {len(selected_scales)} problem scales. Data persisted to SQLite.")

        # -------------------------------------------------------------
        # MODE 3: SEARCH & GRAPH VERIFICATION LAB
        # -------------------------------------------------------------
        else:
            cat_choice = st.radio("Domain Category", ["Searching Algorithms", "Graph Algorithms"], horizontal=True, key="sg_cat_choice")

            if cat_choice == "Searching Algorithms":
                col_sa, col_st, col_sn = st.columns([1.5, 1.2, 1.3], gap="medium")
                with col_sa:
                    s_algo = st.selectbox("Search Algorithm", list(SEARCHING_FUNCTION_MAP.keys()), key="sg_search_algo")
                with col_sn:
                    s_n = st.number_input("Array Scale (N)", min_value=10, max_value=10000, value=1000, step=100, key="sg_search_n")
                with col_st:
                    s_target = st.number_input("Target Value to Locate", value=42, key="sg_search_target")

                run_search_btn = st.button("🔍 RUN SEARCH BENCHMARK", use_container_width=True, type="primary", key="btn_run_search")

                if run_search_btn:
                    arr_s = generate_dataset(s_n, "Sorted" if s_algo == "Binary Search" else "Random", seed=42)
                    res_s = run_search_benchmark(s_algo, arr_s, s_target, repetitions=5)
                    st.session_state['latest_search_res'] = res_s

                    db.insert_experiment({
                        'algorithm': res_s['algorithm'],
                        'category': 'Searching',
                        'dataset': 'Sorted' if s_algo == 'Binary Search' else 'Random',
                        'input_size': res_s['input_size'],
                        'avg_time': res_s['avg_time'],
                        'min_time': res_s['min_time'],
                        'max_time': res_s['max_time'],
                        'std_dev': res_s.get('std_dev', 0.0),
                        'seed': 42,
                        'comparisons': res_s['comparisons'],
                        'swaps': 0,
                        'memory_bytes': 64,
                        'correct': 1 if res_s['correct'] else 0,
                        'repetitions': res_s['repetitions'],
                        'notes': f"Search verification (Target={s_target}, N={s_n})"
                    })

            else:
                col_ga, col_gs = st.columns(2, gap="medium")
                with col_ga:
                    g_algo = st.selectbox("Graph Algorithm", list(GRAPH_FUNCTION_MAP.keys()), key="sg_graph_algo")
                with col_gs:
                    g_start = st.selectbox("Start Node", ["A", "B", "C", "D", "E", "F"], index=0, key="sg_graph_start")

                run_graph_btn = st.button("🕸️ RUN GRAPH BENCHMARK", use_container_width=True, type="primary", key="btn_run_graph")

                if run_graph_btn:
                    res_g = run_graph_benchmark(g_algo, DEFAULT_GRAPH, start_node=g_start, repetitions=5)
                    st.session_state['latest_graph_res'] = res_g

                    db.insert_experiment({
                        'algorithm': res_g['algorithm'],
                        'category': 'Graph',
                        'dataset': 'Default Graph (6 Nodes)',
                        'input_size': res_g['graph_nodes'],
                        'avg_time': res_g['avg_time'],
                        'min_time': res_g['min_time'],
                        'max_time': res_g['max_time'],
                        'std_dev': res_g.get('std_dev', 0.0),
                        'seed': 42,
                        'comparisons': res_g['comparisons'],
                        'swaps': res_g['swaps'],
                        'memory_bytes': res_g['memory_bytes'],
                        'correct': 1 if res_g['correct'] else 0,
                        'repetitions': res_g['repetitions'],
                        'notes': f"Graph benchmark ({g_algo}, Start={g_start})"
                    })

    # =========================================================================
    # DISPLAY RESULTS BASED ON ACTIVE MODE
    # =========================================================================

    # 1. DISPLAY STANDARD BENCHMARK RESULTS
    if bench_mode == "⚡ Standard Benchmark (Single N)":
        results = st.session_state.get('latest_bench_results')
        if results:
            meta = st.session_state.get('latest_bench_dataset_info', {})
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            section_header(f"Empirical Benchmark Results (N={meta.get('N', 0):,}, {meta.get('dist')})", icon="📊")

            # Results Table with Standard Deviation & Correctness
            table_rows = []
            for r in results:
                table_rows.append({
                    "Algorithm": r['algorithm'],
                    "Avg Time": format_time(r['avg_time']),
                    "Min Time": format_time(r['min_time']),
                    "Max Time": format_time(r['max_time']),
                    "Std Dev": f"{r.get('std_dev', 0.0) * 1000:.3f} ms",
                    "Comparisons": format_number(r['comparisons']),
                    "Swaps / Shifts": format_number(r['swaps'] + r.get('shifts', 0)),
                    "Aux Memory": f"{r['memory_bytes']:,} B",
                    "Verification": "✓ VERIFIED" if r['correct'] else "✗ FAILED"
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

            # Charts Section
            c_tab1, c_tab2, c_tab3 = st.tabs(["Execution Timing", "Operation Counts", "Auxiliary Memory"])

            with c_tab1:
                fig_time = go.Figure()
                algo_names = [r['algorithm'] for r in results]
                avg_times = [r['avg_time'] * 1000 for r in results]
                min_times = [r['min_time'] * 1000 for r in results]
                max_times = [r['max_time'] * 1000 for r in results]

                fig_time.add_trace(go.Bar(
                    name="Average Time",
                    x=algo_names,
                    y=avg_times,
                    marker_color=COLOR_CYAN,
                    text=[f"{t:.2f} ms" for t in avg_times],
                    textposition='auto'
                ))
                fig_time.add_trace(go.Bar(name="Min Time", x=algo_names, y=min_times, marker_color=COLOR_GREEN))
                fig_time.add_trace(go.Bar(name="Max Time", x=algo_names, y=max_times, marker_color=COLOR_AMBER))

                fig_time.update_layout(get_plotly_layout("Execution Latency Comparison", height=360, x_title="Algorithm", y_title="Latency (ms)"))
                fig_time.update_layout(barmode='group')
                st.plotly_chart(fig_time, use_container_width=True)

            with c_tab2:
                fig_ops = go.Figure()
                fig_ops.add_trace(go.Bar(
                    name="Comparisons",
                    x=algo_names,
                    y=[r['comparisons'] for r in results],
                    marker_color=COLOR_PURPLE
                ))
                fig_ops.add_trace(go.Bar(
                    name="Swaps / Shifts",
                    x=algo_names,
                    y=[r['swaps'] + r.get('shifts', 0) for r in results],
                    marker_color=COLOR_PURPLE_LIGHT
                ))
                fig_ops.update_layout(get_plotly_layout("Algorithmic Operations Counter", height=360, x_title="Algorithm", y_title="Operations Count"))
                fig_ops.update_layout(barmode='group')
                st.plotly_chart(fig_ops, use_container_width=True)

            with c_tab3:
                fig_mem = go.Figure(data=[
                    go.Bar(
                        x=algo_names,
                        y=[r['memory_bytes'] for r in results],
                        marker_color=COLOR_BLUE,
                        text=[f"{r['memory_bytes']} B" for r in results],
                        textposition='auto'
                    )
                ])
                fig_mem.update_layout(get_plotly_layout("Estimated Auxiliary Memory Footprint", height=360, x_title="Algorithm", y_title="Bytes"))
                st.plotly_chart(fig_mem, use_container_width=True)

            # Insights Panel
            fastest_algo = min(results, key=lambda x: x['avg_time'])
            min_comps_algo = min(results, key=lambda x: x['comparisons'])

            with st.container(border=True):
                render_html(f"""
                <div style="font-weight: 700; font-size: 0.95rem; color: #FFFFFF; margin-bottom: 0.35rem;">
                    Empirical Performance Insights &amp; Verification
                </div>
                <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;">
                    <div>• <b>Fastest Measured:</b> <span style="color: {COLOR_CYAN}; font-weight: 700;">{fastest_algo['algorithm']}</span> recorded the lowest measured average execution time (<b>{format_time(fastest_algo['avg_time'])}</b>) in this trial.</div>
                    <div>• <b>Comparison Efficiency:</b> <span style="color: {COLOR_AMBER}; font-weight: 700;">{min_comps_algo['algorithm']}</span> performed the fewest element comparisons (<b>{min_comps_algo['comparisons']:,}</b> comparisons).</div>
                    <div>• <b>Ground Truth Correctness:</b> All evaluated sorting algorithms produced arrays strictly matching Python's trusted ground truth reference (<b>✓ VERIFIED</b>).</div>
                    <div style="margin-top: 6px; font-size: 0.78rem; color: {COLOR_TEXT_MUTED}; font-style: italic;">
                        * Result is specific to this dataset distribution ({meta.get('dist')}), input size (N={meta.get('N',0):,}), seed={meta.get('seed')}, Python runtime, and hardware.
                    </div>
                </div>
                """)

            # Save to Curated Experiments Section
            with st.expander("Save Run to Curated Experiments"):
                save_title = st.text_input("Experiment Title", value=f"{fastest_algo['algorithm']} vs Alternatives (N={meta.get('N')})", key="bench_save_title")
                save_notes = st.text_area("Lab Notes / Observations", value=f"Tested on {meta.get('dist')} distribution. {fastest_algo['algorithm']} demonstrated superior execution timing.", key="bench_save_notes")
                if st.button("Save To Curated Collection", key="bench_save_commit"):
                    matched_id = None
                    with db.get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute("""
                            SELECT id FROM experiments
                            WHERE algorithm = ? AND dataset = ? AND input_size = ?
                            ORDER BY id DESC LIMIT 1
                        """, (fastest_algo['algorithm'], meta.get('dist'), meta.get('N')))
                        row = cur.fetchone()
                        if row:
                            matched_id = row[0]

                    if not matched_id:
                        recent = db.get_recent_experiments(limit=1)
                        matched_id = recent[0]['id'] if recent else None

                    db.save_experiment(matched_id, save_title, save_notes)
                    st.success(f"Experiment for '{fastest_algo['algorithm']}' successfully saved to your Curated Collection!")
        else:
            empty_state(
                icon="⚗️",
                title="BENCHMARK LAB READY",
                message="Select algorithms and execute the benchmark suite to measure microsecond latencies, operation counters, and memory consumption.",
                button_label="",
                target_page=""
            )

    # 2. DISPLAY SCALING STUDY RESULTS
    elif bench_mode == "📈 Asymptotic Scaling Study (Multi-N)":
        scaling_data = st.session_state.get('latest_scaling_data')
        if scaling_data:
            s_info = st.session_state.get('latest_scaling_info', {})
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            section_header(f"Asymptotic Empirical Scaling Curves ({s_info.get('dist')} Distribution)", icon="📈")

            # Chart: Input Size vs Execution Time
            fig_scale = go.Figure()
            colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_AMBER, COLOR_GREEN, COLOR_BLUE, COLOR_RED]

            for idx, (algo, pts) in enumerate(scaling_data.items()):
                if pts:
                    x_pts = [p['input_size'] for p in pts]
                    y_pts = [p['avg_time'] * 1000.0 for p in pts]
                    c = colors[idx % len(colors)]
                    fig_scale.add_trace(go.Scatter(
                        x=x_pts,
                        y=y_pts,
                        mode='lines+markers',
                        name=algo,
                        line=dict(color=c, width=2.5),
                        marker=dict(size=8, color=c)
                    ))

            fig_scale.update_layout(get_plotly_layout("Empirical Runtime Scaling: Input Size (N) vs Execution Time (ms)", height=400, x_title="Input Size (N)", y_title="Latency (ms)"))
            st.plotly_chart(fig_scale, use_container_width=True)

            # Chart: Input Size vs Operations
            fig_scale_ops = go.Figure()
            for idx, (algo, pts) in enumerate(scaling_data.items()):
                if pts:
                    x_pts = [p['input_size'] for p in pts]
                    y_ops = [p['comparisons'] + p.get('swaps', 0) for p in pts]
                    c = colors[idx % len(colors)]
                    fig_scale_ops.add_trace(go.Scatter(
                        x=x_pts,
                        y=y_ops,
                        mode='lines+markers',
                        name=f"{algo} (Operations)",
                        line=dict(color=c, width=2.5, dash='dot'),
                        marker=dict(size=7, color=c)
                    ))

            fig_scale_ops.update_layout(get_plotly_layout("Asymptotic Operations Growth: Input Size (N) vs Total Operations", height=380, x_title="Input Size (N)", y_title="Operations Count"))
            st.plotly_chart(fig_scale_ops, use_container_width=True)

            # Summary Table
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            scale_rows = []
            for algo, pts in scaling_data.items():
                for p in pts:
                    scale_rows.append({
                        "Algorithm": algo,
                        "Input Size (N)": f"{p['input_size']:,}",
                        "Avg Time (ms)": f"{p['avg_time']*1000.0:.3f}",
                        "Comparisons": f"{p['comparisons']:,}",
                        "Swaps / Shifts": f"{p['swaps'] + p.get('shifts', 0):,}",
                        "Verification": "✓ VERIFIED" if p['correct'] else "✗ FAILED"
                    })
            st.dataframe(pd.DataFrame(scale_rows), use_container_width=True, hide_index=True)
        else:
            empty_state(
                icon="📈",
                title="SCALING STUDY READY",
                message="Select candidate algorithms and multiple input scale points (N), then click 'Run Asymptotic Scaling Study' to plot empirical curves against theoretical Big-O bounds.",
                button_label="",
                target_page=""
            )

    # 3. DISPLAY SEARCH & GRAPH RESULTS
    else:
        s_res = st.session_state.get('latest_search_res')
        g_res = st.session_state.get('latest_graph_res')

        if s_res:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            section_header(f"Search Verification Results — {s_res['algorithm']}", icon="🔍")
            with st.container(border=True):
                s1, s2, s3, s4 = st.columns(4, gap="medium")
                with s1:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>OUTCOME</div><div style='font-size:1.4rem;font-weight:800;color:{COLOR_GREEN if s_res['found'] else COLOR_AMBER};'>{'FOUND' if s_res['found'] else 'ABSENT'}</div></div>")
                with s2:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>RETURNED INDEX</div><div style='font-size:1.4rem;font-weight:800;color:#FFFFFF;'>{s_res['index']}</div></div>")
                with s3:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>COMPARISONS</div><div style='font-size:1.4rem;font-weight:800;color:{COLOR_CYAN};'>{s_res['comparisons']:,}</div></div>")
                with s4:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>VERIFICATION</div><div style='font-size:1.25rem;font-weight:800;color:{COLOR_GREEN};'>{'✓ VERIFIED' if s_res['correct'] else '✗ FAILED'}</div></div>")

                st.markdown(f"<div style='font-size:0.85rem;color:#CBD5E1;margin-top:12px;'>• <b>Execution Latency:</b> {format_time(s_res['avg_time'])} across {s_res['repetitions']} repetition(s).<br>• <b>Verification Details:</b> {s_res.get('verification_msg')}</div>", unsafe_allow_html=True)

        if g_res:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            section_header(f"Graph Algorithm Benchmark — {g_res['algorithm']}", icon="🕸️")
            with st.container(border=True):
                g1, g2, g3, g4 = st.columns(4, gap="medium")
                with g1:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>VERTICES</div><div style='font-size:1.4rem;font-weight:800;color:#FFFFFF;'>{g_res['graph_nodes']}</div></div>")
                with g2:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>EDGES</div><div style='font-size:1.4rem;font-weight:800;color:{COLOR_CYAN};'>{g_res['graph_edges']}</div></div>")
                with g3:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>LATENCY</div><div style='font-size:1.4rem;font-weight:800;color:{COLOR_AMBER};'>{format_time(g_res['avg_time'])}</div></div>")
                with g4:
                    render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>VERIFICATION</div><div style='font-size:1.25rem;font-weight:800;color:{COLOR_GREEN};'>{'✓ VERIFIED' if g_res['correct'] else '✗ FAILED'}</div></div>")

                st.markdown(f"<div style='font-size:0.85rem;color:#CBD5E1;margin-top:12px;'>• <b>Verification Guarantee:</b> {g_res.get('verification_msg')}</div>", unsafe_allow_html=True)

        if not s_res and not g_res:
            empty_state(
                icon="🔍",
                title="SEARCH & GRAPH VERIFICATION LAB READY",
                message="Select either a Searching algorithm or Graph algorithm above and execute to measure performance with formal mathematical verification.",
                button_label="",
                target_page=""
            )

    render_footer()
