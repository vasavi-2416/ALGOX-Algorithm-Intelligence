"""
ALGOX — Complexity Analyzer Module
Interactive asymptotic growth curves, asymptotic taxonomy matrix, and rigorous Big-O derivations.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from core.ui import (
    section_header,
    render_html,
    render_footer,
    get_plotly_layout,
    complexity_badge,
    empty_state,
    format_time,
    format_number,
    COLOR_PURPLE,
    COLOR_PURPLE_LIGHT,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT_MUTED
)
from core.complexity import ALGORITHM_COMPLEXITY

def render_complexity(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">📈</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(245,158,11,0.85);display:block;">ALGOX · COMPLEXITY ANALYZER</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Complexity Analyzer</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Interactive asymptotic growth curves, Big-O taxonomy matrix, empirical-vs-theoretical correlation, and formal DAA mathematical derivations.
</p>
</div>
""")

    t1, t2, t3, t4 = st.tabs([
        "1. 📐 Interactive Big-O Curves",
        "2. 📊 Complexity Taxonomy Matrix",
        "3. 🔬 Empirical vs Theoretical",
        "4. 📜 Formal DAA Deep Dive"
    ])

    with t1:
        _render_growth_curves()

    with t2:
        _render_taxonomy_matrix()

    with t3:
        _render_empirical_vs_theoretical(db)

    with t4:
        _render_deep_dives()


def _render_growth_curves():
    section_header("Complexity Growth Curves", icon="📐", subtitle="Plot and compare asymptotic mathematical growth rates across problem scales.")

    with st.container(border=True):
        selected_curves = st.multiselect(
            "Select Asymptotic Complexities to Chart",
            ["O(1) Constant", "O(log n) Logarithmic", "O(n) Linear", "O(n log n) Linearithmic", "O(n²) Quadratic"],
            default=["O(1) Constant", "O(log n) Logarithmic", "O(n) Linear", "O(n log n) Linearithmic", "O(n²) Quadratic"],
            key="comp_curve_select"
        )

        c_n, c_log = st.columns([2, 1], gap="medium")
        with c_n:
            max_n = st.slider("Maximum Input Scale (N)", min_value=10, max_value=250, value=80, step=10, key="comp_max_n")
        with c_log:
            use_log_y = st.checkbox("Logarithmic Vertical Scale (log₁₀)", value=False, key="comp_log_y")

    n_vals = np.linspace(1, max_n, 200)
    fig = go.Figure()

    curve_configs = {
        "O(1) Constant": (np.ones_like(n_vals), COLOR_GREEN),
        "O(log n) Logarithmic": (np.log2(n_vals), COLOR_CYAN),
        "O(n) Linear": (n_vals, COLOR_BLUE),
        "O(n log n) Linearithmic": (n_vals * np.log2(n_vals), COLOR_AMBER),
        "O(n²) Quadratic": (n_vals ** 2, COLOR_PURPLE_LIGHT)
    }

    for name in selected_curves:
        if name in curve_configs:
            y_vals, color = curve_configs[name]
            fig.add_trace(go.Scatter(
                x=n_vals,
                y=y_vals,
                mode='lines',
                name=name,
                line=dict(color=color, width=3)
            ))

    layout = get_plotly_layout("Asymptotic Operations Growth Curve", height=380, x_title="Input Size (N)", y_title="Operations Count")
    if use_log_y:
        layout['yaxis']['type'] = 'log'
        layout['title']['text'] += " [Logarithmic Scale]"
    fig.update_layout(layout)

    # Full width chart
    st.plotly_chart(fig, use_container_width=True)

    # Full width academic explanation card
    with st.container(border=True):
        render_html(f"""
        <div style="padding: 4px 6px;">
            <div style="font-weight: 700; font-size: 0.95rem; color: #FFFFFF; margin-bottom: 0.4rem;">
                Formal Asymptotic Growth Hierarchy
            </div>
            <p style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6; margin: 0 0 6px 0;">
                <code style="color:#22C55E;">O(1)</code> &sub;
                <code style="color:#06B6D4;">O(log n)</code> &sub;
                <code style="color:#3B82F6;">O(n)</code> &sub;
                <code style="color:#F59E0B;">O(n log n)</code> &sub;
                <code style="color:#C084FC;">O(n²)</code> &sub;
                <code style="color:#EF4444;">O(2ⁿ)</code> &sub;
                <code style="color:#F43F5E;">O(n!)</code>
            </p>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5; margin: 0;">
                In the Design and Analysis of Algorithms (DAA), algorithms bounded by polynomial time O(nᵏ) are defined as tractable.
                Linearithmic bounds O(n log n) represent the information-theoretic lower bound for comparison-based sorting.
            </p>
        </div>
        """)


