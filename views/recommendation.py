"""
ALGOX — Algorithm Recommendation Module
Select a suitable algorithm based on problem requirements and input characteristics.
"""
import streamlit as st
from core.ui import (
    section_header,
    render_html,
    empty_state,
    complexity_badge,
    render_footer,
    COLOR_PURPLE,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_TEXT_MUTED
)
from core.recommendation import get_recommendation
from core.dataset import DISTRIBUTIONS
from core.complexity import ALGORITHM_COMPLEXITY

def render_recommendation(db):
    # Hero Banner
    # Auto-initialize recommendation if None so right panel is immediately active and informative
    if 'active_recommendation' not in st.session_state:
        st.session_state['active_recommendation'] = get_recommendation(
            'Sorting', 2500, 'Random',
            {'in_place': False, 'stable': False, 'nearly_sorted': False, 'heavy_duplicates': False, 'is_sorted': False, 'priority': 'Balanced'},
            priority='Balanced'
        )

    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">🤖</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(6,182,212,0.85);display:block;">ALGOX · RECOMMENDATION ENGINE</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Algorithm Recommendation Engine</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Explainable rule-based algorithm selection — pure algorithmic reasoning, not machine learning. Specify domain constraints and receive formal justification.
</p>
</div>
""")

    left_col, right_col = st.columns([1, 1], gap="large")

    # LEFT COLUMN: Problem Requirements
    with left_col:
        section_header("Problem Requirements", icon="⚙️", subtitle="Specify domain, dataset distribution, input size, and constraints.")

        with st.container(border=True):
            problem_type = st.selectbox("Problem Type", ["Sorting", "Searching"], key="rec_prob_type")
            distribution = st.selectbox("Dataset Distribution", DISTRIBUTIONS, index=0, key="rec_dist")
            input_size = st.number_input("Input Size (N)", min_value=5, max_value=1_000_000, value=2500, step=500, key="rec_input_size")
            priority = st.selectbox("Primary Optimization Priority", ["Balanced", "Speed (Throughput)", "Memory (O(1) Auxiliary)", "Stability (Preserve Order)", "Simplicity (Low Overhead)", "Worst-Case Guarantee"], index=0, key="rec_priority")

            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #FFFFFF; margin: 0.85rem 0 0.4rem 0;'>Constraints & Properties:</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                req_in_place = st.checkbox("Memory Constraint (In-Place)", key="rec_c_inplace")
                req_nearly_sorted = st.checkbox("Nearly Sorted Input", key="rec_c_nearly_sorted")
            with c2:
                req_stable = st.checkbox("Stable Ordering Required", key="rec_c_stable")
                req_duplicates = st.checkbox("Duplicate Values Present", key="rec_c_duplicates")

            st.markdown("<div style='margin-top: 1.1rem;'></div>", unsafe_allow_html=True)
            deduce_clicked = st.button("⚡ GENERATE RECOMMENDATION", use_container_width=True, key="rec_btn_generate", type="primary")

        if deduce_clicked:
            p_key = priority.split(' ')[0]
            constraints = {
                'in_place': req_in_place,
                'stable': req_stable,
                'nearly_sorted': req_nearly_sorted,
                'heavy_duplicates': req_duplicates,
                'is_sorted': (distribution == 'Sorted'),
                'priority': p_key
            }
            rec = get_recommendation(problem_type, input_size, distribution, constraints, priority=p_key)
            st.session_state['active_recommendation'] = rec
            db.increment_recommendations_count()
            st.rerun()

    # RIGHT COLUMN: Algorithm Recommendation
    with right_col:
        section_header("Algorithm Recommendation", icon="💡", subtitle="Recommended algorithm based on specified problem requirements.")

        rec = st.session_state.get('active_recommendation')
        if rec:
            algo_meta = ALGORITHM_COMPLEXITY.get(rec['recommended'], {})

            with st.container(border=True):
                reasons_li = "".join(f"<li>{r}</li>" for r in rec.get('reasons', []))
                render_html(f"""
                <div style="padding: 2px 2px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <span style="font-size: 0.74rem; background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); color: #86EFAC; font-weight: 700; padding: 3px 8px; border-radius: 6px;">
                            Recommended Candidate
                        </span>
                        <span style="font-size: 0.8rem; color: #93C5FD; font-weight: 600;">
                            {rec.get('paradigm', '')}
                        </span>
                    </div>
                    <h2 style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; margin: 0 0 0.5rem 0;">
                        {rec['recommended']}
                    </h2>
                    <div style="display: flex; gap: 0.4rem; margin-bottom: 0.85rem; flex-wrap: wrap;">
                        {complexity_badge(algo_meta.get('best', 'O(1)'))}
                        {complexity_badge(algo_meta.get('average', 'O(n)'))}
                        {complexity_badge(algo_meta.get('worst', 'O(n²)'))}
                        {complexity_badge(algo_meta.get('space', 'O(1)'))}
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.35rem;">Algorithmic Justification:</div>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #CBD5E1; font-size: 0.85rem; line-height: 1.6;">
                        {reasons_li}
                    </ul>
                </div>
                """)

            # Quick action buttons inside right column header
            rec_c1, rec_c2 = st.columns(2, gap="medium")
            with rec_c1:
                if st.button("🔬 Test in Benchmark Lab", key="rec_act_bench", use_container_width=True):
                    st.session_state['current_page'] = 'Benchmark Lab'
                    st.session_state['selected_benchmark_algo'] = rec['recommended']
                    st.rerun()
            with rec_c2:
                if st.button("🎬 Observe in Visualizer", key="rec_act_viz", use_container_width=True):
                    st.session_state['current_page'] = 'Visualizer'
                    st.rerun()
        else:
            with st.container(border=True):
                render_html("""
                <div style="text-align: center; padding: 2.5rem 1rem;">
                    <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">💡</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">Awaiting Problem Parameters</div>
                    <div style="color: #94A3B8; font-size: 0.86rem; margin: 0.4rem auto 0 auto; max-width: 360px; line-height: 1.5;">
                        Configure your domain requirements on the left and click <b>GENERATE RECOMMENDATION</b> to obtain formal algorithmic reasoning.
                    </div>
                </div>
                """)

    # BELOW THE 2 COLUMNS: FULL WIDTH SECTIONS (As explicitly instructed)
    rec = st.session_state.get('active_recommendation')
    if rec:
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        # FULL WIDTH: Architectural Trade-offs
        if rec.get('trade_off'):
            section_header("Architectural Trade-offs", icon="⚖️", subtitle="Asymptotic compromises and engineering implications of this selection.")
            with st.container(border=True):
                render_html(f"""
                <div style="padding: 4px 6px;">
                    <div style="font-size: 0.86rem; color: #CBD5E1; line-height: 1.6;">
                        {rec['trade_off']}
                    </div>
                </div>
                """)

        # FULL WIDTH: Alternative Algorithms
        if rec.get('alternatives'):
            st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
            section_header("Alternative Candidate Algorithms", icon="🔄", subtitle="Secondary options that satisfy subsets of constraints or alternative trade-offs.")
            with st.container(border=True):
                alt_cols = st.columns(len(rec['alternatives']), gap="medium") if len(rec['alternatives']) <= 4 else st.columns(3, gap="medium")
                for idx, alt in enumerate(rec['alternatives']):
                    col_idx = idx % len(alt_cols)
                    with alt_cols[col_idx]:
                        render_html(f"""
                        <div style="background: rgba(10, 18, 45, 0.68); border: 1px solid rgba(6, 182, 212, 0.35); box-shadow: 0 4px 18px rgba(0,0,0,0.32), 0 0 12px rgba(6, 182, 212, 0.16); border-radius: 10px; padding: 12px 14px; height: 100%;">
                            <div style="font-size: 0.95rem; font-weight: 700; color: #38BDF8; margin-bottom: 4px;">{alt.get('name', '')}</div>
                            <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.45;">{alt.get('reason', '')}</div>
                        </div>
                        """)

    render_footer()
