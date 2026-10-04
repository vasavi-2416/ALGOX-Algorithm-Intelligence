"""
ALGOX — Algorithm Visualizer Module
Interactive step-by-step visual execution of sorting and searching algorithms.
Provides real operation accounting, state color-coding, and granular playback controls (Play, Pause, Step).
"""
import streamlit as st
import plotly.graph_objects as go
import time
from core.ui import (
    section_header,
    render_html,
    get_plotly_layout,
    COLOR_PURPLE,
    COLOR_PURPLE_LIGHT,
    COLOR_BLUE,
    COLOR_BLUE_LIGHT,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT_MUTED
,
    render_footer
)
from core.dataset import generate_dataset, DISTRIBUTIONS
from core.steps import get_sorting_steps, get_searching_steps

# Bar color palette according to state
STATE_COLORS = {
    'normal': '#3B82F6',       # Blue
    'compare': '#F59E0B',      # Amber
    'swap': '#8B5CF6',         # Purple
    'select': '#06B6D4',       # Cyan
    'shift': '#38BDF8',        # Sky Blue
    'pivot': '#A855F7',        # Bright Purple
    'heapify': '#C084FC',      # Lavender Purple
    'sorted': '#22C55E',       # Green
    'complete': '#10B981',     # Emerald
    'inspect': '#F59E0B',      # Amber (searching)
    'found': '#22C55E',        # Green (searching)
    'eliminate': '#334155'     # Slate (eliminated interval)
}

def render_visualizer(db):
    # Check for incoming pre-selected algorithm from Library or other views
    incoming_algo = st.session_state.pop('selected_algo_name', None)
    if incoming_algo:
        if incoming_algo in ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]:
            st.session_state['viz_category'] = "Sorting"
            st.session_state['viz_sort_algo'] = incoming_algo
        elif incoming_algo in ["Linear Search", "Binary Search"]:
            st.session_state['viz_category'] = "Searching"
            st.session_state['viz_search_algo'] = incoming_algo

    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">🎬</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(139,92,246,0.85);display:block;">ALGOX · ALGORITHM VISUALIZER</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Algorithm Visualizer</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Step-by-step interactive visual execution with live comparison and swap tracking, state color-coding, and granular playback controls.
