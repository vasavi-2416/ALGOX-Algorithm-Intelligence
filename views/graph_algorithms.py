"""
ALGOX — Graph Algorithm Laboratory Module
Full-featured interactive workbench for BFS, DFS, Dijkstra, Prim, and Kruskal.
Provides explicit algorithm tracking, dynamic source/destination configuration,
real weighted graph visualization, step-by-step playback, and dynamic result analysis.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
import math
from typing import Dict, List, Tuple, Any

from core.ui import (
    section_header,
    render_html,
    render_footer,
    get_plotly_layout,
    format_time,
    format_number,
    warning_card,
    COLOR_PURPLE,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT_MUTED
)
from algorithms.graph import (
    bfs,
    dfs,
    dijkstra,
    prim,
    kruskal,
    DEFAULT_GRAPH,
    NODE_POSITIONS
)
from core.benchmark import verify_graph_result

# Preset Topologies
SPARSE_RING_GRAPH = {
    'A': [('B', 3), ('F', 7)],
    'B': [('A', 3), ('C', 4)],
    'C': [('B', 4), ('D', 2)],
    'D': [('C', 2), ('E', 5)],
    'E': [('D', 5), ('F', 1)],
    'F': [('E', 1), ('A', 7)]
}

DENSE_MESH_GRAPH = {
    'A': [('B', 2), ('C', 4), ('D', 6)],
    'B': [('A', 2), ('C', 1), ('D', 3), ('E', 5)],
    'C': [('A', 4), ('B', 1), ('E', 2), ('F', 6)],
    'D': [('A', 6), ('B', 3), ('E', 1), ('F', 4)],
    'E': [('B', 5), ('C', 2), ('D', 1), ('F', 3)],
    'F': [('C', 6), ('D', 4), ('E', 3)]
}

TOPOLOGY_OPTIONS = {
    'Standard Weighted Benchmark (6 Nodes)': DEFAULT_GRAPH,
    'Sparse Ring Network (6 Nodes)': SPARSE_RING_GRAPH,
    'Dense Mesh Topology (6 Nodes)': DENSE_MESH_GRAPH,
    'Interactive Custom Graph': {}
}

ALGO_EXPLANATIONS = {
    'BFS': "Breadth-First Search (BFS) explores the graph level-by-level starting from the source vertex using a FIFO queue. It systematically discovers all vertices at distance k before moving to distance k+1, guaranteeing shortest path discovery on unweighted edges.",
    'DFS': "Depth-First Search (DFS) explores as deeply as possible along each branch before backtracking using recursion / a LIFO stack. It is fundamental for cycle detection, topological sorting, and discovering connected components.",
    'Dijkstra': "Dijkstra's Algorithm finds the single-source minimum-cost paths on weighted graphs with non-negative edge weights. It greedily settles the closest unvisited vertex using a min-priority queue and relaxes outgoing incident edges.",
    'Prim': "Prim's Algorithm grows a Minimum Spanning Tree (MST) starting from a root vertex by greedily adding the cheapest edge connecting the current tree to an unvisited vertex, guaranteeing a tree with total minimal weight.",
    'Kruskal': "Kruskal's Algorithm constructs an MST by sorting all edges by weight and greedily adding edges in increasing order. It utilizes Disjoint Set Union (Union-Find) to detect and reject edges that would create a cycle."
}


def _get_node_coordinates(nodes: List[str]) -> Dict[str, Tuple[float, float]]:
    """Calculates clean 2D positions for Plotly visualization."""
    base_pos = dict(NODE_POSITIONS)
    if all(n in base_pos for n in nodes) and len(nodes) == len(base_pos):
        return base_pos

    n = len(nodes)
    pos = {}
    sorted_nodes = sorted(nodes)
    for i, node in enumerate(sorted_nodes):
        if node in base_pos and len(nodes) <= len(base_pos):
            pos[node] = base_pos[node]
        else:
            angle = 2 * math.pi * i / max(1, n)
            pos[node] = (round(2.0 + 1.6 * math.cos(angle), 2), round(1.0 + 1.1 * math.sin(angle), 2))
    return pos


def render_graph_algorithms(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">🕸️</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(6,182,212,0.85);display:block;">ALGOX · GRAPH ALGORITHM LAB</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Graph Algorithms Workbench</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Interactive experimental laboratory for graph traversal (BFS, DFS), shortest path (Dijkstra), and minimum spanning tree (Prim, Kruskal) with real weighted topologies and mathematical verification.
</p>
</div>
""")

    # ── 1. ALGORITHM SELECTOR & DYNAMIC CONFIGURATION ───────────────────────────
    section_header("Graph Algorithm Configuration", icon="⚙️", subtitle="Select algorithm, customize graph topology, and configure origin/destination parameters.")

    with st.container(border=True):
        col_algo, col_topo = st.columns([1.5, 1.5], gap="medium")

        with col_algo:
            algo_choice = st.selectbox(
                "Target Graph Algorithm",
                ["BFS", "DFS", "Dijkstra", "Prim", "Kruskal"],
                index=0,
                key="glab_algo_choice"
            )

        with col_topo:
            topology_choice = st.selectbox(
                "Network Topology",
                list(TOPOLOGY_OPTIONS.keys()),
                index=0,
                key="glab_topo_choice"
            )

        # Graph source resolution
        if topology_choice == 'Interactive Custom Graph':
            if 'custom_graph' not in st.session_state:
                st.session_state['custom_graph'] = {k: list(v) for k, v in DEFAULT_GRAPH.items()}
            graph = st.session_state['custom_graph']
        else:
            graph = TOPOLOGY_OPTIONS[topology_choice]

        nodes = sorted(list(graph.keys()))
        if not nodes:
            st.error("Graph has no vertices. Please reset topology.")
            return

        # Algorithm-Specific Inputs Row
        col_in1, col_in2, col_speed = st.columns([1.2, 1.2, 1.6], gap="medium")

        with col_in1:
            if algo_choice in ("BFS", "DFS", "Prim"):
                start_node = st.selectbox("Start Node", nodes, index=0, key="glab_start_node")
                dest_node = None
            elif algo_choice == "Dijkstra":
                start_node = st.selectbox("Source Node", nodes, index=0, key="glab_dijk_start")
            else:
                st.selectbox("Execution Mode", ["Global Edge Sorting (Kruskal)"], disabled=True, key="glab_kruskal_mode")
                start_node = "A"
                dest_node = None

        with col_in2:
            if algo_choice == "Dijkstra":
                dest_default_idx = len(nodes) - 1 if len(nodes) > 1 else 0
                dest_node = st.selectbox("Destination Node", nodes, index=dest_default_idx, key="glab_dijk_dest")
            else:
                st.selectbox("Target Node", ["All Reachable Vertices"], disabled=True, key="glab_target_disabled")
                dest_node = None

        with col_speed:
            anim_speed = st.slider("Animation Step Delay (sec)", min_value=0.1, max_value=1.5, value=0.4, step=0.1, key="glab_speed_slider")

        # Interactive Graph Editor (if Custom Graph selected)
        if topology_choice == 'Interactive Custom Graph':
            with st.expander("🛠️ Interactive Graph Editor (Add/Remove Vertices & Edges)"):
                e_c1, e_c2, e_c3 = st.columns(3)
                with e_c1:
                    new_node = st.text_input("New Node Name", value="", placeholder="e.g. G", key="custom_new_node").strip().upper()
                    if st.button("Add Vertex", key="btn_add_node"):
                        if new_node and new_node not in graph:
                            graph[new_node] = []
                            st.session_state['custom_graph'] = graph
                            st.rerun()
                with e_c2:
                    if len(nodes) >= 2:
                        from_n = st.selectbox("From Node", nodes, key="custom_from_n")
                        to_n = st.selectbox("To Node", [n for n in nodes if n != from_n], key="custom_to_n")
                        edge_w = st.number_input("Edge Weight (Positive)", min_value=1, max_value=100, value=3, key="custom_edge_w")
                        if st.button("Add / Update Edge", key="btn_add_edge"):
                            # Update undirected edge
                            graph[from_n] = [(v, w) for v, w in graph.get(from_n, []) if v != to_n] + [(to_n, int(edge_w))]
                            graph[to_n] = [(v, w) for v, w in graph.get(to_n, []) if v != from_n] + [(from_n, int(edge_w))]
                            st.session_state['custom_graph'] = graph
                            st.rerun()
                with e_c3:
                    if st.button("Reset to Benchmark Graph", key="btn_reset_custom"):
                        st.session_state['custom_graph'] = {k: list(v) for k, v in DEFAULT_GRAPH.items()}
                        st.rerun()

    # ── CURRENTLY RUNNING STATUS BANNER & DYNAMIC EXPLANATION ───────────────────
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    algo_display_names = {
        'BFS': 'Breadth-First Search (BFS)',
        'DFS': 'Depth-First Search (DFS)',
        'Dijkstra': "Dijkstra's Shortest Path Algorithm",
        'Prim': "Prim's Minimum Spanning Tree Algorithm",
        'Kruskal': "Kruskal's Minimum Spanning Tree Algorithm"
    }

    render_html(f"""
    <div style="background: rgba(13, 21, 40, 0.85); border: 1px solid rgba(6, 182, 212, 0.45); box-shadow: 0 0 15px rgba(6, 182, 212, 0.15); border-radius: 10px; padding: 12px 18px; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="algox-badge algox-badge-cyan" style="font-weight: 800;">CURRENTLY RUNNING</span>
                <span style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">{algo_display_names[algo_choice]}</span>
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8;">
                {f"Source: <b style='color:#FFFFFF;'>{start_node}</b>" if algo_choice != 'Kruskal' else ""}
                {f" &bull; Destination: <b style='color:#06B6D4;'>{dest_node}</b>" if dest_node else ""}
                &bull; Vertices: <b style='color:#FFFFFF;'>{len(nodes)}</b>
            </div>
        </div>
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5;">
            {ALGO_EXPLANATIONS[algo_choice]}
        </div>
    </div>
    """)

    # ── 2. EXECUTE ALGORITHM & OBTAIN EXECUTION TRACE ───────────────────────────

    # Dijkstra validation: algorithm is undefined for negative edge weights
    if algo_choice == "Dijkstra":
        _neg_edges = [(u, v, w) for u, nbrs in graph.items() for v, w in nbrs if w < 0]
        if _neg_edges:
            st.error(
                f"⚠️ **Dijkstra's Algorithm requires non-negative edge weights.** "
                f"Found {len(_neg_edges)} negative-weight edge(s): "
                + ", ".join(f"{u}→{v} (w={w})" for u, v, w in _neg_edges[:5])
                + ". Please edit the graph to remove negative weights before running Dijkstra."
            )
            st.info("💡 For graphs with negative edges, use the Bellman-Ford algorithm (not in current ALGOX scope).")
            st.stop()

    t0 = time.perf_counter()
    if algo_choice == "BFS":
        res = bfs(graph, start_node)
    elif algo_choice == "DFS":
        res = dfs(graph, start_node)
    elif algo_choice == "Dijkstra":
        res = dijkstra(graph, start_node)
    elif algo_choice == "Prim":
        res = prim(graph, start_node)
    elif algo_choice == "Kruskal":
        res = kruskal(graph)
    exec_latency = time.perf_counter() - t0

    steps = res.get('steps', [])
    total_steps = len(steps)

    if total_steps == 0:
        st.warning("No execution trace generated for the selected graph.")
        return

    # Track step index in session state
    step_key = f"gstep_{algo_choice}_{topology_choice}_{start_node}_{dest_node}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 0

    curr_step_idx = min(st.session_state[step_key], total_steps - 1)
    curr_step = steps[curr_step_idx]

    # ── 3. VISUALIZATION CANVAS & STEP CONTROLS ─────────────────────────────────
    section_header(f"{algo_choice} Graph Visualization Canvas", icon="🎬",
                   subtitle=f"Interactive step-by-step state inspection — Step {curr_step_idx + 1} of {total_steps}.")

    # Status Pill Box
    action_type = curr_step.get('type', 'PROCESSING').upper()
    if 'accepted_edge' in curr_step:
        status_tag = "<span style='color: #4ADE80; font-weight: 700;'>ACCEPTED INTO MST</span>"
    elif 'rejected_edge' in curr_step:
        status_tag = "<span style='color: #EF4444; font-weight: 700;'>CYCLE REJECTED</span>"
    elif curr_step.get('edge'):
        status_tag = "<span style='color: #38BDF8; font-weight: 700;'>TRAVERSING EDGE</span>"
    else:
        status_tag = f"<span style='color: #F59E0B; font-weight: 700;'>{action_type}</span>"

    render_html(f"""
    <div style="background: rgba(13, 21, 40, 0.7); border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 10px; padding: 10px 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <span style="font-size: 0.85rem; font-weight: 700; color: {COLOR_CYAN};">
            STEP {curr_step_idx + 1} / {total_steps}: {status_tag}
        </span>
        <span style="font-size: 0.84rem; color: #F1F5F9; font-weight: 500;">
            {curr_step.get('description', '')}
        </span>
    </div>
    """)

    # Render Plotly Graph Canvas
    node_positions = _get_node_coordinates(nodes)
    fig = _render_graph_canvas(graph, curr_step, algo_choice, start_node, dest_node, node_positions, res)
    st.plotly_chart(fig, use_container_width=True)

    # Playback Controls Bar
    b1, b2, b3, b4, b5, b6 = st.columns([1, 1, 1, 1, 1, 1])
    with b1:
        if st.button("⏮ Start", use_container_width=True, key="glab_btn_start"):
            st.session_state['glab_playing'] = False
            st.session_state[step_key] = 0
            st.rerun()
    with b2:
        if st.button("◀ Previous", use_container_width=True, key="glab_btn_prev"):
            st.session_state['glab_playing'] = False
            if curr_step_idx > 0:
                st.session_state[step_key] = curr_step_idx - 1
                st.rerun()
    with b3:
        is_playing = st.session_state.get('glab_playing', False)
        if not is_playing:
            if st.button("▶ Auto Play", use_container_width=True, key="glab_btn_play", type="primary"):
                st.session_state['glab_playing'] = True
                if curr_step_idx >= total_steps - 1:
                    st.session_state[step_key] = 0
                st.rerun()
        else:
            if st.button("⏸ Pause", use_container_width=True, key="glab_btn_pause"):
                st.session_state['glab_playing'] = False
                st.rerun()
    with b4:
        if st.button("Next ▶", use_container_width=True, key="glab_btn_next"):
            st.session_state['glab_playing'] = False
            if curr_step_idx < total_steps - 1:
                st.session_state[step_key] = curr_step_idx + 1
                st.rerun()
    with b5:
        if st.button("⏭ Final State", use_container_width=True, key="glab_btn_final"):
            st.session_state['glab_playing'] = False
            st.session_state[step_key] = total_steps - 1
            st.rerun()
    with b6:
        if st.button("↻ Reset", use_container_width=True, key="glab_btn_reset"):
            st.session_state['glab_playing'] = False
            st.session_state[step_key] = 0
            st.rerun()

    # Step Scrubber (active when paused; progress bar during play)
    if not st.session_state.get('glab_playing', False):
        new_gstep = st.slider("Step Scrubber", min_value=1, max_value=total_steps, value=curr_step_idx + 1, key=f"scrub_{step_key}")
        if new_gstep != curr_step_idx + 1:
            st.session_state[step_key] = new_gstep - 1
            st.rerun()
    else:
        st.progress(float(curr_step_idx + 1) / float(total_steps), text=f"Auto Playing: Step {curr_step_idx + 1} / {total_steps}")
        if curr_step_idx < total_steps - 1:
            time.sleep(anim_speed)
            st.session_state[step_key] = curr_step_idx + 1
            st.rerun()
        else:
            st.session_state['glab_playing'] = False
            st.rerun()

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # ── 4. DYNAMIC ALGORITHM RESULT PANEL ───────────────────────────────────────
    section_header(f"{algo_choice} Results &amp; Correctness Verification", icon="📊",
                   subtitle="Measured performance, exact graph output metrics, and formal topological verification.")

    _render_dynamic_result_panel(algo_choice, graph, res, start_node, dest_node, exec_latency)

    render_footer()


