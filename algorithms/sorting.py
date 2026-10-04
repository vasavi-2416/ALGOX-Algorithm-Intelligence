import sys
sys.setrecursionlimit(max(sys.getrecursionlimit(), 100000))
"""
ALGOX — Sorting Algorithms Module
Implements real manual sorting algorithms with rigorous operation counting and step tracing.
Provides deep execution state metadata (pass numbers, pointers, ranges, sorted regions)
for academically defensible visualization.
"""
from typing import List, Dict, Any, Tuple
import copy

def bubble_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Bubble Sort on array of size {n}',
            'array_state': list(a),
            'pass_number': 0,
            'sorted_region': [],
            'comparison_count': 0,
            'swap_count': 0
        })

    for i in range(n):
        swapped = False
        sorted_tail = list(range(n - i, n))
        for j in range(0, n - i - 1):
            comparisons += 1
            if track_steps:
                steps.append({
                    'type': 'compare',
                    'indices': [j, j + 1],
                    'compared_elements': [a[j], a[j + 1]],
                    'current_comparison': f'A[{j}] ({a[j]}) > A[{j+1}] ({a[j+1]})',
                    'description': f'Pass {i+1}: Comparing index {j} ({a[j]}) and index {j+1} ({a[j+1]})',
                    'array_state': list(a),
                    'pass_number': i + 1,
                    'sorted_region': sorted_tail,
                    'comparison_count': comparisons,
                    'swap_count': swaps
                })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
                if track_steps:
                    steps.append({
                        'type': 'swap',
                        'indices': [j, j + 1],
                        'swapped_elements': [a[j + 1], a[j]],
                        'description': f'Swapping index {j} ({a[j+1]}) with index {j+1} ({a[j]})',
                        'array_state': list(a),
                        'pass_number': i + 1,
                        'sorted_region': sorted_tail,
                        'comparison_count': comparisons,
                        'swap_count': swaps
                    })
        new_sorted_tail = list(range(n - i - 1, n))
        if track_steps:
            steps.append({
                'type': 'sorted',
                'indices': [n - i - 1],
                'description': f'Pass {i+1} complete. Element at index {n - i - 1} ({a[n - i - 1]}) is locked in sorted position',
                'array_state': list(a),
                'pass_number': i + 1,
                'sorted_region': new_sorted_tail,
                'comparison_count': comparisons,
                'swap_count': swaps
            })
        if not swapped:
            # Optimized bubble sort early exit
            break

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(n)),
            'description': 'Bubble Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'pass_number': n,
            'sorted_region': list(range(n)),
            'comparison_count': comparisons,
            'swap_count': swaps
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons,
        'swaps': swaps,
        'shifts': 0,
        'steps': steps
    }


def selection_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Selection Sort on array of size {n}',
            'array_state': list(a),
            'current_index': 0,
            'current_minimum': 0,
            'sorted_region': [],
            'comparison_count': 0,
            'swap_count': 0
        })

    for i in range(n):
        min_idx = i
        sorted_head = list(range(i))
        if track_steps:
            steps.append({
                'type': 'select',
                'indices': [min_idx],
                'description': f'Pass {i+1}: Assuming index {i} ({a[i]}) is initial minimum',
                'array_state': list(a),
                'current_index': i,
                'current_minimum': min_idx,
                'scanned_element': i,
                'sorted_region': sorted_head,
                'comparison_count': comparisons,
                'swap_count': swaps
            })
        for j in range(i + 1, n):
            comparisons += 1
            if track_steps:
                steps.append({
                    'type': 'compare',
                    'indices': [min_idx, j],
                    'description': f'Comparing candidate min at index {min_idx} ({a[min_idx]}) with index {j} ({a[j]})',
                    'array_state': list(a),
                    'current_index': i,
                    'current_minimum': min_idx,
                    'scanned_element': j,
                    'current_comparison': f'A[{j}] ({a[j]}) < min A[{min_idx}] ({a[min_idx]})',
                    'sorted_region': sorted_head,
                    'comparison_count': comparisons,
                    'swap_count': swaps
                })
            if a[j] < a[min_idx]:
                min_idx = j
                if track_steps:
                    steps.append({
                        'type': 'select',
                        'indices': [min_idx],
                        'description': f'New minimum found at index {min_idx} with value {a[min_idx]}',
                        'array_state': list(a),
                        'current_index': i,
                        'current_minimum': min_idx,
                        'minimum_update': True,
                        'scanned_element': j,
                        'sorted_region': sorted_head,
                        'comparison_count': comparisons,
                        'swap_count': swaps
                    })
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            if track_steps:
                steps.append({
                    'type': 'swap',
                    'indices': [i, min_idx],
                    'description': f'Swapping index {i} ({a[min_idx]}) with minimum index {min_idx} ({a[i]})',
                    'array_state': list(a),
                    'current_index': i,
                    'current_minimum': min_idx,
                    'swap': True,
                    'sorted_region': sorted_head,
                    'comparison_count': comparisons,
                    'swap_count': swaps
                })
        if track_steps:
            steps.append({
                'type': 'sorted',
                'indices': [i],
                'description': f'Index {i} ({a[i]}) is locked in sorted position',
                'array_state': list(a),
                'current_index': i,
                'sorted_region': list(range(i + 1)),
                'comparison_count': comparisons,
                'swap_count': swaps
            })

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(n)),
            'description': 'Selection Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'current_index': n,
            'sorted_region': list(range(n)),
            'comparison_count': comparisons,
            'swap_count': swaps
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons,
        'swaps': swaps,
        'shifts': 0,
        'steps': steps
    }