def _render_taxonomy_matrix():
    section_header("Asymptotic Taxonomy Matrix (All 13 Core Algorithms)", icon="📊", subtitle="Rigorous academic classification across paradigms, best/average/worst bounds, and spatial properties.")

    matrix_rows = []
    for name, info in ALGORITHM_COMPLEXITY.items():
        matrix_rows.append({
            "Algorithm": name,
            "Category": info['category'],
            "Paradigm": info['paradigm'],
            "Best Case": info['best'],
            "Average Case": info['average'],
            "Worst Case": info['worst'],
            "Aux Space": info['space'],
            "Stable": "✓ Yes" if info.get('stable') else "✗ No",
            "In-Place": "✓ Yes" if info.get('in_place') else "✗ No"
        })

    df = pd.DataFrame(matrix_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_empirical_vs_theoretical(db):
    section_header("Empirical Performance vs Theoretical Bounds", icon="🔬", subtitle="Directly correlate mathematical asymptotic Big-O bounds with physical SQLite execution records.")

    exp_count = db.get_experiment_count()
    if exp_count == 0:
        empty_state(
            icon="📊",
            title="No Empirical Benchmarks Found",
            message="Execute benchmarks in the Benchmark Lab or Algorithm Comparison to populate the database with empirical measurements for theoretical correlation.",
            button_label="Open Benchmark Lab",
            target_page="Benchmark Lab"
        )
        return

    sorting_algos = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort', 'Heap Sort']
    target_algo = st.selectbox("Select Algorithm to Inspect", sorting_algos, key="cplx_emp_algo")

    meta = ALGORITHM_COMPLEXITY.get(target_algo, {})

    # Query real empirical records from SQLite
    with db.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT input_size, dataset, AVG(avg_time) * 1000.0 as avg_ms, AVG(comparisons) as avg_comps
            FROM experiments
            WHERE algorithm = ?
            GROUP BY input_size, dataset
            ORDER BY input_size ASC
        """, (target_algo,))
        emp_records = cur.fetchall()

    ec1, ec2 = st.columns([1, 1], gap="large")

    with ec1:
        with st.container(border=True):
            render_html(f"""
            <div style="padding:4px 2px;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #8B5CF6; text-transform:uppercase; letter-spacing:0.05em; margin-bottom: 0.5rem;">
                    THEORETICAL ASYMPTOTIC ENVELOPE
                </div>
                <div style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.5; margin-bottom: 0.75rem;">
                    Theoretical bounds represent mathematical limits as input size approaches infinity (N &rarr; &infin;), independent of CPU clock speeds or compiler optimizations.
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.84rem;">
                    <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px;">
                        <span style="color: #94A3B8;">Best-Case:</span><br>
                        <b style="color: #4ADE80;">{meta.get('best', 'N/A')}</b>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px;">
                        <span style="color: #94A3B8;">Average-Case:</span><br>
                        <b style="color: #60A5FA;">{meta.get('average', 'N/A')}</b>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px;">
                        <span style="color: #94A3B8;">Worst-Case:</span><br>
                        <b style="color: #F87171;">{meta.get('worst', 'N/A')}</b>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px;">
                        <span style="color: #94A3B8;">Auxiliary Space:</span><br>
                        <b style="color: #C084FC;">{meta.get('space', 'N/A')}</b>
                    </div>
                </div>
            </div>
            """)

    with ec2:
        with st.container(border=True):
            render_html(f"""
            <div style="padding:4px 2px;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #06B6D4; text-transform:uppercase; letter-spacing:0.05em; margin-bottom: 0.5rem;">
                    EMPIRICAL MEASUREMENTS ({target_algo.upper()})
                </div>
            </div>
            """)
            if emp_records:
                df_emp = pd.DataFrame(emp_records, columns=["Input Size (N)", "Dataset Distribution", "Measured Time (ms)", "Comparisons"])
                df_emp["Input Size (N)"] = df_emp["Input Size (N)"].apply(lambda v: f"{v:,}")
                df_emp["Measured Time (ms)"] = df_emp["Measured Time (ms)"].apply(lambda v: f"{v:.3f} ms")
                df_emp["Comparisons"] = df_emp["Comparisons"].apply(lambda v: f"{int(v):,}")
                st.dataframe(df_emp, use_container_width=True, hide_index=True)
            else:
                render_html(f"""
                <div style="color: #94A3B8; font-size: 0.82rem; padding: 1.5rem 0.5rem; text-align: center;">
                    No empirical benchmark records currently found for <b>{target_algo}</b> in SQLite.<br>
                    Run this algorithm in the Benchmark Lab to record physical execution measurements.
                </div>
                """)

    # Full width academic reflection box
    with st.container(border=True):
        render_html(f"""
        <div style="padding:4px 6px;">
            <div style="font-weight: 700; font-size: 0.9rem; color: #FFFFFF; margin-bottom: 0.35rem;">
                Academic Reflection: Why Physical Time &ne; Theoretical Operations Count
            </div>
            <p style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.55; margin: 0;">
                Big-O notation discards lower-order terms and hardware constants (T(n) = c &middot; f(n) &rarr; O(f(n))). Consequently, two algorithms with identical O(n log n) complexity (e.g. Quick Sort and Heap Sort) demonstrate distinct measured execution times because Quick Sort has lower constant factors c due to sequential memory access, pointer locality, and L1/L2 cache line utilization.
            </p>
        </div>
        """)


def _render_deep_dives():
    # Section 12 Structure:
    # Algorithm Selection (FULL WIDTH) -> Complexity Summary (Best | Average | Worst | Space) -> Complexity Chart / Mathematical Derivation (FULL WIDTH) -> Explanation (FULL WIDTH)
    section_header("Formal DAA Derivations & Recurrences", icon="📜", subtitle="Mathematical derivations of algorithmic upper and lower complexity bounds.")

    # 1. Algorithm Selection — FULL WIDTH
    selected_algo = st.selectbox("Select Algorithm to Inspect Formal Proof", list(ALGORITHM_COMPLEXITY.keys()), key="comp_deriv_algo")
    meta = ALGORITHM_COMPLEXITY[selected_algo]

    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    # 2. Complexity Summary — Best | Average | Worst | Space (.algox-stat-card)
    s_c1, s_c2, s_c3, s_c4 = st.columns(4, gap="medium")
    with s_c1:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">BEST CASE</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#22C55E; white-space:nowrap;">{meta['best']}</div>
        </div>
        """)
    with s_c2:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">AVERAGE CASE</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#F59E0B; white-space:nowrap;">{meta['average']}</div>
        </div>
        """)
    with s_c3:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">WORST CASE</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#EF4444; white-space:nowrap;">{meta['worst']}</div>
        </div>
        """)
    with s_c4:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">AUXILIARY SPACE</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#3B82F6; white-space:nowrap;">{meta['space']}</div>
        </div>
        """)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 3. Mathematical Derivation / Proof — FULL WIDTH
    with st.container(border=True):
        st.markdown(f"<h3 style='color: #FFFFFF; font-size: 1.25rem; margin-top: 0;'>{selected_algo} — Rigorous Mathematical Derivation</h3>", unsafe_allow_html=True)

        if selected_algo == "Merge Sort":
            st.markdown(r"""
            **Divide-and-Conquer Recurrence Relation:**
            $$T(n) = 2T(n/2) + \Theta(n)$$

            **Application of the Master Theorem:**
            - Recurrence form: $T(n) = aT(n/b) + f(n)$ with $a = 2$, $b = 2$, $f(n) = \Theta(n)$
            - Critical exponent: $n^{\log_b a} = n^{\log_2 2} = n^1 = n$
            - Since $f(n) = \Theta(n^{\log_b a}) = \Theta(n)$, **Case 2** of the Master Theorem applies:
            $$T(n) = \Theta(n \log n)$$
            This bound holds unconditionally across best, average, and worst-case permutations because merging always processes $n$ items across $\log_2(n)$ recursive levels.
            """)
        elif selected_algo == "Quick Sort":
            st.markdown(r"""
            **Recurrence Relations:**
            - **Best Case (Equally Balanced Partitions):**
              $$T(n) = 2T(n/2) + \Theta(n) \implies \Theta(n \log n)$$
            - **Worst Case (Maximally Unbalanced Partition, e.g. Pre-sorted input with last-element pivot):**
              $$T(n) = T(n - 1) + \Theta(n) = \sum_{i=1}^n i = \frac{n(n+1)}{2} = \Theta(n^2)$$
            - **Average Case (Expected over Random Permutations):**
              $$T(n) = \frac{1}{n}\sum_{q=0}^{n-1} (T(q) + T(n-1-q)) + \Theta(n) = \Theta(n \log n)$$
            """)
        elif selected_algo in ("Bubble Sort", "Selection Sort", "Insertion Sort"):
            st.markdown(r"""
            **Nested Iteration Summations:**
            $$\sum_{i=1}^{n-1} (n - i) = (n-1) + (n-2) + \dots + 1 = \frac{n(n-1)}{2} = \frac{1}{2}n^2 - \frac{1}{2}n = \Theta(n^2)$$
            - **Adaptive Exception:** Insertion Sort and early-exit Bubble Sort detect sorted inputs in a single pass, performing only $n - 1$ comparisons without swaps: $\Omega(n)$.
            """)
        elif selected_algo == "Binary Search":
            st.markdown(r"""
            **Bisection Recurrence Relation:**
            $$T(n) = T(n/2) + O(1)$$
            Using Master Theorem with $a=1, b=2, f(n)=O(1)$:
            $$n^{\log_2 1} = n^0 = 1 = \Theta(f(n)) \implies T(n) = \Theta(\log n)$$
            Each query comparison strictly halves the active search interval $[lo, hi]$.
            """)
        elif selected_algo == "Heap Sort":
            st.markdown(r"""
            **Two-Phase Analysis:**
            1. **Heap Construction (Build-Max-Heap):**
               $$\sum_{h=0}^{\lfloor\log n\rfloor} \left\lceil\frac{n}{2^{h+1}}\right\rceil O(h) = O\left(n \sum_{h=0}^\infty \frac{h}{2^h}\right) = O(2n) = O(n)$$
            2. **Extraction Phase:**
               $n - 1$ calls to Max-Heapify on trees of height up to $\log n$:
               $$\sum_{i=1}^{n-1} O(\log i) = O(n \log n)$$
            Total Worst-Case Time: $O(n) + O(n \log n) = O(n \log n)$.
            """)
        else:
            st.markdown(f"""
            **Graph Traversal / Optimization Complexity Formulation:**
            - **Vertices:** $|V|$, **Edges:** $|E|$
            - **Average-Case Time Bound:** `{meta['average']}`
            - **Auxiliary Space Bound:** `{meta['space']}`
            - **Algorithmic Paradigm:** `{meta['paradigm']}`
            """)

    # 4. Architectural Explanation — FULL WIDTH
    with st.container(border=True):
        st.markdown(f"""
        **Algorithmic Properties & Implementation Notes:**
        - **Description:** {meta.get('description', '')}
        - **How It Works:** {meta.get('how_it_works', '')}
        - **Stability:** {'Preserves relative order of duplicate keys (Stable)' if meta.get('stable') else 'May invert relative order of duplicate keys (Not Stable)'}
        - **In-Place:** {'Operates with O(1) auxiliary working memory' if meta.get('in_place') else f'Requires auxiliary allocations ({meta.get("space")})'}
        """)

    render_footer()
