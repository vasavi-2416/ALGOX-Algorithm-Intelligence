"""
ALGOX — About ALGOX Module
Algorithm Intelligence & Benchmarking Platform for Design and Analysis of Algorithms.
"""
import streamlit as st
from core.ui import (
    render_html,
    section_header,
    render_footer,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_TEXT_MUTED
)

def render_about(db):
    # Hero Banner
    render_html(f"""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">ℹ️</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(6,182,212,0.85);display:block;">ALGOX · ABOUT</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Algorithm Intelligence &amp; Benchmarking Platform</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
<b style="color:#F1F5F9;">ALGOX</b> is an academic platform for Design and Analysis of Algorithms — bridging theoretical Big-O analysis with empirical benchmark measurements through algorithm visualization, complexity analysis, and algorithm selection.
</p>
</div>
""")

    render_html("<div style='margin-bottom: 1.25rem;'></div>")

    # 13 Official Algorithms Scope
    section_header("Core Algorithms (13)", icon="📚", subtitle="The official 13 algorithms covered across sorting, searching, and graph theory.")
    s1, s2, s3 = st.columns(3)

    with s1:
        with st.container(border=True):
            render_html("""
            <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">
                Sorting (6)
            </div>
            <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.7; padding-left: 1.1rem; margin: 0;">
                <li><b>Bubble Sort</b> — Brute Force</li>
                <li><b>Selection Sort</b> — Brute Force</li>
                <li><b>Insertion Sort</b> — Incremental</li>
                <li><b>Merge Sort</b> — Divide and Conquer</li>
                <li><b>Quick Sort</b> — Divide and Conquer</li>
                <li><b>Heap Sort</b> — Heap-Based</li>
            </ul>
            """)

    with s2:
        with st.container(border=True):
            render_html(f"""
            <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">
                Searching (2)
            </div>
            <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.7; padding-left: 1.1rem; margin: 0;">
                <li><b>Linear Search</b> — Sequential Search</li>
                <li><b>Binary Search</b> — Divide and Conquer</li>
            </ul>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.75rem; font-style: italic;">
                Note: Binary Search requires sorted input.
            </div>
            """)

    with s3:
        with st.container(border=True):
            render_html(f"""
            <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">
                Graph Algorithms (5)
            </div>
            <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.7; padding-left: 1.1rem; margin: 0;">
                <li><b>BFS</b> — Graph Traversal</li>
                <li><b>DFS</b> — Graph Traversal</li>
                <li><b>Dijkstra's Algorithm</b> — Greedy</li>
                <li><b>Prim's Algorithm</b> — Greedy</li>
                <li><b>Kruskal's Algorithm</b> — Greedy</li>
            </ul>
            """)

    render_html("<div style='margin-bottom: 1.25rem;'></div>")

    # Technology Stack
    section_header("Technology", icon="⚙️", subtitle="Core technologies utilized in the ALGOX platform.")
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        with st.container(border=True):
            render_html("""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">🐍</div>
                <div style="font-weight: 700; color: #FFFFFF;">Python</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Algorithm Implementations</div>
            </div>
            """)

    with t2:
        with st.container(border=True):
            render_html("""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">⚡</div>
                <div style="font-weight: 700; color: #FFFFFF;">Streamlit</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Reactive User Interface</div>
            </div>
            """)

    with t3:
        with st.container(border=True):
            render_html("""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">📊</div>
                <div style="font-weight: 700; color: #FFFFFF;">Plotly</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Visual Analytics & Charts</div>
            </div>
            """)

    with t4:
        with st.container(border=True):
            render_html("""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">🗄️</div>
                <div style="font-weight: 700; color: #FFFFFF;">SQLite</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Benchmark Persistence</div>
            </div>
            """)


    # Live Algorithm Health Monitor (Real Verification of all 13 algorithms)
    section_header("Algorithmic Health & Self-Test Verification", icon="🩺", subtitle="Real-time live execution check validating all 13 algorithm implementations in ALGOX.")
    with st.container(border=True):
        from algorithms.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort
        from algorithms.searching import linear_search, binary_search
        from algorithms.graph import bfs, dfs, dijkstra, prim, kruskal, DEFAULT_GRAPH

        test_arr = [5, 2, 8, 1, 9]
        expected_sorted = [1, 2, 5, 8, 9]

        health_results = [
            ("Bubble Sort", bubble_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Selection Sort", selection_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Insertion Sort", insertion_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Merge Sort", merge_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Quick Sort", quick_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Heap Sort", heap_sort(list(test_arr))['sorted_array'] == expected_sorted),
            ("Linear Search", linear_search([10, 20, 30], 20)['found'] == True),
            ("Binary Search", binary_search([10, 20, 30], 20)['found'] == True),
            ("BFS (Graph)", len(bfs(DEFAULT_GRAPH, 'A')['traversal_order']) == 6),
            ("DFS (Graph)", len(dfs(DEFAULT_GRAPH, 'A')['traversal_order']) == 6),
            ("Dijkstra", dijkstra(DEFAULT_GRAPH, 'A')['distances']['A'] == 0),
            ("Prim (MST)", len(prim(DEFAULT_GRAPH, 'A')['mst_edges']) == 5),
            ("Kruskal (MST)", len(kruskal(DEFAULT_GRAPH)['mst_edges']) == 5)
        ]

        passed = sum(1 for _, ok in health_results if ok)

        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem;">
            <span style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF;">Implementation Diagnostic Suite</span>
            <span style="background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); color: #86EFAC; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.78rem;">
                {passed} / {len(health_results)} Verified Operational
            </span>
        </div>
        """)

        cols_diag = st.columns(3)
        for idx, (a_name, ok) in enumerate(health_results):
            with cols_diag[idx % 3]:
                status_icon = "<span style='color:#4ADE80;'>✓ PASS</span>" if ok else "<span style='color:#F87171;'>✗ FAIL</span>"
                render_html(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 6px; padding: 6px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; font-size: 0.78rem;">
                    <span style="color: #E2E8F0;">{a_name}</span>
                    <span>{status_icon}</span>
                </div>
                """)

    render_html("<div style='margin-bottom: 1.25rem;'></div>")
    render_footer()