def _render_graph_canvas(graph, curr_step, algo_choice, start_node, dest_node, pos, final_res):
    fig = go.Figure()

    # Collect active edges based on algorithm and current state
    active_mst_edges = set()
    for e in curr_step.get('mst_edges', []):
        active_mst_edges.add(tuple(sorted([e[0], e[1]])))

    # For Dijkstra shortest path highlighting
    dijkstra_path_edges = set()
    if algo_choice == "Dijkstra" and dest_node:
        path = final_res.get('paths', {}).get(dest_node, [])
        for i in range(len(path) - 1):
            dijkstra_path_edges.add(tuple(sorted([path[i], path[i+1]])))

    # For BFS / DFS tree edges discovered so far
    tree_edges = set()
    if algo_choice in ("BFS", "DFS"):
        for s in final_res.get('steps', []):
            if s.get('step_num', 0) <= curr_step.get('step_num', 0) and s.get('edge'):
                tree_edges.add(tuple(sorted([s['edge'][0], s['edge'][1]])))

    cur_edge = curr_step.get('edge') or curr_step.get('accepted_edge') or curr_step.get('rejected_edge')
    cur_edge_key = tuple(sorted([cur_edge[0], cur_edge[1]])) if cur_edge else None

    # Draw all edges
    seen_edges = set()
    for u, neighbors in graph.items():
        if u not in pos:
            continue
        x0, y0 = pos[u]
        for v, w in neighbors:
            if v not in pos:
                continue
            edge_key = tuple(sorted([u, v]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                x1, y1 = pos[v]

                # Determine edge styling
                is_cur = (edge_key == cur_edge_key)
                is_mst = (edge_key in active_mst_edges)
                is_dijk_path = (edge_key in dijkstra_path_edges)
                is_tree = (edge_key in tree_edges)
                is_rejected = ('rejected_edge' in curr_step and edge_key == cur_edge_key)

                if is_dijk_path:
                    line_color = "#F59E0B"  # Vibrant Amber for Dijkstra Path
                    line_width = 5.0
                    dash_style = 'solid'
                elif is_mst:
                    line_color = "#22C55E"  # Vibrant Green for MST
                    line_width = 5.0
                    dash_style = 'solid'
                elif is_tree:
                    line_color = "#06B6D4"  # Vibrant Cyan for Traversal Tree
                    line_width = 3.5
                    dash_style = 'solid'
                elif is_cur:
                    line_color = "#EC4899" if is_rejected else "#A855F7"
                    line_width = 4.0
                    dash_style = 'dot' if is_rejected else 'solid'
                else:
                    line_color = "rgba(100, 116, 139, 0.35)"
                    line_width = 1.5
                    dash_style = 'solid'

                fig.add_trace(go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=line_width, color=line_color, dash=dash_style),
                    hoverinfo='none',
                    showlegend=False
                ))

                # Edge weight label at midpoint with dark backdrop chip
                mid_x = (x0 + x1) / 2
                mid_y = (y0 + y1) / 2
                fig.add_trace(go.Scatter(
                    x=[mid_x],
                    y=[mid_y],
                    mode='text',
                    text=[f" {w} "],
                    textposition='middle center',
                    textfont=dict(color='#F1F5F9', size=11, family='monospace'),
                    hoverinfo='text',
                    hovertext=[f"Edge ({u} — {v}): weight {w}"],
                    showlegend=False
                ))

    # Draw all nodes
    visited_nodes = set(curr_step.get('visited', []))
    current_node = curr_step.get('current_node', None)

    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    border_colors = []
    border_widths = []

    for node in sorted(list(graph.keys())):
        if node not in pos:
            continue
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

        # Node coloring
        if node == current_node:
            node_colors.append("#F59E0B")  # Current active node
            border_colors.append("#FFFFFF")
            border_widths.append(3)
        elif node == dest_node and algo_choice == "Dijkstra":
            node_colors.append("#06B6D4")  # Destination target in Dijkstra
            border_colors.append("#FFFFFF")
            border_widths.append(3)
        elif node == start_node and algo_choice != "Kruskal":
            node_colors.append("#8B5CF6")  # Origin root
            border_colors.append("#FFFFFF")
            border_widths.append(2)
        elif node in visited_nodes:
            node_colors.append("#22C55E")  # Visited node
            border_colors.append("rgba(255,255,255,0.7)")
            border_widths.append(1.5)
        else:
            node_colors.append("#1E293B")  # Normal unvisited
            border_colors.append("rgba(148, 163, 184, 0.5)")
            border_widths.append(1.5)

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=42,
            color=node_colors,
            line=dict(color=border_colors, width=border_widths)
        ),
        text=node_text,
        textposition='middle center',
        textfont=dict(color='#FFFFFF', size=15, family='sans-serif'),
        hoverinfo='text',
        hovertext=[f"Vertex: {n}" for n in node_text],
        showlegend=False
    ))

    layout = get_plotly_layout("", height=420)
    layout['margin'] = dict(l=30, r=30, t=25, b=25)
    layout['xaxis']['showgrid'] = False
    layout['xaxis']['zeroline'] = False
    layout['xaxis']['showticklabels'] = False
    layout['yaxis']['showgrid'] = False
    layout['yaxis']['zeroline'] = False
    layout['yaxis']['showticklabels'] = False
    fig.update_layout(layout)
    return fig


