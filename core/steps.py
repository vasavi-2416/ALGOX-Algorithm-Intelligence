"""
ALGOX — Step Trace Generator Module
Generates granular step-by-step visualizer states for sorting and searching algorithms.
"""
from typing import List, Dict, Any, Optional
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

def get_sorting_steps(algorithm_name: str, arr: List[int]) -> Dict[str, Any]:
    """
    Executes a sorting algorithm with track_steps=True and formats the trace for the visualizer.
    """
    algo_map = {
        'Bubble Sort': bubble_sort,
        'Selection Sort': selection_sort,
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort
    }

    if algorithm_name not in algo_map:
        raise ValueError(f"Visualizer step generation not available for '{algorithm_name}'")

    fn = algo_map[algorithm_name]
    result = fn(arr, track_steps=True)
    return result


def get_searching_steps(algorithm_name: str, arr: List[int], target: int) -> Dict[str, Any]:
    """
    Executes a searching algorithm with track_steps=True and formats the trace for the visualizer.
    """
    if algorithm_name == 'Linear Search':
        return linear_search(arr, target, track_steps=True)
    elif algorithm_name == 'Binary Search':
        # Binary search requires sorted array
        sorted_arr = sorted(arr)
        return binary_search(sorted_arr, target, track_steps=True)
    else:
        raise ValueError(f"Unknown searching algorithm: '{algorithm_name}'")
