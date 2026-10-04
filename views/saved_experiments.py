"""
ALGOX — Saved Experiments Module
Curated laboratory benchmark collections saved for reports, presentations, and viva demonstrations.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.ui import (
    render_html,
    page_header,
    section_header,
    empty_state,
    format_time,
    format_number,
    status_badge,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_RED,
    COLOR_TEXT_MUTED,
    render_footer
)

def render_saved_experiments(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">💾</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(34,197,94,0.85);display:block;">ALGOX · SAVED EXPERIMENTS</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Saved Experiments</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Your curated collection of key benchmark runs — bookmarked for reports, presentations, and academic viva demonstrations.
</p>
</div>
""")

    saved_records = db.get_saved_experiments()

    if saved_records:
        st.markdown(f"<div style='font-size: 0.85rem; color: {COLOR_TEXT_MUTED}; margin-bottom: 1.25rem;'>You have <b>{len(saved_records)}</b> curated experiment(s) bookmarked.</div>", unsafe_allow_html=True)

        # Comparison Section if 2+ experiments exist
        if len(saved_records) >= 2:
            saved_titles = [f"#{item['saved_id']} — {item.get('title', 'Run')} ({item.get('algorithm') or 'Sort'}, N={(item.get('input_size') or 0):,})" for item in saved_records]
            with st.expander("⚖️ Compare Multiple Saved Experiments Head-to-Head"):
                selected_comp_titles = st.multiselect("Select 2 or more saved experiments to compare", saved_titles, key="saved_multicomp_select")
                if len(selected_comp_titles) >= 2:
                    selected_ids = [int(t.split(' — ')[0].replace('#', '')) for t in selected_comp_titles]
                    matched_records = [r for r in saved_records if r['saved_id'] in selected_ids]

                    c_names = [f"{r['title']} ({r.get('algorithm')})" for r in matched_records]
                    c_times = [r.get('avg_time', 0.0) * 1000.0 for r in matched_records]

                    fig_saved_comp = go.Figure(data=[go.Bar(
                        x=c_names,
                        y=c_times,
                        marker=dict(color=COLOR_CYAN),
                        text=[f"{t:.2f} ms" for t in c_times],
                        textposition='outside'
                    )])
                    fig_saved_comp.update_layout(
                        title="Execution Latency Comparison (ms)",
                        height=300,
                        margin=dict(l=10, r=10, t=35, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#F1F5F9'),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.06)')
                    )
                    st.plotly_chart(fig_saved_comp, use_container_width=True)

            st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)

        # Full-width cards for each saved experiment
        for item in saved_records:
            saved_id = item['saved_id']
            title = item.get('title') or f"Experiment #{saved_id}"
            notes = item.get('saved_notes') or ''
            created_at = item.get('created_at') or '—'
            algo = item.get('algorithm') or 'Custom Run'
            dataset = item.get('dataset') or 'Random'
            n = item.get('input_size') or 0
            avg_time = item.get('avg_time')
            comps = item.get('comparisons') or 0
            swaps = item.get('swaps') or 0
            exp_id = item.get('experiment_id') or item.get('id') or '—'

            with st.container(border=True):
                render_html(f"""
                <div style="padding: 4px 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">
                                {title}
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 3px;">
                                Bookmark #{saved_id} &bull; Experiment ID: #{exp_id}
                            </div>
                        </div>
                        <div style="font-size: 0.76rem; color: #94A3B8; background: rgba(255,255,255,0.04); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.08);">
                            📅 {created_at}
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 12px;">
                        <div style="background: rgba(10, 18, 45, 0.65); border: 1px solid rgba(139, 92, 246, 0.24); box-shadow: 0 4px 14px rgba(0,0,0,0.25), 0 0 8px rgba(139, 92, 246, 0.10); padding: 8px 12px; border-radius: 8px;">
                            <span style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">ALGORITHM</span>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #67E8F9; margin-top: 2px;">{algo}</div>
                        </div>
                        <div style="background: rgba(10, 18, 45, 0.65); border: 1px solid rgba(139, 92, 246, 0.24); box-shadow: 0 4px 14px rgba(0,0,0,0.25), 0 0 8px rgba(139, 92, 246, 0.10); padding: 8px 12px; border-radius: 8px;">
                            <span style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">DATASET DISTRIBUTION</span>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #F1F5F9; margin-top: 2px;">{dataset}</div>
                        </div>
                        <div style="background: rgba(10, 18, 45, 0.65); border: 1px solid rgba(139, 92, 246, 0.24); box-shadow: 0 4px 14px rgba(0,0,0,0.25), 0 0 8px rgba(139, 92, 246, 0.10); padding: 8px 12px; border-radius: 8px;">
                            <span style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">INPUT SCALE</span>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #C4B5FD; margin-top: 2px;">N = {n:,}</div>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; background: rgba(5,8,22,0.6); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px;">
                        <div>
                            <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 700;">EXECUTION TIME</span>
                            <div style="font-size: 1.15rem; font-weight: 800; color: #22C55E; margin-top: 2px;">{format_time(avg_time)}</div>
                        </div>
                        <div>
                            <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 700;">COMPARISONS</span>
                            <div style="font-size: 1.15rem; font-weight: 800; color: #93C5FD; margin-top: 2px;">{format_number(comps)}</div>
                        </div>
                        <div>
                            <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 700;">SWAPS / SHIFTS</span>
                            <div style="font-size: 1.15rem; font-weight: 800; color: #FCD34D; margin-top: 2px;">{format_number(swaps)}</div>
                        </div>
                    </div>

                    <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 10px; line-height: 1.5; background: rgba(255,255,255,0.02); padding: 8px 12px; border-radius: 6px;">
                        <span style="color: #94A3B8; font-weight: 700;">Notes:</span> {notes if notes else 'No additional notes provided for this curated trial.'}
                    </div>
                </div>
                """)

                # Actions Toolbar: Open / Export / Delete
                act_c1, act_c2, act_c3 = st.columns([1.5, 1.2, 1.2], gap="small")
                with act_c1:
                    if st.button(f"🔬 Open in Benchmark Lab", key=f"open_saved_{saved_id}", use_container_width=True):
                        st.session_state['current_page'] = 'Benchmark Lab'
                        st.session_state['selected_benchmark_algo'] = algo
                        st.rerun()
                with act_c2:
                    single_df = pd.DataFrame([{
                        "Bookmark_ID": saved_id,
                        "Title": title,
                        "Algorithm": algo,
                        "Distribution": dataset,
                        "Input_Size": n,
                        "Execution_Time_Sec": avg_time,
                        "Comparisons": comps,
                        "Swaps": swaps,
                        "Notes": notes,
                        "Saved_At": created_at
                    }])
                    st.download_button(
                        label="📥 Export CSV",
                        data=single_df.to_csv(index=False),
                        file_name=f"saved_experiment_{saved_id}_{algo.replace(' ', '_')}.csv",
                        mime="text/csv",
                        key=f"exp_csv_{saved_id}",
                        use_container_width=True
                    )
                with act_c3:
                    if st.button(f"🗑️ Delete", key=f"del_saved_{saved_id}", use_container_width=True):
                        db.delete_saved_experiment(saved_id)
                        st.success(f"Curated experiment #{saved_id} removed.")
                        st.rerun()

            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    else:
        empty_state(
            icon="💾",
            title="No Saved Experiments Yet",
            message="You haven't bookmarked any benchmark runs yet. After completing an experiment in the Benchmark Lab or Workspace, save your key findings to curate an academic collection.",
            button_label="Open Benchmark Lab",
            target_page="Benchmark Lab"
        )

    render_footer()
