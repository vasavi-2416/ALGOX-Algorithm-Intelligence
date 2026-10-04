"""
ALGOX — Dataset Laboratory Module
Synthetic distribution generator, mathematical entropy profiler, and statistical feature extractor.
Restructured into a seamless vertical laboratory flow with rich metric tiles.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import statistics
from core.dataset import generate_dataset, DISTRIBUTIONS
from core.ui import (render_html, section_header, success_card, warning_card,
                     get_plotly_layout, format_number, render_footer,
                     COLOR_PURPLE, COLOR_CYAN, COLOR_GREEN, COLOR_AMBER, COLOR_TEXT_MUTED)
from database.database import AlgoxDB


def render_dataset_lab(db: AlgoxDB):
    # Hero Banner
    render_html("""
    <div class="algox-hero-card" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <span class="algox-badge algox-badge-cyan" style="margin-bottom: 6px; box-shadow: 0 0 10px rgba(6,182,212,0.3);">🧪 DATASET LABORATORY</span>
                <h1 style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; margin: 4px 0 0 0;">
                    Synthetic Dataset Laboratory
                </h1>
                <div style="font-size: 0.88rem; color: #CBD5E1; margin-top: 4px;">
                    Synthesize, inspect, and mathematically profile empirical datasets across 5 fundamental asymptotic distributions.
                </div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="algox-badge algox-badge-purple">Entropy Analysis</span>
                <span class="algox-badge algox-badge-green">SQLite Dataset Logging</span>
            </div>
        </div>
    </div>
    """)

    # Populate default dataset on initial visit to ensure the laboratory is immediately active
    if "lab_dataset" not in st.session_state:
        st.session_state["lab_dataset"] = generate_dataset(500, "Random", 42)
        st.session_state["lab_dist"] = "Random"
        st.session_state["lab_size"] = 500
        st.session_state["lab_seed"] = 42

    # =========================================================================
    # SECTION 1: DATASET CONFIGURATION (Full-Width Laboratory Panel)
    # =========================================================================
    section_header("Dataset Parameters", icon="⚙️", subtitle="Specify synthetic generation distribution, scale, and entropy seed.")
    with st.container(border=True):
        c1, c2, c3 = st.columns([1.3, 1.3, 1.4], gap="medium")
        with c1:
            cur_dist = st.session_state.get("lab_dist", "Random")
            dist_options = ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicate Heavy"]
            dist_idx = dist_options.index(cur_dist) if cur_dist in dist_options else 0
            dist = st.selectbox(
                "Distribution Morphology",
                dist_options,
                index=dist_idx,
                key="dsl_dist"
            )

        with c2:
            cur_size = st.session_state.get("lab_size", 500)
            size = st.slider("Dataset Scale (N)", min_value=10, max_value=10000, value=cur_size, step=10, key="dsl_size")

        with c3:
            seed_col, chk_col = st.columns(2, gap="small")
            with seed_col:
                cur_seed = st.session_state.get("lab_seed", 42)
                seed_val = st.number_input("Random Seed", min_value=0, max_value=99999, value=cur_seed if cur_seed else 0, key="dsl_seed")
                seed = int(seed_val) if seed_val > 0 else None
            with chk_col:
                st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
                save_dataset = st.checkbox("Record in DB History", value=True, key="dsl_save_chk")

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        gen_btn = st.button("🧪 GENERATE & PROFILE DATASET", use_container_width=True, type="primary", key="dsl_gen_btn")

    if gen_btn:
        with st.spinner("Synthesizing empirical dataset…"):
            arr = generate_dataset(size, dist, seed)
        st.session_state["lab_dataset"] = arr
        st.session_state["lab_dist"] = dist
        st.session_state["lab_size"] = size
        st.session_state["lab_seed"] = seed

        if save_dataset:
            try:
                db.log_dataset(
                    name=f"{dist} N={size}",
                    distribution=dist,
                    size=size,
                    seed=seed
                )
                success_card("Dataset Recorded", f"{dist} dataset (N={format_number(size)}) saved to database.")
            except Exception as e:
                st.warning(f"Could not record dataset: {e}")
        st.rerun()

    # =========================================================================
    # SECTION 2: STATISTICAL FEATURE EXTRACTION (8 Balanced Metric Cards)
    # =========================================================================
    arr = st.session_state.get("lab_dataset")
    if arr is not None:
        n = len(arr)
        arr_sorted = sorted(arr)
        mn = min(arr)
        mx = max(arr)
        mean_val = sum(arr) / n if n > 0 else 0
        median_val = (arr_sorted[n//2-1] + arr_sorted[n//2]) / 2 if n % 2 == 0 else arr_sorted[n//2]
        std_val = statistics.stdev(arr) if n > 1 else 0
        unique_count = len(set(arr))
        dup_ratio = round((1 - unique_count / n) * 100, 1) if n > 0 else 0
        in_order = sum(1 for i in range(n-1) if arr[i] <= arr[i+1])
        sortedness = round(in_order / (n-1) * 100, 1) if n > 1 else 100.0

        st.markdown("<div style='margin-top: 26px;'></div>", unsafe_allow_html=True)
        section_header("Mathematical Statistics & Feature Extraction", icon="📊",
                       subtitle=f"Computed mathematical properties for {st.session_state.get('lab_dist')} (N={format_number(n)}).")

        # Row 1: Size, Min, Max, Mean
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4, gap="medium")
        with r1_c1:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">SAMPLE SIZE</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; white-space: nowrap;">{format_number(n)}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Total observations</div>
            </div>
            """)
        with r1_c2:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">MINIMUM</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #06B6D4; white-space: nowrap;">{format_number(mn)}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Lower bound</div>
            </div>
            """)
        with r1_c3:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">MAXIMUM</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #8B5CF6; white-space: nowrap;">{format_number(mx)}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Upper bound</div>
            </div>
            """)
        with r1_c4:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">MEAN</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #3B82F6; white-space: nowrap;">{mean_val:,.1f}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Arithmetic average</div>
            </div>
            """)

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        # Row 2: Median, Std Dev, Unique Values, Sortedness
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4, gap="medium")
        with r2_c1:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">MEDIAN</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #F59E0B; white-space: nowrap;">{median_val:,.1f}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">50th percentile</div>
            </div>
            """)
        with r2_c2:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">STD DEV</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #22C55E; white-space: nowrap;">{std_val:,.1f}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Dispersion spread</div>
            </div>
            """)
        with r2_c3:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">UNIQUE VALUES</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #EC4899; white-space: nowrap;">{format_number(unique_count)}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">{dup_ratio:.1f}% duplicate ratio</div>
            </div>
            """)
        with r2_c4:
            render_html(f"""
            <div class="algox-stat-card">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">SORTEDNESS</div>
                <div class="algox-stat-value" style="font-size: 1.65rem; font-weight: 800; color: #22C55E; white-space: nowrap;">{sortedness:.1f}%</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">Ascending order purity</div>
            </div>
            """)

        # =====================================================================
        # SECTION 3: DATASET DISTRIBUTION HISTOGRAM
        # =====================================================================
        st.markdown("<div style='margin-top: 26px;'></div>", unsafe_allow_html=True)
        section_header("Dataset Distribution", icon="📈", subtitle="Frequency distribution histogram across value spectrum.")
        with st.container(border=True):
            render_html("""
            <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                VALUE FREQUENCY SPECTRUM
            </div>
            """)
            fig = go.Figure(go.Histogram(
                x=arr,
                nbinsx=min(50, len(arr) // 10 + 5),
                marker_color="#06B6D4",
                opacity=0.85
            ))
            hist_layout = get_plotly_layout(
                title="",
                height=260,
                x_title="Element Value Range",
                y_title="Frequency Count"
            )
            hist_layout["margin"] = dict(l=10, r=10, t=10, b=10)
            fig.update_layout(**hist_layout)
            st.plotly_chart(fig, use_container_width=True)

        # =====================================================================
        # SECTION 4: DATA PREVIEW (First 30 Elements Monospace Chips)
        # =====================================================================
        st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)
        section_header("First 30 Elements Preview", icon="🔍", subtitle="Initial prefix sequence of the synthesized dataset.")
        with st.container(border=True):
            preview_count = min(30, len(arr))
            chips_html = "".join([
                f'<span style="background: rgba(10,18,45,0.7); border: 1px solid rgba(139,92,246,0.3); padding: 5px 12px; border-radius: 8px; font-size: 0.82rem; font-family: monospace; color: #F1F5F9; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">{x}</span>'
                for x in arr[:preview_count]
            ])
            render_html(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 8px; padding: 4px 0;">
                {chips_html}
            </div>
            """)

    # =========================================================================
    # SECTION 5: RECENT DATASET HISTORY TABLE
    # =========================================================================
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    section_header("Recent Dataset History", icon="🗄️", subtitle="Previously logged synthetic datasets recorded in SQLite.")
    with st.container(border=True):
        try:
            with db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, name, distribution, size, seed, created_at FROM datasets ORDER BY id DESC LIMIT 10")
                ds_rows = cur.fetchall()

            if ds_rows:
                df_ds = pd.DataFrame(ds_rows, columns=["ID", "Name", "Distribution", "Size (N)", "Seed", "Created At"])
                df_ds["ID"] = df_ds["ID"].apply(lambda x: f"#{x:03d}")
                df_ds["Size (N)"] = df_ds["Size (N)"].apply(lambda x: f"{x:,}")
                df_ds["Seed"] = df_ds["Seed"].apply(lambda x: str(x) if x is not None else "Random")
                st.dataframe(df_ds, use_container_width=True, hide_index=True)
            else:
                render_html("""
                <div style="text-align: center; padding: 1.5rem 0.5rem; color: #94A3B8; font-size: 0.85rem;">
                    No datasets logged yet. Check "Record in DB History" when generating a dataset.
                </div>
                """)
        except Exception as e:
            st.caption(f"History query unavailable: {e}")

    render_footer()
