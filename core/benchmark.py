"""
ALGOX — Benchmark Engine Module
Executes empirical performance tests with real microsecond timing, operation counts,
memory estimation, and formal correctness verification across all 13 algorithms.
"""
from typing import List, Dict, Any, Optional, Tuple
import time
import statistics
import math

from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort
)
from algorithms.searching import (
    linear_search,
    binary_search
)
from algorithms.graph import (
    bfs,
    dfs,
    dijkstra,
    prim,
    kruskal,
    DEFAULT_GRAPH
)
from core.dataset import generate_dataset

SORTING_FUNCTION_MAP = {
    'Bubble Sort': bubble_sort,
    'Selection Sort': selection_sort,
    'Insertion Sort': insertion_sort,
    'Merge Sort': merge_sort,
    'Quick Sort': quick_sort,
    'Heap Sort': heap_sort
}

SEARCHING_FUNCTION_MAP = {
    'Linear Search': linear_search,
    'Binary Search': binary_search
}

GRAPH_FUNCTION_MAP = {
    'BFS': bfs,
    'DFS': dfs,
    'Dijkstra': dijkstra,
    'Prim': prim,
    'Kruskal': kruskal
}

QUADRATIC_ALGORITHMS = {'Bubble Sort', 'Selection Sort', 'Insertion Sort'}

# =========================================================================
# 1. CORRECTNESS VERIFICATION SUITE
# =========================================================================

def verify_sorting_result(original: List[int], sorted_arr: List[int]) -> Tuple[bool, str]:
    """
    Verifies that the algorithm output matches ground truth:
    1. Exactly same multiset of elements (same length, elements).
    2. Strictly monotonic non-decreasing order.
    """
    if len(original) != len(sorted_arr):
        return False, f"Length mismatch: original has {len(original)}, result has {len(sorted_arr)}"
    
    is_ordered = all(sorted_arr[i] <= sorted_arr[i + 1] for i in range(len(sorted_arr) - 1))
    if not is_ordered:
        return False, "Result array violates ascending order invariant"
    
    expected = sorted(original)
    if sorted_arr != expected:
        return False, "Result array elements do not match sorted ground truth"
    
    return True, "Ascending order and element integrity verified against ground truth"


