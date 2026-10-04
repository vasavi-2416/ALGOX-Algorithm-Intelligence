# ALGOX — Algorithm Intelligence & Benchmarking Platform

<div align="center">

```
   ___    __    ____  ____  _  __
  / _ |  / /   / ___// __ \| |/ /
 / __ | / /__ / (_ // /_/ /|   / 
/_/ |_|/____/ \___/ \____//_/|_|  
```

**University-Level Design and Analysis of Algorithms (DAA) Research, Visualization & Benchmarking Platform**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)

</div>

---

## 1. Project Objective

In computer science education, **Design and Analysis of Algorithms (DAA)** is often taught purely through mathematical abstractions: asymptotic notations ($O$, $\Omega$, $\Theta$), recurrence relations, and theoretical worst-case proofs.

However, theoretical complexity does not reveal the full picture of **physical computational performance**:
- **CPU Cache Line Locality:** Sequential memory access (Quick Sort) vs non-contiguous pointer hopping (Heap Sort).
- **Memory Copy Overheads:** In-place algorithms ($O(1)$) vs auxiliary allocations (Merge Sort $O(n)$).
- **Input Distribution Skew:** Adaptive performance on pre-sorted arrays (Insertion Sort $O(n)$ vs Selection Sort $O(n^2)$).

**ALGOX** bridges the gap between **theoretical algorithm analysis** and **real empirical execution performance**. Every measurement, chart, and counter in ALGOX is computed in real time from physical machine runs and persisted in an SQLite database.

---

## 2. Core Features

- **Administrator Portal:** Clean dark-cyber authentication interface designed for local university viva and evaluation sessions.
- **Dynamic Analytics Dashboard:** Live SQLite KPI counters (Total Experiments, Fastest Algorithm, Average Latency, Recommendations).
- **Interactive Visualizer:** Step-by-step graphical state transitions for sorting (bar charts with color-coded comparison, swap, pivot, and sorted states) and searching (interval bisection).
- **Algorithm Catalog & Library:** In-depth technical specifications, pseudocode, asymptotic proofs, advantages, disadvantages, and industry use cases for all 13 core algorithms.
- **Benchmark Laboratory:** High-precision empirical execution engine measuring microsecond timing (`time.perf_counter()`), comparisons, swaps/shifts, auxiliary memory footprints, and strict correctness validation.
- **Computational Safety Guardrails:** Dynamic complexity safeguards preventing system freezes when evaluating quadratic algorithms ($O(n^2)$) on large datasets ($N > 5,000$).
- **Head-to-Head Comparison:** Direct multi-algorithm confrontation across single sizes and multi-tier scaling curves ($N=50 \dots 4,000$).
- **Rule-Based Recommendation Engine:** Deterministic algorithmic decision logic recommending optimal algorithms based on problem scale, known distribution, stability requirements, and memory constraints (not fake machine learning).
- **Complexity Analyzer:** Interactive Big-O growth curves (logarithmic/linear scales), asymptotic taxonomy matrices, and formal recurrence relation derivations (Master Theorem).
- **Graph Algorithms Workbench:** Interactive 2D topological graph workbench supporting BFS, DFS, Dijkstra shortest path routing, and Prim/Kruskal Minimum Spanning Tree (MST) algorithms.
- **Persistent Experiment History:** Searchable, filterable audit trail stored in SQLite with CSV export and individual record deletion.
- **Curated Saved Experiments:** Bookmark critical benchmark findings with descriptive titles and lab notes for viva presentations.
- **Data Export & Reporting:** Instant generation and download of CSV reports for full history logs, aggregated statistical summaries, and algorithm best records.
- **Platform Settings:** Configurable benchmark defaults, visualizer parameters, and safe database reset controls.

---

## 3. Official Algorithm Scope (13 Algorithms)

ALGOX implements **exactly 13 official DAA algorithms** with manual, un-shortcuted implementations:

| Category | Algorithm | Paradigm | Best Case | Average Case | Worst Case | Space |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Sorting** | Bubble Sort | Brute Force | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Sorting** | Selection Sort | Brute Force | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Sorting** | Insertion Sort | Incremental / Adaptive | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Sorting** | Merge Sort | Divide and Conquer | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **Sorting** | Quick Sort | Divide and Conquer | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ |
| **Sorting** | Heap Sort | Heap-Based | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ |
| **Searching** | Linear Search | Sequential / Brute Force | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Searching** | Binary Search | Divide and Conquer | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Graph** | Breadth-First Search (BFS) | Graph Traversal | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Graph** | Depth-First Search (DFS) | Graph Traversal | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Graph** | Dijkstra's Algorithm | Greedy Shortest Path | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O(V)$ |
| **Graph** | Prim's Algorithm | Greedy Minimum Spanning Tree | $O(E \log V)$ | $O(E \log V)$ | $O(E \log V)$ | $O(V)$ |
| **Graph** | Kruskal's Algorithm | Greedy MST (Disjoint Set) | $O(E \log E)$ | $O(E \log E)$ | $O(E \log E)$ | $O(V + E)$ |

---

## 4. Fundamental DAA Concepts Covered

1. **Asymptotic Notations & Master Theorem:** Rigorous classification using Big-O, Big-$\Omega$, and Big-$\Theta$, with Master Theorem applications for divide-and-conquer recurrences.
2. **Algorithmic Design Paradigms:**
   - **Brute Force:** Bubble Sort, Selection Sort, Linear Search
   - **Divide and Conquer:** Merge Sort, Quick Sort, Binary Search
   - **Incremental / Adaptive:** Insertion Sort
   - **Heap Invariants:** Max-heap construction and root sift-down in Heap Sort
   - **Greedy Optimization:** Dijkstra, Prim, and Kruskal (Cut Property & Cycle Detection)
   - **Graph Traversal:** Queue-based BFS vs Recursion-based DFS
3. **Stability & In-Place Mechanics:**
   - Stable vs Unstable key retention
   - Auxiliary space bounds ($O(1)$ vs $O(n)$ vs $O(\log n)$ call stack frames)
4. **Disjoint Set Union (DSU):**
   - Implemented via path compression and union-by-rank in Kruskal's MST algorithm.

---

## 5. Technology Stack

- **Core Language:** Python 3.9+
- **Interactive Framework:** Streamlit
- **Visualization Engine:** Plotly Graph Objects (Custom ALGOX Dark Cyber Theme)
- **Data Analysis & Processing:** Pandas & NumPy
- **Persistence Engine:** SQLite3
- **High-Precision Timing:** `time.perf_counter()`

---

## 6. Project Architecture

```
ALGOX/
├── app.py                      # Main entry point, page router & authentication
├── requirements.txt            # Minimal dependencies
├── README.md                   # Comprehensive academic documentation
│
├── algorithms/                 # Real manual algorithm implementations
│   ├── __init__.py
│   ├── sorting.py              # 6 sorting algorithms with step tracing & operation counters
│   ├── searching.py            # Linear and Binary search with intervals
│   └── graph.py                # BFS, DFS, Dijkstra, Prim, Kruskal & DSU
│
├── core/                       # Core platform engine modules
│   ├── __init__.py
│   ├── dataset.py              # 5 distributions: Random, Sorted, Reverse, Nearly, Duplicates
│   ├── complexity.py           # Academic taxonomy & recurrence metadata for 13 algorithms
│   ├── benchmark.py            # Microsecond execution timing, operation counts, safety guards
│   ├── recommendation.py       # Deterministic rule-based algorithmic decision engine
│   ├── steps.py                # Step trace adapter for visualizer
│   └── ui.py                   # Unified Dark Research Lab design system & components
│
├── database/                   # SQLite database persistence layer
│   ├── __init__.py
│   └── database.py             # CRUD operations for experiments, datasets, settings
│
├── views/                      # 13 dedicated application views
│   ├── __init__.py
│   ├── login.py                # Administrator authentication screen
│   ├── dashboard.py            # Real-time analytics, KPIs, distribution histogram
│   ├── visualizer.py           # Step-by-step sorting & searching visualizer
│   ├── algorithms.py           # 13 algorithm catalog with pseudocode & proofs
│   ├── benchmark.py            # Benchmark laboratory with safety alerts & charts
│   ├── comparison.py           # Head-to-head comparison & asymptotic scaling curves
│   ├── recommendation.py       # Rule engine with explainable justification
│   ├── complexity.py           # Interactive Big-O curves & taxonomy matrix
│   ├── graph_algorithms.py     # Graph workbench with 2D topology layouts
│   ├── history.py              # Filterable SQLite experiment log & CSV export
│   ├── saved_experiments.py    # Curated saved benchmark runs with lab notes
│   ├── reports.py              # Formal CSV report downloads
│   ├── settings.py             # Configuration & persistent database management
│   └── about.py                # Academic objectives, scope & paradigms
│
├── tests/                      # Verification test suite
│   └── test_algox.py           # Automated unit & integration tests
│
└── data/                       # Persistent SQLite database storage
    └── algox.db
```

