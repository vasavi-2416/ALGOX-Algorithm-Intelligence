"""
ALGOX — Algorithm Head-to-Head Comparison Module
Direct empirical confrontation across single or multiple input sizes, charting asymptotic scaling curves and comparing theoretical vs practical behavior.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.ui import (
    section_header,
    render_html,
    empty_state,
    get_plotly_layout,
    format_time,
    format_number,
    warning_card,
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
from core.benchmark import run_benchmark, check_safety_level, SORTING_FUNCTION_MAP
from core.complexity import ALGORITHM_COMPLEXITY

def render_comparison(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">⚖️</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(6,182,212,0.85);display:block;">ALGOX · ALGORITHM COMPARISON</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Algorithm Comparison</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Direct empirical head-to-head confrontation across single or multiple input sizes, charting asymptotic scaling curves and comparing theoretical vs practical behavior.
</p>
</div>
""")

    section_header("Comparison Configuration", icon="⚖️", subtitle="Configure algorithm contenders, dataset distributions, and analysis mode.")

    with st.container(border=True):
        mode = st.radio(
            "Analysis Mode",
            ["Single Input Size", "Multiple Input Sizes (Scaling)", "Dataset Distribution Comparison"],
            key="comp_mode",
            horizontal=True
        )

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
        default_algos = ["Merge Sort", "Quick Sort", "Heap Sort"]
        selected_algos = st.multiselect(
            "Select Contender Algorithms",
            list(SORTING_FUNCTION_MAP.keys()),
            default=default_algos,
            key="comp_algos",
            help="Choose at least 2 algorithms to compare."
        )

        col_d, col_opt = st.columns(2, gap="medium")

        if mode == "Single Input Size":
            with col_d:
                distribution = st.selectbox("Dataset Distribution", DISTRIBUTIONS, index=0, key="comp_dist")
            with col_opt:
                single_n = st.slider("Dataset Size (N)", min_value=100, max_value=5000, value=1000, step=100, key="slider_comp_single_n")

            # Safety Check
            safety_level, safety_msg = check_safety_level(selected_algos, single_n)
            if safety_level in ('danger', 'warning'):
                warning_card("Complexity Warning", safety_msg)

            comp_run = st.button("⚖️ COMPARE HEAD-TO-HEAD", disabled=len(selected_algos) < 2, use_container_width=True, type="primary", key="comp_btn_single")

            if comp_run:
                with st.spinner("Generating dataset and measuring contenders..."):
                    arr = generate_dataset(single_n, distribution, seed=101)
                    db.log_dataset(f"CompSingle-{distribution}-{single_n}", distribution, single_n)
                    results = []
                    for algo in selected_algos:
                        res = run_benchmark(algo, arr, repetitions=2)
                        results.append(res)
                        db.insert_experiment({
                            'algorithm': res['algorithm'],
                            'category': 'Sorting',
                            'dataset': distribution,
                            'input_size': res['input_size'],
                            'avg_time': res['avg_time'],
                            'min_time': res['min_time'],
                            'max_time': res['max_time'],
                            'std_dev': res.get('std_dev', 0.0),
                            'seed': 101,
                            'comparisons': res['comparisons'],
                            'swaps': res['swaps'],
                            'memory_bytes': res['memory_bytes'],
                            'correct': res['correct'],
                            'repetitions': res['repetitions'],
                            'notes': f'Comparison Single Size (N={single_n})'
                        })
                    st.session_state['comp_single_results'] = results
                    st.session_state['comp_single_n'] = single_n
                    st.session_state['comp_single_dist'] = distribution

            results = st.session_state.get('comp_single_results')
            if results:
                _render_single_size_results(results, st.session_state.get('comp_single_n'), st.session_state.get('comp_single_dist'))
            else:
                render_html("""
<div style="max-width:520px;margin:2rem auto;text-align:center;background:rgba(124,58,237,0.06);
border:1px solid rgba(124,58,237,0.25);border-radius:16px;padding:36px 32px;min-height:200px;
display:flex;flex-direction:column;align-items:center;justify-content:center;">
<div style="font-size:2.6rem;margin-bottom:12px;">⚖️</div>
<div style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:8px;">Ready for Comparison</div>
<div style="color:#94A3B8;font-size:0.88rem;line-height:1.5;">
Select two or more algorithms above and press <b style="color:#8B5CF6;">COMPARE HEAD-TO-HEAD</b>.
</div>
</div>
""")

        elif mode == "Multiple Input Sizes (Scaling)":
            with col_d:
                distribution = st.selectbox("Dataset Distribution", DISTRIBUTIONS, index=0, key="comp_dist_multi")
            with col_opt:
                size_choices = [50, 100, 250, 500, 1000, 2000, 4000]
                selected_sizes = st.multiselect("Input Sizes (N)", size_choices, default=[100, 250, 500, 1000], key="comp_multi_sizes")

            if selected_sizes:
                max_n = max(selected_sizes)
                safety_level, safety_msg = check_safety_level(selected_algos, max_n)
                if safety_level in ('danger', 'warning'):
                    warning_card("Multi-Size Complexity Alert", safety_msg)

            comp_multi_run = st.button("📈 RUN SCALING ANALYSIS", disabled=not (len(selected_algos) >= 2 and selected_sizes), use_container_width=True, type="primary", key="comp_btn_multi")

            if comp_multi_run:
                with st.spinner("Executing empirical scaling across all size tiers..."):
                    scaling_data = {algo: [] for algo in selected_algos}
                    for n in sorted(selected_sizes):
                        arr = generate_dataset(n, distribution, seed=n)
                        for algo in selected_algos:
                            res = run_benchmark(algo, arr, repetitions=2)
                            scaling_data[algo].append({
                                'N': n,
                                'time_ms': res['avg_time'] * 1000,
                                'comparisons': res['comparisons'],
                                'swaps': res['swaps'] + res.get('shifts', 0)
                            })
                    st.session_state['comp_scaling_data'] = scaling_data
                    st.session_state['comp_scaling_dist'] = distribution

            scaling_data = st.session_state.get('comp_scaling_data')
            if scaling_data:
                _render_scaling_results(scaling_data, st.session_state.get('comp_scaling_dist'))
            else:
                render_html("""
<div style="max-width:520px;margin:2rem auto;text-align:center;background:rgba(6,182,212,0.06);
border:1px solid rgba(6,182,212,0.25);border-radius:16px;padding:36px 32px;min-height:200px;
display:flex;flex-direction:column;align-items:center;justify-content:center;">
<div style="font-size:2.6rem;margin-bottom:12px;">📈</div>
<div style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:8px;">Multi-Size Scaling Ready</div>
<div style="color:#94A3B8;font-size:0.88rem;line-height:1.5;">
Select input sizes and algorithms, then press <b style="color:#06B6D4;">RUN SCALING ANALYSIS</b>.
</div>
</div>
""")

        elif mode == "Dataset Distribution Comparison":
            with col_d:
                dist_n = st.slider("Fixed Input Size (N)", min_value=100, max_value=2500, value=500, step=100, key="comp_dist_n")
            with col_opt:
                st.caption("Contenders will be tested across all 5 standard distributions (Random, Sorted, Reverse Sorted, Nearly Sorted, Duplicate Heavy).")

            comp_dist_run = st.button("🧪 RUN DISTRIBUTION CONFRONTATION", disabled=len(selected_algos) < 2, use_container_width=True, type="primary", key="comp_btn_dist_mode")

            if comp_dist_run:
                with st.spinner("Benchmarking across all 5 distributions..."):
                    dist_results = {}
                    for d in DISTRIBUTIONS:
                        arr = generate_dataset(dist_n, d, seed=42)
                        dist_results[d] = {}
                        for algo in selected_algos:
                            res = run_benchmark(algo, arr, repetitions=2)
                            dist_results[d][algo] = res['avg_time'] * 1000.0
                    st.session_state['comp_dist_matrix_results'] = dist_results
                    st.session_state['comp_dist_matrix_n'] = dist_n
                    st.session_state['comp_dist_algos'] = selected_algos

            d_matrix = st.session_state.get('comp_dist_matrix_results')
            if d_matrix:
                _render_distribution_comparison_results(d_matrix, st.session_state.get('comp_dist_matrix_n'), st.session_state.get('comp_dist_algos', selected_algos))
            else:
                render_html("""
<div style="max-width:520px;margin:2rem auto;text-align:center;background:rgba(59,130,246,0.06);
border:1px solid rgba(59,130,246,0.25);border-radius:16px;padding:36px 32px;min-height:200px;
display:flex;flex-direction:column;align-items:center;justify-content:center;">
<div style="font-size:2.6rem;margin-bottom:12px;">📊</div>
<div style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:8px;">Distribution Confrontation Ready</div>
<div style="color:#94A3B8;font-size:0.88rem;line-height:1.5;">
Choose input size N and algorithms, then press <b style="color:#3B82F6;">RUN DISTRIBUTION CONFRONTATION</b>.
</div>
</div>
""")


