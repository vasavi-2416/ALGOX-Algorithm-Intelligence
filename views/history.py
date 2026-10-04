"""
ALGOX — Experiment History Module
Complete audit log of all empirical benchmarks executed in ALGOX, with filtering, search, CSV export, and deletion.
"""
import streamlit as st
import pandas as pd
from core.ui import (
    render_html,
    page_header,
    section_header,
    empty_state,
    format_time,
    format_number,
    status_badge,
    warning_card,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_RED,
    COLOR_TEXT_MUTED,
    render_footer
)

def render_history(db):
    # Hero Banner
    render_html("""
<div class="algox-hero-card" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
<span style="font-size:2rem;">📋</span>
<div>
<span style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(139,92,246,0.85);display:block;">ALGOX · EXPERIMENT HISTORY</span>
<h1 style="font-size:1.75rem;font-weight:800;color:#FFFFFF;margin:0;line-height:1.15;">Experiment History</h1>
</div>
</div>
<p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;margin:0;max-width:680px;">
Complete audit log of all empirical benchmarks. Filter, search, export to CSV, and manage your recorded experiment database.
</p>
</div>
""")

    total_in_db = db.get_experiment_count()
    avg_t = db.get_average_execution_time()
    avg_t_str = format_time(avg_t) if avg_t is not None else "No data"

    validated_cnt = 0
    top_algo = "No data"
    if total_in_db > 0:
        try:
            with db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT SUM(correct) FROM experiments")
                v_row = cur.fetchone()
                validated_cnt = v_row[0] if v_row and v_row[0] else 0

                cur.execute("SELECT algorithm, COUNT(*) as c FROM experiments GROUP BY algorithm ORDER BY c DESC LIMIT 1")
                top_row = cur.fetchone()
                if top_row:
                    top_algo = f"{top_row[0]} ({top_row[1]} runs)"
        except Exception:
            pass

    # 1. Analytical Summary Cards (4 balanced cards using .algox-stat-card)
    h_c1, h_c2, h_c3, h_c4 = st.columns(4, gap="medium")
    with h_c1:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">TOTAL EXPERIMENTS</div>
            <div class="algox-stat-value" style="font-size:1.65rem; font-weight:800; color:#FFFFFF; white-space:nowrap;">{total_in_db:,}</div>
        </div>
        """)
    with h_c2:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">VALIDATED RUNS</div>
            <div class="algox-stat-value" style="font-size:1.65rem; font-weight:800; color:#06B6D4; white-space:nowrap;">{validated_cnt:,}</div>
        </div>
        """)
    with h_c3:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">AVERAGE RUNTIME</div>
            <div class="algox-stat-value" style="font-size:1.65rem; font-weight:800; color:#F59E0B; white-space:nowrap;">{avg_t_str}</div>
        </div>
        """)
    with h_c4:
        render_html(f"""
        <div class="algox-stat-card">
            <div style="font-size:0.72rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">MOST TESTED</div>
            <div class="algox-stat-value" style="font-size:1.25rem; font-weight:800; color:#22C55E; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{top_algo}</div>
        </div>
        """)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 2. Filter & Search Controls (Full width card)
    section_header("Filter & Search Experiments", icon="🔍", subtitle="Filter empirical database records by algorithm, distribution, or keyword.")
    with st.container(border=True):
        search = st.text_input("🔍 Search Keyword (notes, algorithm, dataset)", placeholder="e.g. Quick Sort, Random, N=1000…", key="hist_search")

        c_a, c_d, c_l = st.columns([1.5, 1.5, 1], gap="medium")
        with c_a:
            algo_filter = st.selectbox("Algorithm Filter", [
                "All",
                "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort",
                "Linear Search", "Binary Search",
                "BFS", "DFS", "Dijkstra", "Prim", "Kruskal"
            ], key="hist_algo")
        with c_d:
            dist_filter = st.selectbox("Distribution Filter", ["All", "Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicate Heavy"], key="hist_dist")
        with c_l:
            limit = st.selectbox("Maximum Records", [25, 50, 100, 500], index=1, key="hist_limit")

    # Fetch Experiments from DB
    records = db.get_experiments(
        limit=limit,
        algorithm=algo_filter,
        distribution=dist_filter,
        search=search if search else None
    )

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 3. Full Width Table
    if records:
        section_header("Recorded Experiments", icon="📋", subtitle=f"Displaying {len(records)} matching trials (Total logged in SQLite: {total_in_db:,}).")

        # Toolbar: CSV export
        t_col1, t_col2 = st.columns([3, 1])
        with t_col2:
            csv_data = db.export_experiments_csv()
            if csv_data:
                st.download_button(
                    label="📥 Export Full History CSV",
                    data=csv_data,
                    file_name="algox_experiment_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="hist_download_csv"
                )

        df = pd.DataFrame(records)
        df_display = pd.DataFrame({
            "ID": df["id"].apply(lambda x: f"#{x:03d}"),
            "Timestamp": df["timestamp"],
            "Algorithm": df["algorithm"],
            "Category": df.get("category", pd.Series(["—"]*len(df))),
            "Distribution": df["dataset"],
            "Input Size (N)": df["input_size"].apply(lambda x: f"{x:,}"),
            "Seed": df["seed"].apply(lambda x: str(int(x)) if pd.notna(x) else "—") if "seed" in df.columns else "—",
            "Avg Time": df["avg_time"].apply(format_time),
            "Std Dev": df["std_dev"].apply(lambda x: f"±{x*1000:.3f} ms" if pd.notna(x) and x > 0 else "—") if "std_dev" in df.columns else "—",
            "Min Time": df["min_time"].apply(format_time),
            "Max Time": df["max_time"].apply(format_time),
            "Comparisons": df["comparisons"].apply(lambda x: f"{x:,}"),
            "Swaps / Shifts": df["swaps"].apply(lambda x: f"{x:,}"),
            "Est. Aux Memory": df["memory_bytes"].apply(lambda x: f"{x:,} B"),
            "Status": df["correct"].apply(lambda c: "✅ Verified" if c == 1 else "❌ Failed"),
            "Notes": df["notes"]
        })
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # Record Deletion & Maintenance
        dz_col1, dz_col2 = st.columns(2, gap="large")
        with dz_col1:
            with st.expander("🗑️ Delete Individual Experiment Record"):
                del_id = st.number_input("Enter Experiment ID to Delete", min_value=1, step=1, key="hist_del_id")
                if st.button("Delete Record", key="hist_del_btn", use_container_width=True):
                    db.delete_experiment(del_id)
                    st.success(f"Experiment #{del_id} removed from SQLite.")
                    st.rerun()

        with dz_col2:
            with st.expander("⚠️ Danger Zone: Clear Entire Experiment History"):
                st.markdown("<div style='font-size:0.8rem; color:#F87171; margin-bottom:6px;'>This permanently deletes all benchmark experiment records from the SQLite database.</div>", unsafe_allow_html=True)
                confirm_str = st.text_input("Type 'DELETE' to confirm action", key="hist_clear_confirm")
                if st.button("Permanently Clear History", key="hist_clear_btn", type="primary", use_container_width=True, disabled=(confirm_str != "DELETE")):
                    db.clear_history()
                    st.success("All experiment history cleared from database.")
                    st.rerun()
    else:
        empty_state(
            icon="📋",
            title="No Benchmark Experiments Recorded Yet",
            message="No benchmark records match your current filters. Execute tests in the Benchmark Lab to populate the database with empirical measurements.",
            button_label="Go to Benchmark Lab",
            target_page="Benchmark Lab"
        )

    render_footer()