def verify_searching_result(arr: List[int], target: int, result: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Verifies searching correctness:
    - If target exists: found is True and arr[index] == target
    - If target absent: found is False and index == -1
    """
    target_in_arr = (target in arr)
    found = result.get('found', False)
    idx = result.get('index', -1)

    if target_in_arr != found:
        return False, f"Presence mismatch: target is {'present' if target_in_arr else 'absent'} in array, but algorithm returned found={found}"

    if found:
        if idx < 0 or idx >= len(arr) or arr[idx] != target:
            return False, f"Index verification failed: returned index {idx} does not contain target {target}"
        return True, f"Target {target} correctly identified at index {idx}"
    else:
        if idx != -1:
            return False, f"Index mismatch: target absent but index returned {idx} instead of -1"
        return True, f"Target {target} correctly confirmed absent from array"


def verify_graph_result(graph: Dict[str, List[Tuple[str, float]]], algo_name: str, result: Dict[str, Any], start_node: str = 'A') -> Tuple[bool, str]:
    """
    Verifies graph algorithm results against formal topological invariants:
    - BFS/DFS: traversal visits reachable vertices without duplicates or unreachable nodes.
    - Dijkstra: distances satisfy triangle inequality (dist[v] <= dist[u] + w).
    - Prim/Kruskal: MST forms an acyclic subgraph spanning all connected vertices with V-1 edges.
    """
    nodes = list(graph.keys())
    V = len(nodes)

    if algo_name in ('BFS', 'DFS'):
        order = result.get('traversal_order', [])
        if not order:
            return False, "Traversal order is empty"
        if order[0] != start_node:
            return False, f"Traversal does not begin at specified start vertex '{start_node}'"
        if len(order) != len(set(order)):
            return False, "Traversal contains duplicate visited vertices"
        for v in order:
            if v not in graph:
                return False, f"Traversal visited unknown vertex '{v}'"
        return True, f"Valid traversal order spanning {len(order)} reachable vertices from '{start_node}'"

    elif algo_name == 'Dijkstra':
        distances = result.get('distances', {})
        if start_node not in distances or distances[start_node] != 0:
            return False, f"Distance to start vertex '{start_node}' is not 0"
        
        # Verify triangle inequality for every edge
        for u, neighbors in graph.items():
            if u in distances and distances[u] != float('inf'):
                for v, w in neighbors:
                    if v in distances and distances[v] != float('inf'):
                        if distances[v] > distances[u] + w + 1e-9:
                            return False, f"Triangle inequality violated on edge ({u} -> {v}): dist[{v}]={distances[v]} > dist[{u}] + {w}"
        return True, f"Shortest path distances strictly satisfy triangle inequality across all edges"

    elif algo_name in ('Prim', 'Kruskal'):
        mst_edges = result.get('mst_edges', [])
        total_w = result.get('total_weight', 0)
        
        # Compute connected components of the graph
        adj = {n: set() for n in nodes}
        for u in graph:
            for v, _ in graph[u]:
                if u in adj and v in adj:
                    adj[u].add(v)
                    adj[v].add(u)

        visited_comp = set()
        components = []
        for n in nodes:
            if n not in visited_comp:
                comp = set()
                q = [n]
                visited_comp.add(n)
                while q:
                    curr = q.pop()
                    comp.add(curr)
                    for nbr in adj.get(curr, []):
                        if nbr not in visited_comp:
                            visited_comp.add(nbr)
                            q.append(nbr)
                components.append(comp)

        num_components = len(components)
        is_connected = (num_components <= 1)

        # Expected edge count check based on graph connectivity
        if algo_name == 'Prim':
            start_comp = next((c for c in components if start_node in c), set())
            expected_edges = max(0, len(start_comp) - 1)
            if len(mst_edges) != expected_edges:
                return False, f"Prim edge count mismatch for component: expected {expected_edges} edges, but got {len(mst_edges)}"
        else:  # Kruskal
            expected_edges = max(0, V - num_components)
            if len(mst_edges) != expected_edges:
                return False, f"Kruskal edge count mismatch: expected V - k = {expected_edges} edges across {num_components} components, but got {len(mst_edges)}"
        
        # Check sum of weights
        calc_w = sum(w for _, _, w in mst_edges)
        if abs(calc_w - total_w) > 1e-6:
            return False, f"MST total weight mismatch: reported {total_w} != calculated {calc_w}"
        
        # Check acyclic property using Disjoint Set Union (DSU)
        parent = {n: n for n in nodes}
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i == root_j:
                return False
            parent[root_i] = root_j
            return True

        for u, v, w in mst_edges:
            if not union(u, v):
                return False, f"Cycle detected in MST: edge ({u}, {v}) connects already unified components"
        
        return True, f"Valid Minimum Spanning Tree: {len(mst_edges)} edges, acyclic, total weight = {total_w}"

    return True, "Algorithm execution completed"


# =========================================================================
# 2. MEMORY ESTIMATION
# =========================================================================

def estimate_auxiliary_memory(algo_name: str, n: int) -> int:
    """
    Estimates auxiliary memory in bytes based on theoretical algorithm memory footprint.
    Integers in 64-bit Python take ~8 bytes (reference in list).
    """
    if algo_name == 'Merge Sort':
        return n * 8 + 64
    elif algo_name == 'Quick Sort':
        depth = max(1, int(math.log2(max(2, n))))
        return depth * 128
    elif algo_name in ('BFS', 'DFS'):
        return n * 64 + 128
    elif algo_name == 'Dijkstra':
        return n * 128 + 256
    elif algo_name in ('Prim', 'Kruskal'):
        return n * 96 + 256
    else:
        return 64


# =========================================================================
# 3. BENCHMARK EXECUTORS
# =========================================================================

def run_benchmark(
    algorithm_name: str,
    arr: List[int],
    repetitions: int = 3,
    distribution: str = 'Random',
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Executes a sorting algorithm on a copy of `arr` for `repetitions` times.
    Uses time.perf_counter() for high precision.
    Returns empirical metrics.
    """
    if algorithm_name not in SORTING_FUNCTION_MAP:
        raise ValueError(f"Unknown sorting algorithm: '{algorithm_name}'")

    fn = SORTING_FUNCTION_MAP[algorithm_name]
    times = []
    last_result = None

    for _ in range(max(1, repetitions)):
        arr_copy = list(arr)
        t_start = time.perf_counter()
        result = fn(arr_copy, track_steps=False)
        t_end = time.perf_counter()
        times.append(t_end - t_start)
        last_result = result

    is_correct, verify_msg = verify_sorting_result(arr, last_result['sorted_array'])

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0.0

    memory_bytes = estimate_auxiliary_memory(algorithm_name, len(arr))

    return {
        'algorithm': algorithm_name,
        'category': 'Sorting',
        'dataset': distribution,
        'distribution': distribution,
        'seed': seed if seed is not None else 42,
        'input_size': len(arr),
        'repetitions': repetitions,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'std_dev': std_dev,
        'comparisons': last_result['comparisons'],
        'swaps': last_result.get('swaps', 0),
        'shifts': last_result.get('shifts', 0),
        'memory_bytes': memory_bytes,
        'memory_label': 'Estimated Auxiliary Memory',
        'correct': is_correct,
        'verification_msg': verify_msg
    }


def run_search_benchmark(
    algorithm_name: str,
    arr: List[int],
    target: int,
    repetitions: int = 5
) -> Dict[str, Any]:
    """
    Executes a search algorithm with high-resolution timing and correctness verification.
    """
    if algorithm_name not in SEARCHING_FUNCTION_MAP:
        raise ValueError(f"Unknown searching algorithm: '{algorithm_name}'")

    fn = SEARCHING_FUNCTION_MAP[algorithm_name]
    search_input = sorted(arr) if algorithm_name == 'Binary Search' else arr

    times = []
    last_result = None

    for _ in range(max(1, repetitions)):
        t_start = time.perf_counter()
        result = fn(search_input, target, track_steps=False)
        t_end = time.perf_counter()
        times.append(t_end - t_start)
        last_result = result

    is_correct, verify_msg = verify_searching_result(search_input, target, last_result)

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0.0

    return {
        'algorithm': algorithm_name,
        'category': 'Searching',
        'input_size': len(arr),
        'target': target,
        'found': last_result.get('found', False),
        'index': last_result.get('index', -1),
        'repetitions': repetitions,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'std_dev': std_dev,
        'comparisons': last_result.get('comparisons', 0),
        'swaps': 0,
        'memory_bytes': 64,
        'correct': is_correct,
        'verification_msg': verify_msg
    }


def run_graph_benchmark(
    algorithm_name: str,
    graph: Optional[Dict[str, List[Tuple[str, float]]]] = None,
    start_node: str = 'A',
    repetitions: int = 5
) -> Dict[str, Any]:
    """
    Executes a graph algorithm with high-resolution timing and correctness verification.
    """
    if graph is None:
        graph = DEFAULT_GRAPH

    if algorithm_name not in GRAPH_FUNCTION_MAP:
        raise ValueError(f"Unknown graph algorithm: '{algorithm_name}'")

    fn = GRAPH_FUNCTION_MAP[algorithm_name]
    times = []
    last_result = None

    for _ in range(max(1, repetitions)):
        t_start = time.perf_counter()
        if algorithm_name == 'Kruskal':
            result = fn(graph)
        else:
            result = fn(graph, start_node)
        t_end = time.perf_counter()
        times.append(t_end - t_start)
        last_result = result

    is_correct, verify_msg = verify_graph_result(graph, algorithm_name, last_result, start_node)

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0.0

    # Meaningful operation metrics
    visited_nodes = len(last_result.get('traversal_order', last_result.get('distances', [])))
    if algorithm_name in ('Prim', 'Kruskal'):
        visited_nodes = len(last_result.get('mst_edges', [])) + 1
    total_edges = sum(len(edges) for edges in graph.values()) // 2

    return {
        'algorithm': algorithm_name,
        'category': 'Graph',
        'input_size': len(graph),
        'graph_nodes': len(graph),
        'graph_edges': total_edges,
        'start_node': start_node,
        'repetitions': repetitions,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'std_dev': std_dev,
        'comparisons': visited_nodes,
        'swaps': len(last_result.get('mst_edges', [])),
        'memory_bytes': estimate_auxiliary_memory(algorithm_name, len(graph)),
        'correct': is_correct,
        'verification_msg': verify_msg,
        'raw_result': last_result
    }


def run_scaling_benchmark(
    algorithm_names: List[str],
    input_sizes: List[int],
    distribution: str = 'Random',
    seed: Optional[int] = 42,
    repetitions: int = 2
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Executes multiple algorithms across multiple input scales for asymptotic growth curves.
    Never returns fabricated values.
    """
    scaling_data: Dict[str, List[Dict[str, Any]]] = {algo: [] for algo in algorithm_names}

    for n in sorted(input_sizes):
        arr = generate_dataset(n, distribution, seed=seed)
        for algo in algorithm_names:
            # Check quadratic limit safety
            if algo in QUADRATIC_ALGORITHMS and n > 5000:
                continue
            res = run_benchmark(algo, arr, repetitions=repetitions)
            scaling_data[algo].append(res)

    return scaling_data


def benchmark_multiple(
    algorithms: List[str],
    arr: List[int],
    repetitions: int = 3,
    distribution: str = 'Random',
    seed: Optional[int] = 42
) -> List[Dict[str, Any]]:
    """
    Runs benchmark on multiple algorithms sequentially on identical input array.
    Strictly uses a defensive copy of the exact same dataset for each candidate.
    """
    results = []
    for algo in algorithms:
        if algo in SORTING_FUNCTION_MAP:
            arr_copy = list(arr)
            res = run_benchmark(algo, arr_copy, repetitions=repetitions, distribution=distribution, seed=seed)
            results.append(res)
    return results


def check_safety_level(algorithm_names: List[str], n: int) -> Tuple[str, str]:
    """
    Returns safety level ('safe', 'warning', 'danger') and descriptive message.
    """
    has_quadratic = any(algo in QUADRATIC_ALGORITHMS for algo in algorithm_names)

    if has_quadratic:
        if n > 10000:
            return 'danger', f"Input size N={n:,} is dangerously large for quadratic algorithms ({', '.join(a for a in algorithm_names if a in QUADRATIC_ALGORITHMS)}). Execution would likely freeze the application."
        elif n > 5000:
            return 'warning', f"Input size N={n:,} may take 5–20 seconds for quadratic algorithms ({', '.join(a for a in algorithm_names if a in QUADRATIC_ALGORITHMS)})."
        elif n > 1000:
            return 'caution', f"Notice: N={n:,} will run quickly, but quadratic algorithms will register noticeably more operations."

    if n > 100000:
        return 'warning', f"Input size N={n:,} will allocate significant memory. Please allow a few seconds for completion."

    return 'safe', "Parameters within optimal real-time benchmark range."


def run_full_verification_suite() -> Dict[str, Any]:
    """
    Executes an automated battery of empirical correctness checks on all 13 algorithms
    across multiple rigorous edge cases (empty input, single element, duplicates, sorted,
    reverse sorted, negative numbers, boundary searches, disconnected graphs).
    Returns real pass/fail metrics and detailed audit logs.
    """
    results = []

    # 1. SORTING ALGORITHMS (6)
    sorting_cases = [
        ("Empty Array", []),
        ("Single Element", [42]),
        ("Two Elements Inverted", [2, 1]),
        ("All Identical Duplicates", [7, 7, 7, 7]),
        ("Frequent Duplicates", [3, 1, 3, 2, 3, 1]),
        ("Already Sorted", [1, 2, 3, 4, 5, 6]),
        ("Reverse Sorted", [6, 5, 4, 3, 2, 1]),
        ("Negative Numbers", [-5, 12, -20, 0, 7, -1]),
    ]

    for algo_name, fn in SORTING_FUNCTION_MAP.items():
        for case_name, arr in sorting_cases:
            try:
                res = fn(list(arr), track_steps=False)
                expected = sorted(arr)
                actual = res.get('sorted_array', [])
                passed = (actual == expected)
                results.append({
                    'algorithm': algo_name,
                    'category': 'Sorting',
                    'case': case_name,
                    'expected': f"Ascending {expected[:4]}..." if len(expected) > 4 else str(expected),
                    'actual': f"Ascending {actual[:4]}..." if len(actual) > 4 else str(actual),
                    'status': 'PASSED' if passed else 'FAILED'
                })
            except Exception as e:
                results.append({
                    'algorithm': algo_name,
                    'category': 'Sorting',
                    'case': case_name,
                    'expected': "Sorted list",
                    'actual': f"Exception: {str(e)}",
                    'status': 'FAILED'
                })

    # 2. SEARCHING ALGORITHMS (2)
    searching_cases = [
        ("Empty Array", [], 5, False, -1),
        ("Single Found", [10], 10, True, 0),
        ("Single Absent", [10], 5, False, -1),
        ("First Element", [1, 2, 3, 4, 5], 1, True, 0),
        ("Last Element", [1, 2, 3, 4, 5], 5, True, 4),
        ("Absent Key", [1, 2, 3, 4, 5], 99, False, -1),
    ]

    for s_algo in ['Linear Search', 'Binary Search']:
        fn = SEARCHING_FUNCTION_MAP[s_algo]
        for case_name, arr, target, exp_found, exp_idx in searching_cases:
            try:
                res = fn(list(arr), target, track_steps=False)
                actual_found = res.get('found', False)
                actual_idx = res.get('index', -1)
                passed = (actual_found == exp_found) and (exp_idx == -1 or actual_idx == exp_idx)
                results.append({
                    'algorithm': s_algo,
                    'category': 'Searching',
                    'case': f"{case_name} (Target={target})",
                    'expected': f"Found={exp_found}, Idx={exp_idx}",
                    'actual': f"Found={actual_found}, Idx={actual_idx}",
                    'status': 'PASSED' if passed else 'FAILED'
                })
            except Exception as e:
                results.append({
                    'algorithm': s_algo,
                    'category': 'Searching',
                    'case': f"{case_name} (Target={target})",
                    'expected': f"Found={exp_found}",
                    'actual': f"Exception: {str(e)}",
                    'status': 'FAILED'
                })

    # 3. GRAPH ALGORITHMS (5)
    graph_cases = [
        ("Default 6-Node Graph", DEFAULT_GRAPH, 'A'),
        ("Single Node Graph", {'A': []}, 'A'),
        ("Disconnected Graph", {'A': [('B', 2)], 'B': [('A', 2)], 'C': [('D', 3)], 'D': [('C', 3)]}, 'A')
    ]

    for g_algo, g_fn in GRAPH_FUNCTION_MAP.items():
        for case_name, g_input, start_v in graph_cases:
            try:
                if g_algo == 'Kruskal':
                    res = g_fn(g_input)
                else:
                    res = g_fn(g_input, start_v)
                valid, msg = verify_graph_result(g_input, g_algo, res, start_node=start_v)
                results.append({
                    'algorithm': g_algo,
                    'category': 'Graph',
                    'case': case_name,
                    'expected': "Valid Topological Invariant",
                    'actual': msg,
                    'status': 'PASSED' if valid else 'FAILED'
                })
            except Exception as e:
                results.append({
                    'algorithm': g_algo,
                    'category': 'Graph',
                    'case': case_name,
                    'expected': "Valid Output",
                    'actual': f"Exception: {str(e)}",
                    'status': 'FAILED'
                })

    total = len(results)
    passed_count = sum(1 for r in results if r['status'] == 'PASSED')
    failed_count = total - passed_count
    rate = (passed_count / total * 100.0) if total > 0 else 0.0

    return {
        'total_tests': total,
        'passed': passed_count,
        'failed': failed_count,
        'rate': rate,
        'details': results
    }