---

## 7. Installation & Running Instructions

### Prerequisites
Ensure Python 3.9 or newer is installed on your system.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run ALGOX Platform
```bash
python -m streamlit run app.py --server.port 8052
```

The application will launch in your browser at `http://localhost:8052`.

---

## 8. Login Credentials

- **Username:** `admin`
- **Password:** `algox`

*Designed for local academic evaluation and university viva demonstration.*

---

## 9. Verification & Automated Testing

ALGOX includes an automated test suite verifying all 13 algorithms, 5 dataset distributions, SQLite operations, and recommendation logic:

```bash
python -m unittest tests/test_algox.py
```

---

## 10. Academic Evaluation & Viva Demonstration Guide

When presenting ALGOX for academic grading or project evaluation:

1. **Benchmark Lab Demonstration:**
   - Execute a benchmark comparing **Merge Sort**, **Quick Sort**, and **Heap Sort** on $N=2,000$ elements.
   - Highlight that while all three are asymptotically $O(n \log n)$, **Quick Sort** executes faster empirically due to sequential CPU cache locality.
   - Show that **Merge Sort** requires $16,064$ bytes of auxiliary memory, whereas **Heap Sort** requires $O(1)$ space.
2. **Distribution Impact Demonstration:**
   - In the **Comparison** module, select **Insertion Sort** vs **Selection Sort**.
   - Test first on **Random** data, then switch to **Nearly Sorted** data.
   - Point out that Insertion Sort drops to $O(n)$ linear runtime on nearly sorted data, while Selection Sort remains stuck in $O(n^2)$ quadratic comparisons.
3. **Graph Algorithms Workbench:**
   - Run **Prim's Algorithm** and **Kruskal's Algorithm** on the 6-node network.
   - Demonstrate that both distinct greedy paradigms produce the exact same Minimum Spanning Tree weight ($13$), while displaying rejected cycle-forming edges in Kruskal's run.
4. **Recommendation Engine:**
   - Enter input constraints: *Large Scale ($N=10,000$)*, *Strict In-Place Memory Required*, *No Stability Needed*.
   - Watch the engine deduce **Quick Sort** or **Heap Sort** with mathematical proofs and alternative trade-offs.

---

## 11. Database Schema

Stored at `data/algox.db` using SQLite:

- `experiments`: Stores empirical benchmark runs (Timestamp, Algorithm, Distribution, $N$, Latencies, Operations, Memory, Correctness).
- `saved_experiments`: Stores curated user bookmarks with titles and research notes.
- `datasets`: Records synthetic datasets generated during lab sessions.
- `settings`: Key-value store persisting platform configuration across restarts.
- `counters`: Tracks system-wide statistics (e.g. recommendations computed).

---

## 12. License & Academic Integrity

Built for university academic demonstrations, algorithm benchmarking research, and viva examinations in Design & Analysis of Algorithms (DAA).