def insertion_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Insertion Sort on array of size {n}',
            'array_state': list(a),
            'key_element': None,
            'sorted_prefix': [0] if n > 0 else [],
            'comparison_count': 0,
            'shift_count': 0
        })

    for i in range(1, n):
        key = a[i]
        j = i - 1
        sorted_prefix = list(range(i))
        if track_steps:
            steps.append({
                'type': 'select',
                'indices': [i],
                'description': f'Picked key {key} at index {i} to insert into sorted prefix [0..{i-1}]',
                'array_state': list(a),
                'key_element': key,
                'key_index': i,
                'sorted_prefix': sorted_prefix,
                'comparison_count': comparisons,
                'shift_count': shifts
            })
        while j >= 0:
            comparisons += 1
            if track_steps:
                steps.append({
                    'type': 'compare',
                    'indices': [j, j + 1],
                    'description': f'Comparing key {key} with sorted prefix element A[{j}] ({a[j]})',
                    'array_state': list(a),
                    'key_element': key,
                    'key_index': i,
                    'compared_index': j,
                    'comparison': f'A[{j}] ({a[j]}) > key ({key})',
                    'sorted_prefix': sorted_prefix,
                    'comparison_count': comparisons,
                    'shift_count': shifts
                })
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                if track_steps:
                    steps.append({
                        'type': 'shift',
                        'indices': [j, j + 1],
                        'description': f'Shifting element {a[j]} right from index {j} to {j+1}',
                        'array_state': list(a),
                        'key_element': key,
                        'shifting': True,
                        'shifted_from': j,
                        'shifted_to': j + 1,
                        'sorted_prefix': sorted_prefix,
                        'comparison_count': comparisons,
                        'shift_count': shifts
                    })
                j -= 1
            else:
                break
        a[j + 1] = key
        new_sorted_prefix = list(range(i + 1))
        if track_steps:
            steps.append({
                'type': 'sorted',
                'indices': [j + 1],
                'description': f'Inserted key {key} into position {j+1}. Prefix [0..{i}] is sorted.',
                'array_state': list(a),
                'key_element': key,
                'insertion_position': j + 1,
                'sorted_prefix': new_sorted_prefix,
                'comparison_count': comparisons,
                'shift_count': shifts
            })

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(n)),
            'description': 'Insertion Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'key_element': None,
            'sorted_prefix': list(range(n)),
            'comparison_count': comparisons,
            'shift_count': shifts
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons,
        'swaps': 0,
        'shifts': shifts,
        'steps': steps
    }


