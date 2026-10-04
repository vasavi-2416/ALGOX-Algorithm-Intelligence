"""
ALGOX — Algorithm Library Module
Comprehensive academic catalog covering all 13 core algorithms, design paradigms,
asymptotic complexities, implementation properties, and deep-dive technical taxonomy.
"""
import streamlit as st
from core.complexity import ALGORITHM_COMPLEXITY
from core.ui import (
    complexity_badge,
    render_html,
    section_header,
    render_footer,
    COLOR_PURPLE,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_AMBER,
    COLOR_RED,
    COLOR_TEXT,
    COLOR_TEXT_MUTED
)

CATEGORY_COLORS = {
    'Sorting': COLOR_PURPLE,
    'Searching': COLOR_BLUE,
    'Graph': COLOR_CYAN
}

def render_algorithms(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">📚</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(139,92,246,0.85);display:block;">ALGOX · ALGORITHM LIBRARY</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Algorithm Catalog &amp; Library</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Comprehensive academic catalog covering all 13 core algorithms — design paradigms, asymptotic complexities, implementation properties, and technical taxonomy.
</p>
</div>
""")

    # Pre-populate filter from session state if set by dashboard click
    default_cat_idx = 0
    if 'algo_filter_category' in st.session_state:
        cat_val = st.session_state.pop('algo_filter_category')
        cat_list = ['All', 'Sorting', 'Searching', 'Graph']
        if cat_val in cat_list:
            default_cat_idx = cat_list.index(cat_val)

    # 1. Search and Filter Toolbar
    with st.container(border=True):
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])

        with f_col1:
            search_query = st.text_input(
                "Search algorithms, paradigms, or properties...",
                placeholder="e.g. Quick Sort, Divide and Conquer, Greedy, In-place...",
                key="algo_lib_search"
            )

        with f_col2:
            category_options = ["All", "Sorting", "Searching", "Graph"]
            selected_category = st.selectbox("Category Filter", category_options, index=default_cat_idx, key="algo_lib_cat")

        with f_col3:
            all_paradigms = sorted(list(set(info['paradigm'] for info in ALGORITHM_COMPLEXITY.values())))
            paradigm_options = ["All"] + all_paradigms
            selected_paradigm = st.selectbox("Paradigm Filter", paradigm_options, index=0, key="algo_lib_paradigm")

    # 2. Filter Algorithms
    filtered_algos = []
    for name, info in ALGORITHM_COMPLEXITY.items():
        if selected_category != "All" and info['category'] != selected_category:
            continue
        if selected_paradigm != "All" and info['paradigm'] != selected_paradigm:
            continue
        if search_query:
            query = search_query.lower()
            matches_name = query in name.lower()
            matches_desc = query in info.get('description', '').lower()
            matches_paradigm = query in info.get('paradigm', '').lower()
            matches_category = query in info.get('category', '').lower()
            matches_complexity = (query in info.get('best', '').lower() or
                                  query in info.get('average', '').lower() or
                                  query in info.get('worst', '').lower() or
                                  query in info.get('space', '').lower())
            if not (matches_name or matches_desc or matches_paradigm or matches_category or matches_complexity):
                continue
        filtered_algos.append((name, info))

    render_html(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin: 0.85rem 0 1.25rem 0;'>
        <div style='font-size: 0.85rem; color: {COLOR_TEXT_MUTED};'>
            Showing <b style='color: #FFFFFF;'>{len(filtered_algos)}</b> of 13 official DAA algorithms
        </div>
        <div style='font-size: 0.74rem; color: {COLOR_CYAN};'>
            Click 'View Details' on any algorithm card for full pseudocode, mathematical analysis &amp; action routes.
        </div>
    </div>
    """)

    if not filtered_algos:
        render_html(f"""
        <div style="text-align: center; padding: 3rem 1rem; color: #94A3B8;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🔍</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">No matching algorithms found</div>
            <div style="font-size: 0.82rem;">Try broadening your search term or resetting the category and paradigm filters.</div>
        </div>
        """)
        return

    # 3. Render Algorithm Cards in balanced 2-column layout
    cols = st.columns(2, gap="medium")
    for idx, (name, info) in enumerate(filtered_algos):
        with cols[idx % 2]:
            cat = info.get('category', 'Sorting')
            cat_color = CATEGORY_COLORS.get(cat, COLOR_PURPLE)
            stable_val = info.get('stable')
            stable_badge = "<span style='color:#4ADE80; font-weight:600;'>Stable</span>" if stable_val else "<span style='color:#94A3B8;'>Unstable</span>"
            inplace_val = info.get('in_place')
            inplace_badge = "<span style='color:#38BDF8; font-weight:600;'>In-place (O(1))</span>" if inplace_val else "<span style='color:#F59E0B;'>Auxiliary RAM</span>"

            with st.container(border=True):
                render_html(f"""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.65rem;">
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">{name}</div>
                        <div style="font-size: 0.76rem; color: {cat_color}; font-weight: 700; margin-top: 2px;">
                            {cat.upper()} &bull; <span style="color: #C4B5FD;">{info.get('paradigm', '')}</span>
                        </div>
                    </div>
                    <span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 3px 8px; font-size: 0.68rem; color: #CBD5E1;">
                        {stable_badge} &bull; {inplace_badge}
                    </span>
                </div>

                <div style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.5; min-height: 48px; margin-bottom: 0.85rem;">
                    {info.get('description', '')}
                </div>

                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.4rem; background: rgba(8, 14, 38, 0.65); padding: 0.65rem 0.5rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.24); box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 0 12px rgba(124, 58, 237, 0.10); margin-bottom: 0.75rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Best</div>
                        <div style="margin-top: 3px;">{complexity_badge(info.get('best', 'O(1)'))}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Average</div>
                        <div style="margin-top: 3px;">{complexity_badge(info.get('average', 'O(n)'))}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Worst</div>
                        <div style="margin-top: 3px;">{complexity_badge(info.get('worst', 'O(n)'))}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Space</div>
                        <div style="margin-top: 3px;">{complexity_badge(info.get('space', 'O(1)'))}</div>
                    </div>
                </div>
                """)

                with st.expander("📖 View Academic Details & Taxonomy"):
                    st.markdown("**Theoretical How It Works:**"); st.markdown(info.get("how_it_works", ""))
                    st.markdown("**Formal Pseudocode:**")
                    st.code(info.get('pseudocode', ''), language="python")

                    adv_col, dis_col = st.columns(2)
                    with adv_col:
                        st.markdown("**Key Advantages:**")
                        for adv in info.get('advantages', []):
                            st.markdown(f"- {adv}")

                    with dis_col:
                        st.markdown("**Key Limitations:**")
                        for dis in info.get('disadvantages', []):
                            st.markdown(f"- {dis}")

                    st.markdown("**Recommended Real-World Use Cases:**")
                    for uc in info.get('use_cases', []):
                        st.markdown(f"- {uc}")

                    if 'related' in info:
                        st.markdown(f"**Related Algorithms:** *{', '.join(info['related'])}*")

                    render_html("<div style='border-top: 1px solid rgba(255,255,255,0.08); margin: 0.85rem 0;'></div>")
                    btn_c1, btn_c2, btn_c3 = st.columns(3)

                    with btn_c1:
                        target = "Visualizer" if cat != "Graph" else "Graph Algorithms"
                        if st.button("Open Visualizer", key=f"lib_viz_{name}", use_container_width=True):
                            st.session_state['current_page'] = target
                            st.session_state['selected_algo_name'] = name
                            st.rerun()

                    with btn_c2:
                        if cat == "Sorting":
                            if st.button("Benchmark Lab", key=f"lib_bench_{name}", use_container_width=True):
                                st.session_state['current_page'] = "Benchmark Lab"
                                st.session_state['selected_benchmark_algo'] = name
                                st.rerun()
                        else:
                            if st.button("Complexity", key=f"lib_cplx_{name}", use_container_width=True):
                                st.session_state['current_page'] = "Complexity Analyzer"
                                st.rerun()

                    with btn_c3:
                        if st.button("Compare", key=f"lib_comp_{name}", use_container_width=True):
                            st.session_state['current_page'] = "Comparison"
                            st.rerun()

            render_html("<div style='margin-bottom: 0.75rem;'></div>")

    render_footer()