</p>
</div>
""")

    cat_default_idx = 1 if st.session_state.get('viz_category') == "Searching" else 0
    cat_col, _ = st.columns([1, 2])
    with cat_col:
        category = st.radio("Domain Mode", ["Sorting", "Searching"], index=cat_default_idx, horizontal=True, key="viz_category")

    st.markdown("<div style='border-top: 1px solid rgba(124,58,237,0.15); margin: 0.5rem 0 1.1rem 0;'></div>", unsafe_allow_html=True)

    if category == "Sorting":
        render_sorting_visualizer(db)
    else:
        render_searching_visualizer(db)


def render_sorting_visualizer(db):
    # 1. CONTROL PANEL
    c1, c2, c3, c4 = st.columns([1.5, 1.2, 1, 1.2])

    with c1:
        sort_options = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]
        cur_sort_algo = st.session_state.get('viz_sort_algo', 'Bubble Sort')
        sort_default_idx = sort_options.index(cur_sort_algo) if cur_sort_algo in sort_options else 0
        algo_name = st.selectbox(
            "Algorithm",
            sort_options,
            index=sort_default_idx,
            key="viz_sort_algo"
        )
    with c2:
        distribution = st.selectbox("Dataset Distribution", DISTRIBUTIONS, key="viz_sort_dist")
    with c3:
        array_size = st.slider("Array Size", min_value=8, max_value=32, value=14, step=2, key="viz_sort_n")
    with c4:
        use_custom = st.checkbox("Custom Array Input", key="viz_sort_custom_toggle")

    custom_arr = None
    if use_custom:
        custom_input_str = st.text_input("Comma-separated integers (e.g. 45, 12, 89, 3, 27)", value="38, 14, 52, 9, 21, 67, 4", key="viz_custom_str")
        try:
            custom_arr = [int(x.strip()) for x in custom_input_str.split(",") if x.strip()]
        except ValueError:
            st.error("Invalid custom array format. Please provide comma-separated integers.")

    # 2. ACTION CONTROLS
    action_col, speed_col = st.columns([1.5, 1.5])
    with action_col:
        if st.button("Generate Trace", use_container_width=True, key="viz_sort_gen_btn"):
            raw_data = custom_arr if custom_arr else generate_dataset(array_size, distribution)
            trace_result = get_sorting_steps(algo_name, raw_data)
            st.session_state['viz_sort_steps'] = trace_result['steps']
            st.session_state['viz_sort_step_idx'] = 0
            st.session_state['viz_sort_raw_data'] = raw_data
            st.session_state['viz_sort_active_algo'] = algo_name
            st.session_state['viz_sort_playing'] = False
            st.rerun()

    with speed_col:
        anim_speed = st.slider("Animation Speed (sec)", min_value=0.05, max_value=1.0, value=0.25, step=0.05, key="viz_anim_speed")

    # Ensure steps exist
    if 'viz_sort_steps' not in st.session_state or st.session_state.get('viz_sort_active_algo') != algo_name:
        raw_data = custom_arr if custom_arr else generate_dataset(array_size, distribution, seed=42)
        trace_result = get_sorting_steps(algo_name, raw_data)
        st.session_state['viz_sort_steps'] = trace_result['steps']
        st.session_state['viz_sort_step_idx'] = 0
        st.session_state['viz_sort_raw_data'] = raw_data
        st.session_state['viz_sort_active_algo'] = algo_name
        st.session_state['viz_sort_playing'] = False

    steps = st.session_state['viz_sort_steps']
    total_steps = len(steps)
    curr_idx = min(st.session_state.get('viz_sort_step_idx', 0), total_steps - 1)
    curr_step = steps[curr_idx]

    # 3. METRIC CARDS (.algox-stat-card)
    comparisons_so_far = sum(1 for s in steps[:curr_idx + 1] if s.get('type') == 'compare')
    swaps_so_far = sum(1 for s in steps[:curr_idx + 1] if s.get('type') in ('swap', 'shift'))

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">CURRENT STEP</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#06B6D4; white-space:nowrap;">{curr_idx + 1} / {total_steps}</div>
        </div>
        """)
    with m2:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">COMPARISONS</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#F59E0B; white-space:nowrap;">{comparisons_so_far}</div>
        </div>
        """)
    with m3:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">SWAPS / SHIFTS</div>
            <div class="algox-stat-value" style="font-size:1.55rem; font-weight:800; color:#8B5CF6; white-space:nowrap;">{swaps_so_far}</div>
        </div>
        """)
    with m4:
        action_state = curr_step.get('type', 'running')
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">ACTION STATE</div>
            <div class="algox-stat-value" style="font-size:1.35rem; font-weight:800; color:#FFFFFF; text-transform:uppercase; white-space:nowrap;">{action_state}</div>
        </div>
        """)

    # 4. STEP INFORMATION BANNER
    desc_msg = curr_step.get('description', '')
    render_html(f"<div style='background: rgba(16,22,45,0.7); border-left: 4px solid {COLOR_PURPLE}; border-radius: 6px; padding: 0.75rem 1rem; margin: 0.25rem 0 0.85rem 0;'><span style='font-size: 0.75rem; color: {COLOR_PURPLE_LIGHT}; font-weight: 700; text-transform: uppercase; margin-right: 0.5rem;'>LOG TRACE:</span><span style='font-size: 0.92rem; font-weight: 600; color: #F1F5F9;'>{desc_msg}</span></div>")

    # 4b. RIGOROUS ALGORITHMIC STATE TELEMETRY (Phase 6 Specs)
    tel_items = []
    if algo_name == "Bubble Sort":
        pass_no = curr_step.get('pass_number', 1)
        tel_items.append(("PASS NUMBER", f"Pass {pass_no}"))
        if curr_step.get('compared_elements'):
            tel_items.append(("COMPARED ELEMENTS", f"{curr_step['compared_elements'][0]} vs {curr_step['compared_elements'][1]}"))
        s_reg = curr_step.get('sorted_region', [])
        tel_items.append(("SORTED REGION", f"Indices {s_reg}" if s_reg else "None yet"))
    elif algo_name == "Selection Sort":
        tel_items.append(("CURRENT INDEX", f"i = {curr_step.get('current_index', 0)}"))
        tel_items.append(("CURRENT MINIMUM", f"Min Idx: {curr_step.get('current_minimum', 0)}"))
        if curr_step.get('scanned_element') is not None:
            tel_items.append(("SCANNED ELEMENT", f"Idx: {curr_step.get('scanned_element')}"))
        s_reg = curr_step.get('sorted_region', [])
        tel_items.append(("SORTED REGION", f"[0..{len(s_reg)-1}]" if s_reg else "None yet"))
    elif algo_name == "Insertion Sort":
        if curr_step.get('key_element') is not None:
            tel_items.append(("KEY ELEMENT", f"{curr_step.get('key_element')} (idx {curr_step.get('key_index')})"))
        if curr_step.get('compared_index') is not None:
            tel_items.append(("COMPARED INDEX", f"A[{curr_step.get('compared_index')}]"))
        tel_items.append(("SHIFTING STATUS", "Active Shift" if curr_step.get('shifting') else "In Place"))
        s_pref = curr_step.get('sorted_prefix', [])
        tel_items.append(("SORTED PREFIX", f"[0..{len(s_pref)-1}]" if s_pref else "[0]"))
    elif algo_name == "Merge Sort":
        l_rng = curr_step.get('left_range', [])
        r_rng = curr_step.get('right_range', [])
        m_rng = curr_step.get('merged_range', [])
        tel_items.append(("LEFT RANGE", f"[{l_rng[0]}..{l_rng[1]}]" if len(l_rng) == 2 else "—"))
        tel_items.append(("RIGHT RANGE", f"[{r_rng[0]}..{r_rng[1]}]" if len(r_rng) == 2 else "—"))
        tel_items.append(("MERGED REGION", f"[{m_rng[0]}..{m_rng[1]}]" if len(m_rng) == 2 else "In Progress"))
    elif algo_name == "Quick Sort":
        p_val = curr_step.get('pivot')
        tel_items.append(("PIVOT ELEMENT", f"{p_val}" if p_val is not None else "—"))
        tel_items.append(("LEFT POINTER (i)", f"{curr_step.get('left_pointer', '—')}"))
        tel_items.append(("RIGHT POINTER (j)", f"{curr_step.get('right_pointer', '—')}"))
        r_rng = curr_step.get('recursive_range', [])
        tel_items.append(("ACTIVE RANGE", f"[{r_rng[0]}..{r_rng[1]}]" if len(r_rng) == 2 else "—"))
    elif algo_name == "Heap Sort":
        tel_items.append(("PHASE", "Build Max-Heap" if curr_step.get('heap_construction') else "Root Extraction"))
        if curr_step.get('parent_index') is not None:
            tel_items.append(("PARENT / CHILD", f"P: {curr_step.get('parent_index')} &bull; C: {curr_step.get('child_index')}"))
        tel_items.append(("ACTIVE HEAP SIZE", f"{curr_step.get('heap_size', 0)} elements"))
        s_reg = curr_step.get('sorted_region', [])
        tel_items.append(("SORTED TAIL", f"{len(s_reg)} locked" if s_reg else "0 locked"))

    if tel_items:
        t_cols = st.columns(len(tel_items))
        for col, (t_label, t_val) in zip(t_cols, tel_items):
            with col:
                render_html(f"""
                <div style="background: rgba(14,20,48,0.55); border: 1px solid rgba(139,92,246,0.22); border-radius: 8px; padding: 6px 10px; text-align: center; margin-bottom: 0.75rem;">
                    <div style="font-size: 0.65rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">{t_label}</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #67E8F9; margin-top: 2px;">{t_val}</div>
                </div>
                """)

    # 5. ARRAY VISUALIZATION
    chart_placeholder = st.empty()

    def draw_chart(step):
        arr_state = step['array_state']
        step_type = step.get('type', 'normal')
        active_indices = step.get('indices', [])

        bar_colors = []
        for i in range(len(arr_state)):
            if step_type == 'complete':
                bar_colors.append(STATE_COLORS['complete'])
            elif i in active_indices:
                bar_colors.append(STATE_COLORS.get(step_type, COLOR_PURPLE_LIGHT))
            else:
                bar_colors.append(STATE_COLORS['normal'])

        fig = go.Figure(data=[
            go.Bar(
                x=[f"[{i}]" for i in range(len(arr_state))],
                y=arr_state,
                marker=dict(
                    color=bar_colors,
                    line=dict(color="rgba(255,255,255,0.2)", width=1.5)
                ),
                text=arr_state,
                textposition='outside',
                textfont=dict(color="#FFFFFF", size=12, family="monospace"),
                hoverinfo="x+y"
            )
        ])

        y_max = max(arr_state) if arr_state else 100
        fig.update_layout(
            get_plotly_layout(
                title=f"{algo_name} — Step {curr_idx + 1} of {total_steps}",
                height=340,
                x_title="Array Index",
                y_title="Value"
            ),
            yaxis=dict(range=[0, int(y_max * 1.25)]),
            bargap=0.25
        )
        return fig

    chart_placeholder.plotly_chart(draw_chart(curr_step), use_container_width=True)

    # 6. PLAYBACK CONTROLS
    ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([1, 1, 1, 1, 1])

    with ctrl1:
        if st.button("Previous", use_container_width=True, key="btn_prev_step"):
            st.session_state['viz_sort_playing'] = False
            if curr_idx > 0:
                st.session_state['viz_sort_step_idx'] = curr_idx - 1
                st.rerun()

    with ctrl2:
        is_playing = st.session_state.get('viz_sort_playing', False)
        if not is_playing:
            if st.button("Play", use_container_width=True, key="btn_play_step"):
                st.session_state['viz_sort_playing'] = True
                if curr_idx >= total_steps - 1:
                    st.session_state['viz_sort_step_idx'] = 0
                st.rerun()
        else:
            if st.button("Pause", use_container_width=True, key="btn_pause_step"):
                st.session_state['viz_sort_playing'] = False
                st.rerun()

    with ctrl3:
        if st.button("Next", use_container_width=True, key="btn_next_step"):
            st.session_state['viz_sort_playing'] = False
            if curr_idx < total_steps - 1:
                st.session_state['viz_sort_step_idx'] = curr_idx + 1
                st.rerun()

    with ctrl4:
        if st.button("Reset", use_container_width=True, key="btn_reset_step"):
            st.session_state['viz_sort_playing'] = False
            st.session_state['viz_sort_step_idx'] = 0
            st.rerun()

    with ctrl5:
        if st.button("Show Final State", use_container_width=True, key="btn_last_step"):
            st.session_state['viz_sort_playing'] = False
            st.session_state['viz_sort_step_idx'] = total_steps - 1
            st.rerun()

    # Step Scrubbing Slider — only active when NOT playing
    if not st.session_state.get('viz_sort_playing', False):
        new_step_slider = st.slider(
            "Step Scrubber",
            min_value=1,
            max_value=total_steps,
            value=curr_idx + 1,
            key="viz_sort_slider_ctrl"
        )
        if new_step_slider != curr_idx + 1:
            st.session_state['viz_sort_step_idx'] = new_step_slider - 1
            st.rerun()
    else:
        st.progress(float(curr_idx + 1) / float(total_steps), text=f"Step {curr_idx + 1} / {total_steps}")

    # If playing, auto-advance to next step
    if st.session_state.get('viz_sort_playing', False):
        if curr_idx < total_steps - 1:
            time.sleep(anim_speed)
            st.session_state['viz_sort_step_idx'] = curr_idx + 1
            st.rerun()
        else:
            st.session_state['viz_sort_playing'] = False
            st.rerun()

    # 7. FINAL ANALYSIS & CORRECTNESS VERIFICATION (When at final step)
    if curr_idx >= total_steps - 1:
        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            final_arr = curr_step.get('array_state', [])
            is_sorted = (final_arr == sorted(final_arr))
            status_badge = "<span style='color: #4ADE80; font-weight: 700;'>✅ Verification Passed (Ascending Order Confirmed)</span>" if is_sorted else "<span style='color: #EF4444; font-weight: 700;'>❌ Order Mismatch</span>"

            render_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.65rem;">
                <div style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF;">Execution Trace Analysis — {algo_name}</div>
                <div>{status_badge}</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1rem;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">TOTAL STEPS</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {COLOR_CYAN};">{total_steps:,}</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">TOTAL COMPARISONS</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {COLOR_AMBER};">{comparisons_so_far:,}</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">TOTAL SWAPS / SHIFTS</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {COLOR_PURPLE_LIGHT};">{swaps_so_far:,}</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">FINAL ARRAY SIZE</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {COLOR_GREEN};">{len(final_arr)} elements</div>
                </div>
            </div>
            """)

            fin_c1, fin_c2 = st.columns(2)
            with fin_c1:
                if st.button("Run Empirical Benchmark on this Algorithm", key="viz_fin_bench", use_container_width=True):
                    st.session_state['current_page'] = 'Benchmark Lab'
                    st.session_state['selected_benchmark_algo'] = algo_name
                    st.rerun()
            with fin_c2:
                if st.button("Compare with Alternative Sorting Algorithms", key="viz_fin_comp", use_container_width=True):
                    st.session_state['current_page'] = 'Comparison'
                    st.rerun()


