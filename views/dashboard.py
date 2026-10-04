import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime

from core.ui import (
    render_html,
    render_kpi_row,
    section_header,
    empty_state,
    get_plotly_layout,
    format_time,
    format_number,
    render_footer,
    COLOR_PURPLE,
    COLOR_PURPLE_LIGHT,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT,
    COLOR_TEXT_MUTED
)
from core.dataset import generate_dataset, DISTRIBUTIONS
from core.benchmark import benchmark_multiple, SORTING_FUNCTION_MAP
from core.complexity import ALGORITHM_COMPLEXITY

DAA_INSIGHTS = [
    ("Why does Insertion Sort achieve O(n) on nearly sorted data?",
     "Insertion Sort operates by shifting elements into an already-sorted prefix. When the inversion count is small, the inner while-loop terminates almost immediately after 1 or 2 comparisons per element, requiring at most n - 1 comparisons to verify order without performing significant memory shifts."),

    ("Why can Quick Sort degrade to O(n²) in the worst case?",
     "When a naive pivot (such as the first or last element) is chosen on already sorted or reverse-sorted data, one partition ends up with n - 1 elements and the other with 0 elements. The recursion tree degenerates from depth log₂(n) to depth n, producing Σ(n - i) = n(n - 1)/2 comparisons."),

    ("Why does Merge Sort require O(n) auxiliary memory for arrays?",
     "While the divide step only computes midpoints, the linear-time combine (merge) step requires merging two adjacent sorted subarrays. Because contiguous memory cannot be shifted in-place without incurring O(n²) overhead, Merge Sort allocates a secondary scratch buffer of size n to hold merged values before copying them back."),

    ("How does Dijkstra's greedy strategy guarantee optimality?",
     "Dijkstra maintains the invariant that once a vertex u is extracted from the min-priority queue, its tentative distance dist[u] is guaranteed to be the true shortest path distance from the source. Because all edge weights are non-negative, any alternative path to u would have to traverse edges with positive weight, yielding a strictly greater distance."),

    ("Why are BFS and DFS fundamentally different graph paradigms?",
     "BFS uses a FIFO queue to explore nodes level-by-level in non-decreasing order of distance, guaranteeing the shortest path in unweighted graphs. DFS uses a LIFO stack (or recursion) to explore as deep as possible before backtracking, making it ideal for topological sorting, cycle detection, and strongly connected components."),

    ("How does Binary Search achieve O(log n) efficiency?",
     "Binary Search halves the search space at every comparison step. For an array of size N, after k bisections the remaining elements are N / 2^k. Solving N / 2^k = 1 gives k = log₂(N). For 1,000,000 items, at most 20 comparisons are needed to find or confirm the absence of any key."),

    ("Why does Heap Sort build a max-heap in O(n) time, not O(n log n)?",
     "Bottom-up heap construction calls sift-down on nodes starting at the leaves. Most nodes reside near the bottom of the tree where heights are small: n/4 nodes have height 1, n/8 have height 2, etc. The sum Σ (h / 2^h) converges to 2, proving that building the initial heap is strictly linear O(n)."),

    ("Why does Kruskal's algorithm use Union-Find with path compression?",
     "Kruskal sorts all E edges and adds each edge that connects two previously disjoint trees. The Disjoint Set Union (DSU) structure with path compression and union-by-rank optimizes cycle detection to nearly O(1) amortized time (specifically O(α(V)), where α is the inverse Ackermann function)."),

    ("Why does Selection Sort always execute exactly n(n - 1)/2 comparisons?",
     "Unlike Insertion Sort, Selection Sort lacks an adaptive early termination mechanism. In pass i, it must scan every single element from i + 1 to n - 1 to identify the absolute minimum index, regardless of whether the array is completely sorted or in random order."),

    ("What determines whether an algorithm is in-place?",
     "An algorithm is defined as in-place if its auxiliary memory consumption (excluding the input array itself) is bounded by O(1) or O(log n) for recursion stack frames. Heap Sort is strictly O(1), Quick Sort is O(log n), while Merge Sort is O(n).")
]

