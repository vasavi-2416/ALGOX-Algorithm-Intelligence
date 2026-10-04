"""
ALGOX — Algorithm Intelligence & Benchmarking Platform
Main Application Entry Point & Custom Session-State Router
"""
import streamlit as st
import os
import sys
import logging

# Ensure project root is prioritized in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import AlgoxDB
from core.ui import inject_css, render_sidebar, render_page_header

# Import all view modules from views/ (NOT pages/)
from views.login import render_login
from views.dashboard import render_dashboard
from views.visualizer import render_visualizer
from views.algorithms import render_algorithms
from views.benchmark import render_benchmark
from views.comparison import render_comparison
from views.recommendation import render_recommendation
from views.complexity import render_complexity
from views.graph_algorithms import render_graph_algorithms
from views.history import render_history
from views.saved_experiments import render_saved_experiments
from views.reports import render_reports
from views.settings import render_settings
from views.about import render_about
from views.battle import render_battle
from views.dataset_lab import render_dataset_lab
from views.workspace import render_workspace

PAGE_METADATA = {
    'Dashboard': (
        'Algorithm Intelligence Dashboard',
        'Analyze algorithm behavior, benchmark performance, and study complexity using real execution data.'
    ),
    'Visualizer': (
        'Algorithm Visualizer',
        'Observe algorithm execution step by step through actual state changes and operation counts.'
    ),
    'Algorithms': (
        'Algorithm Library',
        'Explore the 13 core algorithms, their design paradigms, complexities, and implementation properties.'
    ),
    'Benchmark Lab': (
        'Benchmark Lab',
        'Measure the execution performance of algorithms across different input distributions and dataset sizes.'
    ),
    'Comparison': (
        'Algorithm Comparison',
        'Compare sorting algorithms using measured execution time, comparisons, swaps, and memory usage.'
    ),
    'Recommendation': (
        'Algorithm Recommendation',
        'Select an algorithm based on problem characteristics, input properties, and resource requirements.'
    ),
    'Complexity Analyzer': (
        'Complexity Analyzer',
        'Study asymptotic growth and compare theoretical complexity with measured execution behavior.'
    ),
    'Graph Algorithms': (
        'Graph Algorithms',
        'Explore graph traversal, shortest-path, and minimum-spanning-tree algorithms on an interactive graph.'
    ),
    'History': (
        'Experiment History',
        'Review previously executed benchmark experiments and their measured results.'
    ),
    'Saved Experiments': (
        'Saved Experiments',
        'Access benchmark experiments saved for later analysis.'
    ),
    'Reports': (
        'Research Reports',
        'Export benchmark results and experiment records for academic analysis.'
    ),
    'Algorithm Battle': (
        'Algorithm Battle Arena',
        'Head-to-head empirical algorithm performance confrontation under identical experimental conditions.'
    ),
    'Dataset Lab': (
        'Dataset Laboratory',
        'Synthesize, inspect, and analyze benchmark datasets across diverse asymptotic distributions.'
    ),
    'Experiment Workspace': (
        'Experiment Workspace',
        'Integrated scientific workspace: configure, execute, inspect, and archive algorithm trials.'
    ),
    'Settings': (
        'Settings',
        'Configure application, benchmark, visualization, and data preferences.'
    ),
    'About': (
        'About ALGOX',
        'Algorithm Intelligence & Benchmarking Platform for Design and Analysis of Algorithms.'
    )
}

PAGE_ROUTING = {
    'Dashboard': render_dashboard,
    'Visualizer': render_visualizer,
    'Algorithms': render_algorithms,
    'Benchmark Lab': render_benchmark,
    'Comparison': render_comparison,
    'Recommendation': render_recommendation,
    'Complexity Analyzer': render_complexity,
    'Graph Algorithms': render_graph_algorithms,
    'History': render_history,
    'Saved Experiments': render_saved_experiments,
    'Reports': render_reports,
    'Algorithm Battle': render_battle,
    'Dataset Lab': render_dataset_lab,
    'Experiment Workspace': render_workspace,
    'Settings': render_settings,
    'About': render_about
}

def main():
    st.set_page_config(
        page_title="ALGOX — Algorithm Intelligence Platform",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject global Dark Research Lab theme and layout system
    inject_css()

    # Initialize SQLite database
    db = AlgoxDB()

    # Authentication guard
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # When unauthenticated: Show ONLY the login screen (sidebar is 100% hidden)
    if not st.session_state['authenticated']:
        import importlib
        import views.login
        importlib.reload(views.login)
        views.login.render_login()
        return

    # When authenticated: Render custom ALGOX sidebar
    current_page = render_sidebar(db)

    # Render ONE unified header per page
    title, subtitle = PAGE_METADATA.get(current_page, (current_page, "Algorithm Intelligence Platform"))
    render_page_header(title, subtitle, db=db)

    # Single-point application routing via session state
    render_fn = PAGE_ROUTING.get(current_page, render_dashboard)

    try:
        render_fn(db)
    except Exception as e:
        logging.error(f"Error rendering {current_page}: {e}", exc_info=True)
        st.error(f"Something went wrong while rendering the {current_page} view. Please refresh or regenerate the trace.")

if __name__ == "__main__":
    main()