def _render_single_size_results(results, n, dist):
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    section_header(f"Algorithm Comparison Table (N={n:,}, {dist})", icon="📋")

    # Table
    table_data = []
    for r in results:
        meta = ALGORITHM_COMPLEXITY.get(r['algorithm'], {})
        std_val = r.get('std_dev', 0.0) or 0.0
        table_data.append({
            "Algorithm": r['algorithm'],
            "Theoretical Avg": meta.get('average', 'N/A'),
            "Empirical Time": format_time(r['avg_time']),
            "Std Dev": f"±{std_val*1000:.3f} ms" if std_val > 0 else "—",
            "Comparisons": format_number(r['comparisons']),
            "Swaps / Shifts": format_number(r['swaps'] + r.get('shifts', 0)),
            "Aux Space": meta.get('space', 'N/A'),
            "Stable?": "Yes" if meta.get('stable') else "No",
            "In-place?": "Yes" if meta.get('in_place') else "No",
            "Verification": "✅ Verified" if r.get('correct') else "❌ Failed"
        })
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    df_export = pd.DataFrame(table_data)
    st.download_button(
        label="📥 Export Comparison CSV",
        data=df_export.to_csv(index=False),
        file_name=f"algox_comparison_{dist}_N{n}.csv",
        mime="text/csv",
        key="comp_export_btn"
    )

    # 1. Execution Time Chart (FULL WIDTH)
    section_header("Execution Time Comparison", icon="⏱️")
    algo_names = [r['algorithm'] for r in results]
    times_ms = [r['avg_time'] * 1000 for r in results]
    fig_time = go.Figure(data=[
        go.Bar(
            x=algo_names,
            y=times_ms,
            marker=dict(color=COLOR_CYAN),
            text=[f"{t:.2f} ms" for t in times_ms],
            textposition='outside'
        )
    ])
    fig_time.update_layout(get_plotly_layout("Execution Latency (ms)", height=320, x_title="Contender", y_title="Time (ms)"))
    st.plotly_chart(fig_time, use_container_width=True)

    # 2. Comparisons Chart (FULL WIDTH)
    section_header("Comparisons Count", icon="🔍")
    comps = [r['comparisons'] for r in results]
    fig_comps = go.Figure(data=[
        go.Bar(
            x=algo_names,
            y=comps,
            marker=dict(color=COLOR_PURPLE),
            text=[f"{c:,}" for c in comps],
            textposition='outside'
        )
    ])
    fig_comps.update_layout(get_plotly_layout("Total Element Comparisons", height=320, x_title="Contender", y_title="Comparisons"))
    st.plotly_chart(fig_comps, use_container_width=True)

    # 3. Swaps / Shifts Chart (FULL WIDTH)
    section_header("Swaps & Shifts Count", icon="🔄")
    swaps = [r['swaps'] + r.get('shifts', 0) for r in results]
    fig_swaps = go.Figure(data=[
        go.Bar(
            x=algo_names,
            y=swaps,
            marker=dict(color=COLOR_AMBER),
            text=[f"{s:,}" for s in swaps],
            textposition='outside'
        )
    ])
    fig_swaps.update_layout(get_plotly_layout("Total Element Swaps / Memory Shifts", height=320, x_title="Contender", y_title="Swaps / Shifts"))
    st.plotly_chart(fig_swaps, use_container_width=True)

    # Theoretical vs Empirical Dissection
    section_header("DAA Theoretical vs Empirical Analysis", icon="🔬")
    with st.container(border=True):
        render_html(f"""
        <div style="font-weight: 700; font-size: 1rem; color: #FFFFFF; margin-bottom: 0.5rem;">
            Theoretical Complexity vs Empirical Reality
        </div>
        <p style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;">
            While algorithms such as <b>Merge Sort</b>, <b>Quick Sort</b>, and <b>Heap Sort</b> share identical asymptotic bounds of <b>O(n log n)</b>, their physical runtimes diverge due to constant factor overheads:
        </p>
        <ul style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6;">
            <li><b>Quick Sort</b> benefits from cache line locality during contiguous array partitioning, resulting in fewer CPU branch mispredictions.</li>
            <li><b>Merge Sort</b> guarantees O(n log n) in all distributions with stability, but bears the memory copy overhead of O(n) auxiliary allocations.</li>
            <li><b>Heap Sort</b> achieves in-place O(1) space, but non-contiguous parent/child hops (2i+1, 2i+2) cause cache line misses on large arrays.</li>
        </ul>
        """)