def _render_dynamic_result_panel(algo, graph, res, start_node, dest_node, exec_latency):
    is_valid, verify_msg = verify_graph_result(graph, algo, res, start_node=start_node)
    badge_color = "#4ADE80" if is_valid else "#EF4444"

    # Formal Verification Status Card
    render_html(f"""
    <div style="background: rgba(13, 21, 40, 0.85); border: 1px solid {badge_color}66; border-radius: 8px; padding: 10px 16px; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div>
            <span style="font-weight: 800; font-size: 0.95rem; color: {badge_color};">
                {'✓ VERIFIED' if is_valid else '✗ VERIFICATION FAILED'}
            </span>
            <span style="font-size: 0.85rem; color: #CBD5E1; margin-left: 10px;">
                {verify_msg}
            </span>
        </div>
        <span style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">
            DAA Mathematical Guarantee
        </span>
    </div>
    """)

    # 1. BFS & DFS RESULTS
    if algo in ("BFS", "DFS"):
        order = res.get('traversal_order', [])
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>START VERTEX</div><div style='font-size:1.6rem;font-weight:800;color:#FFFFFF;'>{start_node}</div></div>")
        with c2:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>NODES VISITED</div><div style='font-size:1.6rem;font-weight:800;color:{COLOR_CYAN};'>{len(order)} of {len(graph)}</div></div>")
        with c3:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>MEASURED LATENCY</div><div style='font-size:1.6rem;font-weight:800;color:{COLOR_AMBER};'>{format_time(exec_latency)}</div></div>")

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            render_html(f"""
            <div style="padding: 4px 6px;">
                <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700; letter-spacing:0.05em; margin-bottom:8px;">COMPLETE TRAVERSAL ORDER</div>
                <div style="font-size:1.2rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;">
                    {' &nbsp;➔&nbsp; '.join([f"<span style='background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);color:#86EFAC;padding:4px 12px;border-radius:6px;'>{n}</span>" for n in order])}
                </div>
                <div style="font-size:0.82rem; color:#94A3B8;">Algorithm Data Structure: <b style="color:#FFFFFF;">{'FIFO Queue (Breadth First)' if algo == 'BFS' else 'LIFO Stack / Call Stack (Depth First)'}</b></div>
            </div>
            """)

    # 2. DIJKSTRA RESULTS
    elif algo == "Dijkstra":
        distances = res.get('distances', {})
        paths = res.get('paths', {})
        dest_cost = distances.get(dest_node, -1)
        dest_path = paths.get(dest_node, [])

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>SOURCE ➔ DESTINATION</div><div style='font-size:1.5rem;font-weight:800;color:#FFFFFF;'>{start_node} ➔ {dest_node}</div></div>")
        with c2:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>SHORTEST PATH COST</div><div style='font-size:1.5rem;font-weight:800;color:{COLOR_AMBER};'>{dest_cost if dest_cost != -1 else 'UNREACHABLE'}</div></div>")
        with c3:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>MEASURED LATENCY</div><div style='font-size:1.5rem;font-weight:800;color:{COLOR_CYAN};'>{format_time(exec_latency)}</div></div>")

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        if dest_path:
            with st.container(border=True):
                render_html(f"""
                <div style="padding: 4px 6px;">
                    <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700; letter-spacing:0.05em; margin-bottom:8px;">OPTIMAL SHORTEST PATH TO DESTINATION</div>
                    <div style="font-size:1.2rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;">
                        {' &nbsp;➔&nbsp; '.join([f"<span style='background:rgba(245,158,11,0.2);border:1px solid rgba(245,158,11,0.5);color:#FDE68A;padding:4px 12px;border-radius:6px;'>{n}</span>" for n in dest_path])}
                    </div>
                    <div style="font-size:0.82rem; color:#94A3B8;">Highlighted in bright amber on the topology canvas above.</div>
                </div>
                """)

        # Complete routing table
        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        route_rows = []
        for v in sorted(list(graph.keys())):
            route_rows.append({
                "Target Vertex": v,
                "Shortest Distance": distances.get(v, "∞"),
                "Optimal Route Path": " ➔ ".join(paths.get(v, [v])) if paths.get(v) else "Unreachable"
            })
        st.dataframe(pd.DataFrame(route_rows), use_container_width=True, hide_index=True)

    # 3. PRIM & KRUSKAL RESULTS
    elif algo in ("Prim", "Kruskal"):
        mst_edges = res.get('mst_edges', [])
        total_w = res.get('total_weight', 0)

        # Determine if result is a full spanning tree or only a spanning forest (disconnected graph)
        num_vertices = len(graph)
        is_full_spanning = len(mst_edges) >= num_vertices - 1
        span_label = "Minimum Spanning Tree" if is_full_spanning else "Minimum Spanning Forest"
        span_note = "" if is_full_spanning else " ⚠️ Graph is disconnected — result is a spanning forest, not a full MST."

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>TOTAL {span_label.upper()} WEIGHT</div><div style='font-size:1.6rem;font-weight:800;color:{COLOR_GREEN};'>{total_w}</div></div>")
        _edge_check = "(COMPLETE SPANNING TREE)" if is_full_spanning else "(SPANNING FOREST - DISCONNECTED)"
        with c2:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>EDGES SELECTED (V-1={num_vertices-1})</div><div style='font-size:1.6rem;font-weight:800;color:{COLOR_CYAN};'>{len(mst_edges)}</div><div style='font-size:0.65rem;color:#94A3B8;margin-top:2px;'>{_edge_check}</div></div>")
        with c3:
            render_html(f"<div class='algox-stat-card'><div style='font-size:0.72rem;color:#94A3B8;'>MEASURED LATENCY</div><div style='font-size:1.6rem;font-weight:800;color:{COLOR_AMBER};'>{format_time(exec_latency)}</div></div>")

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        col_t, col_r = st.columns([1.5, 1.5] if (algo == "Kruskal" and res.get('rejected_edges')) else [1, 0.001], gap="medium")

        with col_t:
            with st.container(border=True):
                render_html(f"<div style='font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700; margin-bottom:8px;'>SELECTED {span_label.upper()} EDGES{span_note}</div>")
                edge_rows = [{"Edge": f"{u} — {v}", "Edge Weight": w, "Status": "ACCEPTED"} for u, v, w in mst_edges]
                st.dataframe(pd.DataFrame(edge_rows), use_container_width=True, hide_index=True)

        if algo == "Kruskal" and res.get('rejected_edges'):
            with col_r:
                with st.container(border=True):
                    render_html("<div style='font-size:0.75rem; color:#EF4444; text-transform:uppercase; font-weight:700; margin-bottom:8px;'>REJECTED EDGES (CYCLE PREVENTION)</div>")
                    rej_rows = [{"Edge": f"{u} — {v}", "Edge Weight": w, "Reason": "Cycle Detected (DSU)"} for u, v, w in res['rejected_edges']]
                    st.dataframe(pd.DataFrame(rej_rows), use_container_width=True, hide_index=True)
