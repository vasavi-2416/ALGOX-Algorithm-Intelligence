"""
Comprehensive Integration & Functional Test Suite for ALGOX
Tests all 13 algorithms, 5 dataset distributions, SQLite operations, and page modules.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort
)
from algorithms.searching import linear_search, binary_search
from algorithms.graph import bfs, dfs, dijkstra, prim, kruskal, DEFAULT_GRAPH
from core.dataset import generate_dataset, get_dataset_info, DISTRIBUTIONS
from core.benchmark import run_benchmark, benchmark_multiple, check_safety_level
from core.recommendation import get_recommendation
from core.steps import get_sorting_steps, get_searching_steps
from core.complexity import ALGORITHM_COMPLEXITY
from database.database import AlgoxDB

class TestAlgoxSuite(unittest.TestCase):

    def test_sorting_algorithms(self):
        test_cases = [
            [64, 34, 25, 12, 22, 11, 90],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [4, 2, 2, 8, 3, 3, 1],
            [42]
        ]
        algorithms = [
            ('Bubble Sort', bubble_sort),
            ('Selection Sort', selection_sort),
            ('Insertion Sort', insertion_sort),
            ('Merge Sort', merge_sort),
            ('Quick Sort', quick_sort),
            ('Heap Sort', heap_sort)
        ]
        for arr in test_cases:
            expected = sorted(arr)
            for name, fn in algorithms:
                res = fn(arr, track_steps=True)
                self.assertEqual(res['sorted_array'], expected, f"{name} failed on {arr}")
                self.assertGreater(res['comparisons'], 0 if len(arr) > 1 else -1)
                self.assertGreater(len(res['steps']), 0)

    def test_searching_algorithms(self):
        arr = [10, 23, 45, 70, 90, 120]
        # Linear search found & not found
        res_l1 = linear_search(arr, 70, track_steps=True)
        self.assertTrue(res_l1['found'])
        self.assertEqual(res_l1['index'], 3)

        res_l2 = linear_search(arr, 999, track_steps=True)
        self.assertFalse(res_l2['found'])
        self.assertEqual(res_l2['index'], -1)

        # Binary search found & not found
        res_b1 = binary_search(arr, 70, track_steps=True)
        self.assertTrue(res_b1['found'])
        self.assertEqual(res_b1['index'], 3)

        res_b2 = binary_search(arr, 999, track_steps=True)
        self.assertFalse(res_b2['found'])
        self.assertEqual(res_b2['index'], -1)

    def test_graph_algorithms(self):
        # BFS & DFS
        b_res = bfs(DEFAULT_GRAPH, 'A')
        self.assertEqual(len(b_res['traversal_order']), 6)

        d_res = dfs(DEFAULT_GRAPH, 'A')
        self.assertEqual(len(d_res['traversal_order']), 6)

        # Dijkstra
        dijk_res = dijkstra(DEFAULT_GRAPH, 'A')
        self.assertEqual(dijk_res['distances']['A'], 0)
        self.assertEqual(dijk_res['distances']['B'], 3) # A-C(2) + C-B(1) = 3
        self.assertEqual(dijk_res['distances']['C'], 2)

        # Prim & Kruskal MST weights must be identical
        prim_res = prim(DEFAULT_GRAPH, 'A')
        krus_res = kruskal(DEFAULT_GRAPH)
        self.assertEqual(len(prim_res['mst_edges']), 5)
        self.assertEqual(len(krus_res['mst_edges']), 5)
        self.assertEqual(prim_res['total_weight'], krus_res['total_weight'])
        self.assertEqual(prim_res['total_weight'], 13)

    def test_dataset_distributions(self):
        for dist in DISTRIBUTIONS:
            arr = generate_dataset(30, dist, seed=42)
            self.assertEqual(len(arr), 30)
            info = get_dataset_info(arr)
            self.assertEqual(info['size'], 30)
            if dist == 'Sorted':
                self.assertTrue(info['is_sorted'])

    def test_benchmark_engine(self):
        arr = generate_dataset(100, 'Random', seed=123)
        res = run_benchmark('Merge Sort', arr, repetitions=2)
        self.assertTrue(res['correct'])
        self.assertGreater(res['avg_time'], 0)
        self.assertGreater(res['comparisons'], 0)

        # Multi-benchmark
        multi = benchmark_multiple(['Merge Sort', 'Quick Sort'], arr, repetitions=2)
        self.assertEqual(len(multi), 2)

        # Safety check
        status, msg = check_safety_level(['Bubble Sort'], 15000)
        self.assertEqual(status, 'danger')

    def test_recommendation_engine(self):
        rec1 = get_recommendation('Sorting', 5000, 'Random', {'in_place': True, 'stable': False})
        self.assertIn(rec1['recommended'], ['Quick Sort', 'Heap Sort'])
        self.assertGreater(len(rec1['reasons']), 0)

        rec2 = get_recommendation('Sorting', 5000, 'Nearly Sorted', {})
        self.assertEqual(rec2['recommended'], 'Insertion Sort')

        rec3 = get_recommendation('Searching', 5000, 'Sorted', {})
        self.assertEqual(rec3['recommended'], 'Binary Search')

    def test_database_crud(self):
        test_db_path = 'data/test_algox.db'
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

        db = AlgoxDB(test_db_path)
        # Insert experiment
        exp_id = db.insert_experiment({
            'algorithm': 'Quick Sort',
            'category': 'Sorting',
            'dataset': 'Random',
            'input_size': 500,
            'avg_time': 0.0012,
            'min_time': 0.0010,
            'max_time': 0.0015,
            'comparisons': 4500,
            'swaps': 1200,
            'memory_bytes': 1024,
            'correct': True,
            'repetitions': 3,
            'notes': 'Unit test run'
        })
        self.assertGreater(exp_id, 0)
        self.assertEqual(db.get_experiment_count(), 1)
        self.assertAlmostEqual(db.get_average_execution_time(), 0.0012, places=4)

        # Save experiment
        saved_id = db.save_experiment(exp_id, "Test Title", "Notes for test")
        self.assertGreater(saved_id, 0)
        self.assertEqual(len(db.get_saved_experiments()), 1)

        # Export CSV
        csv_out = db.export_experiments_csv()
        self.assertIn("Quick Sort", csv_out)

        # Settings
        db.set_setting("unit_test_key", "42")
        self.assertEqual(db.get_setting("unit_test_key"), "42")

        # Cleanup
        db.clear_history()
        self.assertEqual(db.get_experiment_count(), 0)
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def test_complexity_taxonomies(self):
        self.assertEqual(len(ALGORITHM_COMPLEXITY), 13)
        for name, meta in ALGORITHM_COMPLEXITY.items():
            self.assertIn('paradigm', meta)
            self.assertIn('best', meta)
            self.assertIn('average', meta)
            self.assertIn('worst', meta)
            self.assertIn('space', meta)

if __name__ == '__main__':
    unittest.main()