def _render_scaling_results(scaling_data, dist):
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    section_header(f"Empirical Scaling Curves ({dist})", icon="📈")

    tab1, tab2, tab3 = st.tabs(["Execution Time Scaling", "Comparisons Scaling", "Swaps / Shifts Scaling"])

    colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_AMBER, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE_LIGHT]

    with tab1:
        fig_scale = go.Figure()
        for idx, (algo, data_points) in enumerate(scaling_data.items()):
            x_vals = [p['N'] for p in data_points]
            y_vals = [p['time_ms'] for p in data_points]
            fig_scale.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers',
                name=algo,
                line=dict(color=colors[idx % len(colors)], width=2.5),
                marker=dict(size=7)
            ))
        fig_scale.update_layout(get_plotly_layout(f"Execution Latency vs Input Size N ({dist})", height=380, x_title="Input Size (N)", y_title="Time (ms)"))
        st.plotly_chart(fig_scale, use_container_width=True)

    with tab2:
        fig_ops = go.Figure()
        for idx, (algo, data_points) in enumerate(scaling_data.items()):
            x_vals = [p['N'] for p in data_points]
            y_vals = [p['comparisons'] for p in data_points]
            fig_ops.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers',
                name=algo,
                line=dict(color=colors[idx % len(colors)], width=2.5),
                marker=dict(size=7)
            ))
        fig_ops.update_layout(get_plotly_layout(f"Comparisons Count vs Input Size N ({dist})", height=380, x_title="Input Size (N)", y_title="Comparisons"))
        st.plotly_chart(fig_ops, use_container_width=True)

    with tab3:
        fig_swaps = go.Figure()
        for idx, (algo, data_points) in enumerate(scaling_data.items()):
            x_vals = [p['N'] for p in data_points]
            y_vals = [p['swaps'] for p in data_points]
            fig_swaps.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers',
                name=algo,
                line=dict(color=colors[idx % len(colors)], width=2.5),
                marker=dict(size=7)
            ))
        fig_swaps.update_layout(get_plotly_layout(f"Swaps / Shifts Count vs Input Size N ({dist})", height=380, x_title="Input Size (N)", y_title="Swaps / Shifts"))
        st.plotly_chart(fig_swaps, use_container_width=True)

    render_footer()


def _render_distribution_comparison_results(d_matrix, dist_n, selected_algos):
    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
    section_header(f"Distribution Performance Matrix (N={dist_n:,})", icon="🧪")

    df_dist = pd.DataFrame(d_matrix)
    st.dataframe(df_dist.applymap(lambda v: f"{v:.2f} ms"), use_container_width=True)

    section_header("Latency Across Distributions", icon="⏱️")
    fig_dist_bar = go.Figure()
    colors = [COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE, COLOR_AMBER, COLOR_GREEN, COLOR_RED]
    for idx, algo in enumerate(selected_algos):
        y_times = [d_matrix[d].get(algo, 0) for d in DISTRIBUTIONS]
        fig_dist_bar.add_trace(go.Bar(
            name=algo,
            x=DISTRIBUTIONS,
            y=y_times,
            marker_color=colors[idx % len(colors)]
        ))
    fig_dist_bar.update_layout(get_plotly_layout("Latency Across Distributions (ms)", height=360, x_title="Distribution", y_title="Latency (ms)"))
    fig_dist_bar.update_layout(barmode='group')
    st.plotly_chart(fig_dist_bar, use_container_width=True)

    render_footer()