def render_dashboard(db):
    # ==========================================================
    # 1. SYSTEM OVERVIEW HERO PANEL (Futuristic Command Center)
    # ==========================================================
    render_html(f"""
    <div class="algox-hero-card" style="position: relative; overflow: hidden;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; position: relative; z-index: 2;">
            <div style="max-width: 780px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 10px #22C55E;"></span>
                    <span style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #86EFAC;">SYSTEM STATUS: ONLINE &bull; RESEARCH LAB MODE</span>
                </div>
                <h2 style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; margin: 0 0 6px 0; letter-spacing: -0.02em; line-height: 1.2;">
                    ALGOX Laboratory Command Center
                </h2>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.5; margin-bottom: 16px;">
                    Design and Analysis of Algorithms &bull; Empirical Benchmarking, Visualization, and Complexity Platform
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span class="algox-badge algox-badge-purple" style="box-shadow: 0 0 10px rgba(168,85,247,0.25);">⚡ 13 Implementations Active</span>
                    <span class="algox-badge algox-badge-blue">📊 6 Sorting</span>
                    <span class="algox-badge algox-badge-cyan">🔍 2 Searching</span>
                    <span class="algox-badge algox-badge-green">🕸️ 5 Graph</span>
                    <span class="algox-badge algox-badge-amber">🗄️ SQLite Online</span>
                </div>
            </div>
            <!-- Futuristic Algorithmic Constellation SVG (Illuminated Nodes with Glow Filters) -->
            <div style="display: flex; align-items: center; justify-content: center;">
                <svg width="190" height="105" viewBox="0 0 190 105" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <filter id="glow-purple" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                        </filter>
                        <filter id="glow-blue" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                        </filter>
                        <filter id="glow-cyan" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                        </filter>
                        <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                        </filter>
                    </defs>
                    <line x1="30" y1="52" x2="95" y2="22" stroke="rgba(168,85,247,0.50)" stroke-width="1.8" stroke-dasharray="3 3"/>
                    <line x1="30" y1="52" x2="95" y2="82" stroke="rgba(6,182,212,0.50)" stroke-width="1.8"/>
                    <line x1="95" y1="22" x2="160" y2="52" stroke="rgba(59,130,246,0.55)" stroke-width="1.8"/>
                    <line x1="95" y1="82" x2="160" y2="52" stroke="rgba(168,85,247,0.50)" stroke-width="1.8" stroke-dasharray="3 3"/>
                    <line x1="95" y1="22" x2="95" y2="82" stroke="rgba(245,158,11,0.40)" stroke-width="1.2"/>
                    
                    <!-- Node 1: Purple -->
                    <circle cx="30" cy="52" r="10" fill="rgba(10,18,45,0.95)" stroke="#A855F7" stroke-width="2.2" filter="url(#glow-purple)"/>
                    <circle cx="30" cy="52" r="4" fill="#C084FC"/>
                    
                    <!-- Node 2: Blue -->
                    <circle cx="95" cy="22" r="11" fill="rgba(10,18,45,0.95)" stroke="#3B82F6" stroke-width="2.2" filter="url(#glow-blue)"/>
                    <circle cx="95" cy="22" r="4.5" fill="#60A5FA"/>
                    
                    <!-- Node 3: Cyan -->
                    <circle cx="95" cy="82" r="11" fill="rgba(10,18,45,0.95)" stroke="#06B6D4" stroke-width="2.2" filter="url(#glow-cyan)"/>
                    <circle cx="95" cy="82" r="4.5" fill="#22D3EE"/>
                    
                    <!-- Node 4: Green -->
                    <circle cx="160" cy="52" r="12" fill="rgba(10,18,45,0.95)" stroke="#22C55E" stroke-width="2.5" filter="url(#glow-green)"/>
                    <circle cx="160" cy="52" r="5" fill="#4ADE80"/>
                </svg>
            </div>
        </div>
    </div>
    """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 2. KPI GRID (3 cards × 2 rows)
    # ==========================================================
    exp_count = db.get_experiment_count()
    dataset_count = db.get_dataset_count()
    rec_count = db.get_recommendations_count()
    fastest_algo = db.get_fastest_algorithm("Sorting")
    avg_exec_time = db.get_average_execution_time()

    fastest_label = "No data"
    if fastest_algo and 'algorithm' in fastest_algo:
        fastest_label = f"{fastest_algo['algorithm']} ({format_time(fastest_algo.get('avg_time', 0))})"

    avg_time_label = format_time(avg_exec_time) if avg_exec_time is not None else "No data"

    total_comparisons = 0
    total_swaps = 0
    total_validated = 0
    slowest_label = "No data"

    if exp_count > 0:
        try:
            with db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT SUM(comparisons), SUM(swaps), COUNT(CASE WHEN correct = 1 THEN 1 END) FROM experiments")
                row = cur.fetchone()
                if row:
                    total_comparisons = row[0] or 0
                    total_swaps = row[1] or 0
                    total_validated = row[2] or 0

                cur.execute("SELECT algorithm, avg_time FROM experiments WHERE category = 'Sorting' ORDER BY avg_time DESC LIMIT 1")
                slow_row = cur.fetchone()
                if slow_row:
                    slowest_label = f"{slow_row[0]} ({format_time(slow_row[1])})"
        except Exception:
            pass

    # ROW 1 (3 Cards — Algorithms (Purple), Experiments (Blue), Fastest Measured (Cyan))
    r1_col1, r1_col2, r1_col3 = st.columns(3, gap="medium")
    row1_items = [
        ("ALGORITHMS", "13", "Implemented & Verified", "#C4B5FD", "purple", "⚙️"),
        ("EXPERIMENTS", f"{exp_count:,}", "Recorded Benchmarks", "#93C5FD", "blue", "🧪"),
        ("FASTEST MEASURED", fastest_label.split(' ')[0], fastest_label, "#67E8F9", "cyan", "⚡")
    ]
    for col, (label, val, sub, accent, glow_cls, icon) in zip([r1_col1, r1_col2, r1_col3], row1_items):
        with col:
            render_html(f"""
            <div class="algox-kpi-card {glow_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">{label}</span>
                    <span class="algox-neon-icon algox-neon-icon-{glow_cls}">{icon}</span>
                </div>
                <div class="algox-kpi-value" style="font-size: 24px; font-weight: 700; color: #FFFFFF; line-height: 1.1; margin-bottom: 8px;">{val}</div>
                <div style="font-size: 0.78rem; color: {accent}; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sub}</div>
            </div>
            """)

    render_html("<div style='margin-bottom: 18px;'></div>")

    # ROW 2 (3 Cards — Average Time (Amber), Total Datasets (Green), Recommendations (Pink))
    r2_col1, r2_col2, r2_col3 = st.columns(3, gap="medium")
    row2_items = [
        ("AVERAGE TIME", avg_time_label, "Across Recorded Runs", "#FCD34D", "amber", "⏱️"),
        ("TOTAL DATASETS", f"{dataset_count:,}", "Generated Syntheses", "#86EFAC", "green", "📊"),
        ("RECOMMENDATIONS", f"{rec_count:,}", "Algorithmic Queries", "#F472B6", "pink", "💡")
    ]
    for col, (label, val, sub, accent, glow_cls, icon) in zip([r2_col1, r2_col2, r2_col3], row2_items):
        with col:
            render_html(f"""
            <div class="algox-kpi-card {glow_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">{label}</span>
                    <span class="algox-neon-icon algox-neon-icon-{glow_cls}">{icon}</span>
                </div>
                <div class="algox-kpi-value" style="font-size: 24px; font-weight: 700; color: #FFFFFF; line-height: 1.1; margin-bottom: 8px;">{val}</div>
                <div style="font-size: 0.78rem; color: {accent}; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sub}</div>
            </div>
            """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 3. QUICK ACTIONS (6 Premium Action Cards with Icons & Descriptions)
    # ==========================================================
    section_header("Quick Actions", icon="⚡", subtitle="Direct access to core laboratory, visualizer, and analysis workbenches.")
    
    qa_row1 = st.columns(3, gap="medium")
    qa_actions_r1 = [
        ("⚗️ Run Benchmark", "Benchmark Lab", "Measure execution latencies and operation metrics", "qa_bench", "purple"),
        ("⚖️ Compare Algorithms", "Comparison", "Head-to-head empirical scaling confrontation", "qa_comp", "cyan"),
        ("🎬 Open Visualizer", "Visualizer", "Step-by-step state animations and execution trace", "qa_viz", "blue")
    ]

    for col, (title, target_page, desc, key, cls) in zip(qa_row1, qa_actions_r1):
        with col:
            with st.container(border=True):
                render_html(f"""
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.98rem; color: #FFFFFF; margin-bottom: 3px;">{title}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.4;">{desc}</div>
                </div>
                """)
                if st.button("Launch Module →", key=key, use_container_width=True):
                    st.session_state['current_page'] = target_page
                    st.rerun()

    render_html("<div style='margin-bottom: 16px;'></div>")

    qa_row2 = st.columns(3, gap="medium")
    qa_actions_r2 = [
        ("📈 Analyze Complexity", "Complexity Analyzer", "Interactive Big-O curves and asymptotic proofs", "qa_cplx", "amber"),
        ("🤖 Get Recommendation", "Recommendation", "Rule-based algorithmic selection for your constraints", "qa_rec", "pink"),
        ("🕸️ Graph Algorithms", "Graph Algorithms", "Interactive topology traversal, Dijkstra, and MST", "qa_graph", "green")
    ]

    for col, (title, target_page, desc, key, cls) in zip(qa_row2, qa_actions_r2):
        with col:
            with st.container(border=True):
                render_html(f"""
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.98rem; color: #FFFFFF; margin-bottom: 3px;">{title}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.4;">{desc}</div>
                </div>
                """)
                if st.button("Launch Module →", key=key, use_container_width=True):
                    st.session_state['current_page'] = target_page
                    st.rerun()

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 4. PERFORMANCE ANALYTICS (Two balanced columns)
    # ==========================================================
    section_header("Performance Analytics & Scaling", subtitle="Real execution metrics stored in SQLite and empirical runtime scaling trends.")
    sn_col1, sn_col2 = st.columns([1, 1.4], gap="large")

    # Left: Performance Snapshot Card
    with sn_col1:
        with st.container(border=True):
            render_html("""
            <div style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.85rem;">
                Performance Snapshot
            </div>
            """)

            if exp_count > 0:
                render_html(f"""
                <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.84rem;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 7px;">
                        <span style="color: #94A3B8;">Fastest Sorting Measured:</span>
                        <span style="font-weight: 700; color: {COLOR_GREEN};">{fastest_label}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 7px;">
                        <span style="color: #94A3B8;">Slowest Sorting Measured:</span>
                        <span style="font-weight: 700; color: {COLOR_AMBER};">{slowest_label}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 7px;">
                        <span style="color: #94A3B8;">Total Comparisons:</span>
                        <span style="font-weight: 700; color: #FFFFFF;">{total_comparisons:,}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 7px;">
                        <span style="color: #94A3B8;">Total Swaps / Shifts:</span>
                        <span style="font-weight: 700; color: #FFFFFF;">{total_swaps:,}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 7px;">
                        <span style="color: #94A3B8;">Total Validated Runs:</span>
                        <span style="font-weight: 700; color: {COLOR_CYAN};">{total_validated:,} / {exp_count:,} ({(total_validated / exp_count * 100.0) if exp_count > 0 else 100.0:.1f}%)</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #94A3B8;">Generated Datasets:</span>
                        <span style="font-weight: 700; color: #FFFFFF;">{dataset_count:,}</span>
                    </div>
                </div>
                """)
            else:
                render_html("""
                <div style="text-align: center; padding: 2.2rem 1rem; color: #94A3B8;">
                    <div style="font-size: 1.8rem; margin-bottom: 8px;">⚗️</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">No Benchmarks Recorded</div>
                    <div style="font-size: 0.8rem; line-height: 1.45;">Execute benchmarks in the Benchmark Lab to populate empirical analytics.</div>
                </div>
                """)

    # Right: Scaling Analysis Plotly Line Chart
    with sn_col2:
        with st.container(border=True):
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <div style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.04em;">
                    Input Size vs Execution Time Scaling
                </div>
                <div style="font-size: 0.74rem; color: #94A3B8;">Empirical SQLite Records</div>
            </div>
            """)

            chart_plotted = False
            if exp_count > 0:
                try:
                    with db.get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute("""
                            SELECT algorithm, input_size, AVG(avg_time) * 1000.0 as avg_ms
                            FROM experiments
                            GROUP BY algorithm, input_size
                            ORDER BY algorithm, input_size
                        """)
                        rows = cur.fetchall()

                    if rows:
                        df_chart = pd.DataFrame(rows, columns=["algorithm", "input_size", "avg_ms"])
                        unique_sizes = df_chart["input_size"].nunique()

                        if unique_sizes >= 2:
                            fig_scale = go.Figure()
                            colors_list = [COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE, COLOR_AMBER, COLOR_GREEN, COLOR_RED]

                            for idx, (algo_name, group) in enumerate(df_chart.groupby("algorithm")):
                                c = colors_list[idx % len(colors_list)]
                                fig_scale.add_trace(go.Scatter(
                                    x=group["input_size"],
                                    y=group["avg_ms"],
                                    mode="lines+markers",
                                    name=algo_name,
                                    line=dict(color=c, width=2.5),
                                    marker=dict(size=7, color=c)
                                ))

                            fig_scale.update_layout(get_plotly_layout(
                                title="",
                                height=230,
                                x_title="Input Size (N)",
                                y_title="Execution Time (ms)"
                            ))
                            fig_scale.update_layout(margin=dict(l=10, r=10, t=10, b=10))
                            st.plotly_chart(fig_scale, use_container_width=True)
                            chart_plotted = True
                except Exception:
                    pass

            if not chart_plotted:
                render_html(f"""
                <div style="text-align: center; padding: 2.2rem 1rem; color: #94A3B8;">
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                        Insufficient Multi-N Records
                    </div>
                    <div style="font-size: 0.82rem; max-width: 440px; margin: 0 auto; line-height: 1.45;">
                        Run benchmarks at multiple input sizes (e.g. N=100, N=500, N=1,000) in the Benchmark Lab or Algorithm Comparison to unlock asymptotic scaling curves.
                    </div>
                </div>
                """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 5. DATASET PERFORMANCE MATRIX (Full width)
    # ==========================================================
    section_header("Dataset Performance Matrix", icon="🧪", subtitle="Measured execution times across all 6 core sorting algorithms and 5 dataset distributions.")
    with st.container(border=True):
        algos = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort', 'Heap Sort']
        dists = ['Random', 'Sorted', 'Reverse Sorted', 'Nearly Sorted', 'Duplicate Heavy']

        matrix_data = {d: ['—'] * len(algos) for d in dists}
        try:
            with db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT algorithm, dataset, MIN(avg_time) FROM experiments WHERE category = 'Sorting' GROUP BY algorithm, dataset")
                for row in cur.fetchall():
                    a_name, d_name, b_time = row[0], row[1], row[2]
                    if a_name in algos and d_name in dists:
                        row_idx = algos.index(a_name)
                        matrix_data[d_name][row_idx] = format_time(b_time)
        except Exception:
            pass

        df_matrix = pd.DataFrame(matrix_data, index=algos)
        st.dataframe(df_matrix, use_container_width=True)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 6. ALGORITHM PARADIGM TAXONOMY (2-column grid)
    # ==========================================================
    section_header("Algorithm Paradigm Taxonomy", icon="📚", subtitle="13 Core algorithms categorized into fundamental DAA algorithm design paradigms.")
    with st.container(border=True):
        paradigms = [
            ("Divide and Conquer", "3 Algorithms", "Merge Sort, Quick Sort, Binary Search", COLOR_PURPLE),
            ("Brute Force / Exchange", "2 Algorithms", "Bubble Sort, Selection Sort", COLOR_BLUE),
            ("Greedy Method", "3 Algorithms", "Dijkstra, Prim, Kruskal", COLOR_CYAN),
            ("Graph Traversal", "2 Algorithms", "BFS, DFS", COLOR_GREEN),
            ("Heap-based / Selection", "1 Algorithm", "Heap Sort", COLOR_AMBER),
            ("Incremental / Adaptive", "1 Algorithm", "Insertion Sort", COLOR_PURPLE_LIGHT),
            ("Sequential Search", "1 Algorithm", "Linear Search", COLOR_TEXT_MUTED)
        ]

        p_cols = st.columns(2, gap="medium")
        for idx, (p_name, count_str, alg_list, color) in enumerate(paradigms):
            with p_cols[idx % 2]:
                render_html(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; transition: border-color 0.2s ease;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF;">{p_name}</span>
                        <span class="algox-badge algox-badge-purple" style="font-size: 0.70rem;">{count_str}</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 5px;">{alg_list}</div>
                </div>
                """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 7. DAA THEORETICAL INSIGHT (Full width)
    # ==========================================================
    today_idx = datetime.date.today().toordinal() % len(DAA_INSIGHTS)
    insight_title, insight_text = DAA_INSIGHTS[today_idx]

    render_html(f"""
    <div class="algox-info-card" style="border-left: 4px solid {COLOR_CYAN};">
        <div style="display: flex; align-items: flex-start; gap: 16px;">
            <div style="font-size: 38px; line-height: 1;">💡</div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 0.74rem; font-weight: 700; color: {COLOR_CYAN}; text-transform: uppercase; letter-spacing: 0.08em;">
                        DAA Theoretical Insight
                    </span>
                    <span style="font-size: 0.75rem; color: #94A3B8;">Academic Concept #{today_idx + 1} of {len(DAA_INSIGHTS)}</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                    {insight_title}
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;">
                    {insight_text}
                </div>
            </div>
        </div>
    </div>
    """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 8. RECENT BENCHMARK ACTIVITY (Full width)
    # ==========================================================
    section_header("Recent Benchmark Activity", icon="📋", subtitle="Previously executed empirical benchmark experiments and their measured results.")
    with st.container(border=True):
        recent_exps = db.get_recent_experiments(limit=8)
        if recent_exps:
            df_recent = pd.DataFrame(recent_exps)
            df_display = pd.DataFrame({
                "ID": [f"#{x['id']:03d}" for x in recent_exps],
                "Algorithm": df_recent["algorithm"],
                "Dataset": df_recent["dataset"],
                "Input Size (N)": df_recent["input_size"].apply(lambda x: f"{x:,}"),
                "Avg Time": df_recent["avg_time"].apply(lambda x: format_time(x)),
                "Comparisons": df_recent["comparisons"].apply(lambda x: f"{x:,}"),
                "Swaps / Shifts": df_recent["swaps"].apply(lambda x: f"{x:,}"),
                "Status": ["✅ Verified" if x["correct"] else "❌ Failed" for x in recent_exps],
                "Timestamp": df_recent["timestamp"]
            })
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            render_html(f"""
            <div style="text-align: center; padding: 2rem 0.5rem; color: {COLOR_TEXT_MUTED};">
                <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
                    No experiments recorded yet in SQLite.
                </div>
                <div style="font-size: 0.85rem; max-width: 400px; margin: 0 auto; line-height: 1.45;">
                    Open the Benchmark Lab to execute your first empirical algorithm experiment.
                </div>
            </div>
            """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # ==========================================================
    # 9. FOOTER
    # ==========================================================
    render_footer()
