"""
ALGOX — Reports & Data Export Module
Generates real CSV datasets and summaries for external academic reporting, spreadsheet analysis, and project viva submissions.
"""
import streamlit as st
import pandas as pd
import datetime
from core.ui import (
    render_html,
    section_header,
    empty_state,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_TEXT_MUTED
,
    render_footer
)

def render_reports(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">📊</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(34,197,94,0.85);display:block;">ALGOX · REPORTS &amp; EXPORTS</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Reports &amp; Data Exports</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Generate and download formatted CSV reports from your experiment database for academic reporting, spreadsheet analysis, and viva submissions.
</p>
</div>
""")

    raw_experiments = db.get_experiments(limit=10000)
    total_records = len(raw_experiments)

    if total_records == 0:
        empty_state(
            icon="📊",
            title="No benchmark data available",
            message="Run a benchmark before generating a report.",
            button_label="Open Benchmark Lab",
            target_page="Benchmark Lab"
        )
        return

    df_raw = pd.DataFrame(raw_experiments)

    # 1. Full Experiment History Report Card
    with st.container(border=True):
        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; font-size: 1.15rem; color: #FFFFFF;">
                Complete Experiment History Log
            </div>
            <span style="font-size: 0.75rem; color: {COLOR_CYAN}; font-weight: 600;">
                {total_records:,} Total Records Logged
            </span>
        </div>
        <p style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; margin-bottom: 1rem;">
            Full raw empirical dataset containing timestamps, algorithm names, input scale (N), execution latencies (avg/min/max), comparisons, swaps/shifts, and memory metrics.
        </p>
        """)

        csv_history = db.export_experiments_csv()
        st.download_button(
            label="Export CSV",
            data=csv_history,
            file_name=f"algox_full_history_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
            key="rep_dl_full_csv"
        )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 2. Aggregated Benchmark Summary Report Card
    agg_df = df_raw.groupby(['algorithm', 'dataset']).agg(
        total_runs=('id', 'count'),
        avg_latency=('avg_time', 'mean'),
        min_latency=('min_time', 'min'),
        max_latency=('max_time', 'max'),
        avg_comparisons=('comparisons', 'mean'),
        avg_swaps=('swaps', 'mean')
    ).reset_index()

    agg_csv = agg_df.to_csv(index=False)

    with st.container(border=True):
        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; font-size: 1.15rem; color: #FFFFFF;">
                Aggregated Algorithm Performance Summary
            </div>
            <span style="font-size: 0.75rem; color: {COLOR_CYAN}; font-weight: 600;">
                {len(agg_df)} Groupings
            </span>
        </div>
        <p style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; margin-bottom: 1rem;">
            Statistical grouping by Algorithm and Dataset Distribution. Computes mean execution times, boundary latencies, and mean operation counts.
        </p>
        """)

        st.download_button(
            label="Export CSV",
            data=agg_csv,
            file_name=f"algox_aggregated_summary_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
            key="rep_dl_agg_csv"
        )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 3. Top Performers Report Card
    top_df = df_raw.sort_values(by='avg_time', ascending=True).groupby('algorithm').first().reset_index()
    top_csv = top_df.to_csv(index=False)

    with st.container(border=True):
        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; font-size: 1.15rem; color: #FFFFFF;">
                Algorithm Personal Best Runs
            </div>
            <span style="font-size: 0.75rem; color: {COLOR_GREEN}; font-weight: 600;">
                {len(top_df)} Algorithm Bests
            </span>
        </div>
        <p style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; margin-bottom: 1rem;">
            Extracts the fastest recorded execution run for every algorithm in the SQLite database, detailing measured execution times.
        </p>
        """)

        st.download_button(
            label="Export CSV",
            data=top_csv,
            file_name=f"algox_best_performers_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
            key="rep_dl_top_csv"
        )

    render_footer()