def merge_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    comparisons = [0]
    swaps = [0]
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Merge Sort on array of size {len(a)}',
            'array_state': list(a),
            'left_range': [0, len(a) // 2],
            'right_range': [len(a) // 2 + 1, len(a) - 1],
            'merged_range': []
        })

    def _merge_sort_recursive(left: int, right: int):
        if left >= right:
            return
        mid = (left + right) // 2
        if track_steps:
            steps.append({
                'type': 'divide',
                'indices': [mid],
                'description': f'Divide: bisecting subarray [{left}..{right}] into left [{left}..{mid}] and right [{mid+1}..{right}]',
                'array_state': list(a),
                'divide_operation': True,
                'left_range': [left, mid],
                'right_range': [mid + 1, right],
                'merged_range': [left, right]
            })
        _merge_sort_recursive(left, mid)
        _merge_sort_recursive(mid + 1, right)
        _merge(left, mid, right)

    def _merge(left: int, mid: int, right: int):
        left_sub = a[left:mid + 1]
        right_sub = a[mid + 1:right + 1]
        i = 0
        j = 0
        k = left

        if track_steps:
            steps.append({
                'type': 'merge',
                'indices': list(range(left, right + 1)),
                'description': f'Combine: Merging sorted slices [{left}..{mid}] ({left_sub}) and [{mid+1}..{right}] ({right_sub})',
                'array_state': list(a),
                'merge_operation': True,
                'left_range': [left, mid],
                'right_range': [mid + 1, right],
                'merged_range': [left, right]
            })

        while i < len(left_sub) and j < len(right_sub):
            comparisons[0] += 1
            if track_steps:
                steps.append({
                    'type': 'compare',
                    'indices': [left + i, mid + 1 + j],
                    'description': f'Comparing left {left_sub[i]} (idx {left+i}) with right {right_sub[j]} (idx {mid+1+j})',
                    'array_state': list(a),
                    'comparison': f'left[{i}] ({left_sub[i]}) <= right[{j}] ({right_sub[j]})',
                    'left_range': [left, mid],
                    'right_range': [mid + 1, right],
                    'merged_range': [left, right]
                })
            if left_sub[i] <= right_sub[j]:
                a[k] = left_sub[i]
                i += 1
            else:
                a[k] = right_sub[j]
                j += 1
                swaps[0] += 1
            if track_steps:
                steps.append({
                    'type': 'shift',
                    'indices': [k],
                    'description': f'Placed merged element {a[k]} at position {k}',
                    'array_state': list(a),
                    'merge_operation': True,
                    'left_range': [left, mid],
                    'right_range': [mid + 1, right],
                    'merged_range': [left, k]
                })
            k += 1

        while i < len(left_sub):
            a[k] = left_sub[i]
            i += 1
            k += 1

        while j < len(right_sub):
            a[k] = right_sub[j]
            j += 1
            k += 1

        if track_steps:
            steps.append({
                'type': 'sorted',
                'indices': list(range(left, right + 1)),
                'description': f'Merged slice [{left}..{right}] is now sorted: {a[left:right+1]}',
                'array_state': list(a),
                'left_range': [left, mid],
                'right_range': [mid + 1, right],
                'merged_range': [left, right]
            })

    if len(a) > 0:
        _merge_sort_recursive(0, len(a) - 1)

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(len(a))),
            'description': 'Merge Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'merged_range': list(range(len(a)))
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons[0],
        'swaps': swaps[0],
        'shifts': 0,
        'steps': steps
    }


def quick_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    comparisons = [0]
    swaps = [0]
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Quick Sort on array of size {len(a)}',
            'array_state': list(a),
            'pivot': None,
            'left_pointer': 0,
            'right_pointer': len(a) - 1,
            'recursive_range': [0, len(a) - 1]
        })

    def _quick_sort(low: int, high: int):
        if low < high:
            pi = _partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    def _partition(low: int, high: int) -> int:
        pivot = a[high]
        if track_steps:
            steps.append({
                'type': 'pivot',
                'indices': [high],
                'description': f'Partition [{low}..{high}]: Selected pivot {pivot} at index {high}',
                'array_state': list(a),
                'pivot': pivot,
                'pivot_index': high,
                'left_pointer': low,
                'right_pointer': low,
                'recursive_range': [low, high]
            })
        i = low - 1
        for j in range(low, high):
            comparisons[0] += 1
            if track_steps:
                steps.append({
                    'type': 'compare',
                    'indices': [j, high],
                    'description': f'Comparing element A[{j}] ({a[j]}) with pivot {pivot}',
                    'array_state': list(a),
                    'pivot': pivot,
                    'pivot_index': high,
                    'left_pointer': i,
                    'right_pointer': j,
                    'comparison': f'A[{j}] ({a[j]}) <= pivot ({pivot})',
                    'recursive_range': [low, high]
                })
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps[0] += 1
                    if track_steps:
                        steps.append({
                            'type': 'swap',
                            'indices': [i, j],
                            'description': f'Partition swap: moved smaller element {a[i]} to index {i} and {a[j]} to {j}',
                            'array_state': list(a),
                            'pivot': pivot,
                            'left_pointer': i,
                            'right_pointer': j,
                            'recursive_range': [low, high]
                        })
        a[i + 1], a[high] = a[high], a[i + 1]
        swaps[0] += 1
        pivot_idx = i + 1
        if track_steps:
            steps.append({
                'type': 'sorted',
                'indices': [pivot_idx],
                'description': f'Pivot {pivot} locked in final sorted position at index {pivot_idx}',
                'array_state': list(a),
                'pivot': pivot,
                'pivot_index': pivot_idx,
                'left_pointer': i + 1,
                'right_pointer': high,
                'partition_boundary': pivot_idx,
                'recursive_range': [low, high]
            })
        return pivot_idx

    if len(a) > 0:
        _quick_sort(0, len(a) - 1)

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(len(a))),
            'description': 'Quick Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'pivot': None,
            'recursive_range': [0, len(a) - 1]
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons[0],
        'swaps': swaps[0],
        'shifts': 0,
        'steps': steps
    }