def render_searching_visualizer(db):
    search_options = ["Linear Search", "Binary Search"]
    cur_search_algo = st.session_state.get('viz_search_algo', 'Linear Search')
    search_default_idx = search_options.index(cur_search_algo) if cur_search_algo in search_options else 0

    c1, c2, c3 = st.columns([1.5, 1, 1.2])
    with c1:
        search_algo = st.selectbox("Searching Algorithm", search_options, index=search_default_idx, key="viz_search_algo")
    with c2:
        search_n = st.slider("Array Size", min_value=10, max_value=32, value=16, step=2, key="viz_search_n")
    with c3:
        target_mode = st.radio("Target Presence", ["Present Target", "Custom Target"], horizontal=True, key="viz_search_tgt_mode")

    # Dataset generation & Invariant Validation (Binary Search MUST operate on sorted data)
    if search_algo == "Binary Search":
        search_arr = sorted(generate_dataset(search_n, "Random", seed=100))
        st.info("ℹ️ Binary Search requires monotonically sorted input. Dataset verified and sorted in non-decreasing order.")
    else:
        search_arr = generate_dataset(search_n, "Random", seed=100)

    if target_mode == "Present Target":
        target_val = search_arr[len(search_arr) // 2]
        st.markdown(f"<div style='font-size: 0.82rem; color: {COLOR_CYAN}; margin-bottom: 0.5rem;'>Pre-selected target value from array: <b>{target_val}</b></div>", unsafe_allow_html=True)
    else:
        target_val = st.number_input("Target Search Key", value=int(search_arr[len(search_arr) // 2]), key="viz_search_custom_val")

    gen_col, speed_col = st.columns([1.5, 1.5])
    with gen_col:
        if st.button("🔄 GENERATE SEARCH TRACE", use_container_width=True, key="viz_search_gen_btn"):
            trace = get_searching_steps(search_algo, search_arr, int(target_val))
            st.session_state['viz_search_steps'] = trace['steps']
            st.session_state['viz_search_step_idx'] = 0
            st.session_state['viz_search_found'] = trace.get('found', False)
            st.session_state['viz_search_target'] = target_val
            st.session_state['viz_search_arr'] = search_arr
            st.rerun()

    with speed_col:
        search_anim_speed = st.slider("Animation Speed (sec)", min_value=0.05, max_value=1.0, value=0.3, step=0.05, key="viz_search_anim_speed")

    # Auto-generate if absent
    if 'viz_search_steps' not in st.session_state or st.session_state.get('viz_search_active_algo') != search_algo:
        trace = get_searching_steps(search_algo, search_arr, int(target_val))
        st.session_state['viz_search_steps'] = trace['steps']
        st.session_state['viz_search_step_idx'] = 0
        st.session_state['viz_search_found'] = trace.get('found', False)
        st.session_state['viz_search_target'] = target_val
        st.session_state['viz_search_active_algo'] = search_algo
        st.session_state['viz_search_arr'] = search_arr

    steps = st.session_state['viz_search_steps']
    total_steps = len(steps)
    curr_idx = min(st.session_state.get('viz_search_step_idx', 0), total_steps - 1)
    curr_step = steps[curr_idx]

    # Real comparisons count from execution step
    comps_so_far = curr_step.get('comparisons', curr_idx + 1)
    found_status = "FOUND" if (curr_step.get('type') == 'found' or curr_step.get('found')) else ("SEARCHING" if curr_idx < total_steps - 1 else ("NOT FOUND" if not st.session_state.get('viz_search_found') else "COMPLETE"))
    status_color = COLOR_GREEN if found_status == 'FOUND' else (COLOR_CYAN if found_status == 'SEARCHING' else COLOR_AMBER)

    # 4 Real Metric Tiles
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        render_html(f"""
        <div class="algox-glass-card" style="padding: 0.75rem; text-align: center; margin-bottom: 0.5rem;">
            <div style="font-size: 0.75rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;">CURRENT STEP</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: {COLOR_CYAN};">{curr_idx + 1} / {total_steps}</div>
        </div>
        """)
    with s_col2:
        render_html(f"""
        <div class="algox-glass-card" style="padding: 0.75rem; text-align: center; margin-bottom: 0.5rem;">
            <div style="font-size: 0.75rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;">TARGET KEY</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: {COLOR_AMBER};">{target_val}</div>
        </div>
        """)
    with s_col3:
        render_html(f"""
        <div class="algox-glass-card" style="padding: 0.75rem; text-align: center; margin-bottom: 0.5rem;">
            <div style="font-size: 0.75rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;">COMPARISONS COUNT</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: {COLOR_PURPLE_LIGHT};">{comps_so_far}</div>
        </div>
        """)
    with s_col4:
        render_html(f"""
        <div class="algox-glass-card" style="padding: 0.75rem; text-align: center; margin-bottom: 0.5rem;">
            <div style="font-size: 0.75rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;">SEARCH RESULT</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: {status_color};">{found_status}</div>
        </div>
        """)

    # Granular Search Telemetry (Phase 7 Specs)
    if search_algo == "Linear Search":
        c_idx = curr_step.get('current_index')
        c_val = curr_step.get('current_value')
        comp_str = curr_step.get('comparison', '—')
        f_idx = curr_step.get('final_index', '—')
        ls_cols = st.columns(4)
        with ls_cols[0]:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.70rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>CURRENT INDEX</div><div style='font-size: 1.1rem; font-weight: 800; color: {COLOR_CYAN};'>{c_idx if c_idx is not None else '—'}</div></div>")
        with ls_cols[1]:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.70rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>CURRENT VALUE</div><div style='font-size: 1.1rem; font-weight: 800; color: {COLOR_AMBER};'>{c_val if c_val is not None else '—'}</div></div>")
        with ls_cols[2]:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.70rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>COMPARISON</div><div style='font-size: 0.88rem; font-weight: 700; color: #FFFFFF; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{comp_str}</div></div>")
        with ls_cols[3]:
            with st.container(border=True):
                final_str = f"Index {f_idx}" if (f_idx is not None and f_idx != -1 and f_idx != '—') else ("Not Found" if f_idx == -1 else "Scanning...")
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.70rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>FINAL RESULT</div><div style='font-size: 1.05rem; font-weight: 800; color: {status_color};'>{final_str}</div></div>")
    else:
        # Binary Search Interval bound tracking
        low_idx = curr_step.get('low', 0)
        mid_idx = curr_step.get('mid', 0)
        high_idx = curr_step.get('high', len(search_arr) - 1)

        low_disp = f"Index {low_idx} ({search_arr[low_idx]})" if 0 <= low_idx < len(search_arr) else "Out of bounds"
        mid_disp = f"Index {mid_idx} ({search_arr[mid_idx]})" if 0 <= mid_idx < len(search_arr) else "—"
        high_disp = f"Index {high_idx} ({search_arr[high_idx]})" if 0 <= high_idx < len(search_arr) else "Out of bounds"
        low_val = search_arr[low_idx] if 0 <= low_idx < len(search_arr) else "—"
        high_val = search_arr[high_idx] if 0 <= high_idx < len(search_arr) else "—"

        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.72rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>LOW BOUND</div><div style='font-size: 1.15rem; font-weight: 800; color: {COLOR_CYAN}; margin-top: 2px;'>{low_disp}</div></div>")
        with b_col2:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.72rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>MIDPOINT</div><div style='font-size: 1.15rem; font-weight: 800; color: {COLOR_AMBER}; margin-top: 2px;'>{mid_disp}</div></div>")
        with b_col3:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.72rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>HIGH BOUND</div><div style='font-size: 1.15rem; font-weight: 800; color: {COLOR_PURPLE_LIGHT}; margin-top: 2px;'>{high_disp}</div></div>")
        with b_col4:
            with st.container(border=True):
                render_html(f"<div style='text-align: center;'><div style='font-size: 0.72rem; color: {COLOR_TEXT_MUTED}; font-weight: 700;'>ACTIVE INTERVAL</div><div style='font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-top: 2px;'>[{low_val} .. {high_val}]</div></div>")

    # Step description banner
    sdesc = curr_step.get('description', '')
    render_html(f"<div style='background: rgba(16,22,45,0.7); border-left: 4px solid {COLOR_CYAN}; border-radius: 6px; padding: 0.75rem 1rem; margin: 0.25rem 0 0.85rem 0;'><span style='font-size: 0.75rem; color: {COLOR_CYAN}; font-weight: 700; text-transform: uppercase; margin-right: 0.5rem;'>STEP {curr_idx + 1}/{total_steps}:</span><span style='font-size: 0.92rem; font-weight: 600; color: #F1F5F9;'>{sdesc}</span></div>")

    # Searching chart
    search_placeholder = st.empty()

    def draw_search_chart(step):
        arr_state = step.get('array_state', search_arr)
        step_type = step.get('type', 'inspect')
        if search_algo == "Linear Search":
            active_idx = step.get('current_index')
            if active_idx is None:
                active_idx = step.get('indices', [-1])[0] if step.get('indices') else -1
        else:
            active_idx = step.get('mid', -1)

        bar_colors = []
        for i in range(len(arr_state)):
            if search_algo == "Binary Search":
                low = step.get('low', 0)
                high = step.get('high', len(arr_state) - 1)
                if i < low or i > high:
                    bar_colors.append(STATE_COLORS['eliminate'])
                elif i == active_idx:
                    bar_colors.append(STATE_COLORS['found'] if (step_type == 'found' or step.get('found')) else STATE_COLORS['inspect'])
                else:
                    bar_colors.append(STATE_COLORS['normal'])
            else:
                if i == active_idx:
                    bar_colors.append(STATE_COLORS['found'] if (step_type == 'found' or step.get('found')) else STATE_COLORS['inspect'])
                elif active_idx != -1 and i < active_idx:
                    bar_colors.append(STATE_COLORS['eliminate'])
                else:
                    bar_colors.append(STATE_COLORS['normal'])

        fig = go.Figure(data=[
            go.Bar(
                x=[f"[{i}]" for i in range(len(arr_state))],
                y=arr_state,
                marker=dict(
                    color=bar_colors,
                    line=dict(color="rgba(255,255,255,0.2)", width=1.5)
                ),
                text=arr_state,
                textposition='outside',
                textfont=dict(color="#FFFFFF", size=12, family="monospace"),
                hoverinfo="x+y"
            )
        ])

        y_max = max(arr_state) if arr_state else 100
        fig.update_layout(
            get_plotly_layout(
                title=f"{search_algo} — Target: {target_val} (Step {curr_idx + 1}/{total_steps})",
                height=340,
                x_title="Array Index",
                y_title="Value"
            ),
            yaxis=dict(range=[0, int(y_max * 1.25)]),
            bargap=0.25
        )
        return fig

    search_placeholder.plotly_chart(draw_search_chart(curr_step), use_container_width=True)

    # Search playback
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        if st.button("⏮ Previous Step", use_container_width=True, key="btn_search_prev"):
            if curr_idx > 0:
                st.session_state['viz_search_step_idx'] = curr_idx - 1
                st.rerun()
    with sc2:
        if st.button("⏭ Next Step", use_container_width=True, key="btn_search_next"):
            if curr_idx < total_steps - 1:
                st.session_state['viz_search_step_idx'] = curr_idx + 1
                st.rerun()
    with sc3:
        if st.button("↻ Reset Search", use_container_width=True, key="btn_search_reset"):
            st.session_state['viz_search_step_idx'] = 0
            st.rerun()
    with sc4:
        if st.button("⏩ Fast Forward", use_container_width=True, key="btn_search_end"):
            st.session_state['viz_search_step_idx'] = total_steps - 1
            st.rerun()

    render_footer()