def heap_sort(arr: List[int], track_steps: bool = False) -> Dict[str, Any]:
    a = list(arr)
    n = len(a)
    comparisons = [0]
    swaps = [0]
    steps = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'description': f'Starting Heap Sort on array of size {n}',
            'array_state': list(a),
            'heap_construction': True,
            'heap_size': n,
            'sorted_region': []
        })

    if n <= 1:
        if track_steps and n == 1:
            steps.append({
                'type': 'sorted',
                'indices': [0],
                'description': 'Single element array is trivially sorted.',
                'array_state': list(a),
                'heap_size': 0,
                'sorted_region': [0]
            })
        if track_steps:
            steps.append({
                'type': 'complete',
                'indices': list(range(n)),
                'description': 'Heap Sort completed. Array is fully sorted.',
                'array_state': list(a),
                'heap_size': 0,
                'sorted_region': list(range(n))
            })
        return {
            'sorted_array': a,
            'comparisons': 0,
            'swaps': 0,
            'shifts': 0,
            'steps': steps
        }

    def _heapify(n_size: int, i: int, phase: str = 'Heap Construction'):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n_size:
            comparisons[0] += 1
            if a[left] > a[largest]:
                largest = left

        if right < n_size:
            comparisons[0] += 1
            if a[right] > a[largest]:
                largest = right

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps[0] += 1
            if track_steps:
                steps.append({
                    'type': 'heapify',
                    'indices': [i, largest],
                    'description': f'{phase}: Sifted down parent A[{i}] with larger child A[{largest}] ({a[i]})',
                    'array_state': list(a),
                    'parent_index': i,
                    'child_index': largest,
                    'heap_size': n_size,
                    'heapify_step': True,
                    'sorted_region': list(range(n_size, n))
                })
            _heapify(n_size, largest, phase)

    # Build max heap (bottom-up in O(n))
    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i, 'Heap Construction')

    if track_steps:
        steps.append({
            'type': 'pivot',
            'indices': [0],
            'description': f'Max-Heap construction complete. Maximum root element is {a[0]}',
            'array_state': list(a),
            'heap_construction': False,
            'heap_size': n,
            'sorted_region': []
        })

    # Extract elements one by one from root
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps[0] += 1
        if track_steps:
            steps.append({
                'type': 'swap',
                'indices': [0, i],
                'description': f'Root Extraction: Extracted maximum {a[i]} to index {i}, moved tail to root',
                'array_state': list(a),
                'root_extraction': True,
                'extracted_value': a[i],
                'extracted_to': i,
                'heap_size': i,
                'sorted_region': list(range(i, n))
            })
            steps.append({
                'type': 'sorted',
                'indices': [i],
                'description': f'Index {i} ({a[i]}) is locked into its final sorted position',
                'array_state': list(a),
                'heap_size': i,
                'sorted_region': list(range(i, n))
            })
        _heapify(i, 0, 'Extract Phase')

    if n > 0 and track_steps:
        steps.append({
            'type': 'sorted',
            'indices': [0],
            'description': f'Index 0 ({a[0]}) is in final sorted position',
            'array_state': list(a),
            'heap_size': 0,
            'sorted_region': list(range(n))
        })

    if track_steps:
        steps.append({
            'type': 'complete',
            'indices': list(range(n)),
            'description': 'Heap Sort completed. Array is fully sorted.',
            'array_state': list(a),
            'heap_size': 0,
            'sorted_region': list(range(n))
        })

    return {
        'sorted_array': a,
        'comparisons': comparisons[0],
        'swaps': swaps[0],
        'shifts': 0,
        'steps': steps
    }
