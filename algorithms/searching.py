"""
ALGOX — Searching Algorithms Module
Implements Linear Search and Binary Search with step tracing.
Provides comprehensive execution state telemetry (low, mid, high, target, comparisons, eliminated intervals)
for academically rigorous visualization.
"""
from typing import List, Dict, Any, Optional

def linear_search(arr: List[int], target: int, track_steps: bool = False) -> Dict[str, Any]:
    comparisons = 0
    steps = []
    found_idx = -1

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'target': target,
            'current_index': None,
            'current_value': None,
            'comparison': None,
            'comparisons': 0,
            'found': False,
            'final_index': None,
            'description': f'Starting Linear Search for target {target} in array of length {len(arr)}',
            'array_state': list(arr)
        })

    for i in range(len(arr)):
        comparisons += 1
        comp_str = f'A[{i}] ({arr[i]}) == target ({target})'
        if track_steps:
            steps.append({
                'type': 'compare',
                'indices': [i],
                'target': target,
                'current_index': i,
                'current_value': arr[i],
                'comparison': comp_str,
                'comparisons': comparisons,
                'found': False,
                'final_index': None,
                'description': f'Step {comparisons}: Inspecting element at index {i} (value: {arr[i]}) vs target {target}',
                'array_state': list(arr)
            })
        if arr[i] == target:
            found_idx = i
            if track_steps:
                steps.append({
                    'type': 'found',
                    'indices': [i],
                    'target': target,
                    'current_index': i,
                    'current_value': arr[i],
                    'comparison': f'{arr[i]} == {target} (MATCH)',
                    'comparisons': comparisons,
                    'found': True,
                    'final_index': i,
                    'description': f'Target {target} FOUND at index {i} after {comparisons} comparisons',
                    'array_state': list(arr)
                })
            break

    if found_idx == -1 and track_steps:
        steps.append({
            'type': 'not_found',
            'indices': [],
            'target': target,
            'current_index': len(arr) - 1,
            'current_value': arr[-1] if arr else None,
            'comparison': 'All elements evaluated (NO MATCH)',
            'comparisons': comparisons,
            'found': False,
            'final_index': -1,
            'description': f'Target {target} NOT FOUND after scanning all {len(arr)} elements ({comparisons} comparisons)',
            'array_state': list(arr)
        })

    return {
        'index': found_idx,
        'comparisons': comparisons,
        'found': found_idx != -1,
        'steps': steps
    }


def binary_search(arr: List[int], target: int, track_steps: bool = False) -> Dict[str, Any]:
    comparisons = 0
    steps = []
    low = 0
    high = len(arr) - 1
    found_idx = -1
    low_high_history = []

    if track_steps:
        steps.append({
            'type': 'start',
            'indices': [],
            'low': low,
            'mid': -1,
            'high': high,
            'target': target,
            'current_value': None,
            'comparison': None,
            'comparisons': 0,
            'eliminated_region': [],
            'found': False,
            'final_index': None,
            'description': f'Starting Binary Search for target {target}. Range [0..{high}]',
            'array_state': list(arr)
        })

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        low_high_history.append((low, mid, high))
        comp_str = f'A[{mid}] ({arr[mid]}) vs target ({target})'
        eliminated = list(range(0, low)) + list(range(high + 1, len(arr)))

        if track_steps:
            steps.append({
                'type': 'inspect',
                'indices': [mid],
                'low': low,
                'mid': mid,
                'high': high,
                'target': target,
                'current_value': arr[mid],
                'comparison': comp_str,
                'comparisons': comparisons,
                'eliminated_region': eliminated,
                'found': False,
                'final_index': None,
                'description': f'Step {comparisons}: Checking midpoint index {mid} (value: {arr[mid]}) in interval [{low}..{high}]',
                'array_state': list(arr)
            })

        if arr[mid] == target:
            found_idx = mid
            if track_steps:
                steps.append({
                    'type': 'found',
                    'indices': [mid],
                    'low': low,
                    'mid': mid,
                    'high': high,
                    'target': target,
                    'current_value': arr[mid],
                    'comparison': f'{arr[mid]} == {target} (EQUAL)',
                    'comparisons': comparisons,
                    'eliminated_region': eliminated,
                    'found': True,
                    'final_index': mid,
                    'description': f'Target {target} FOUND at index {mid} after {comparisons} comparisons!',
                    'array_state': list(arr)
                })
            break
        elif arr[mid] < target:
            old_low = low
            low = mid + 1
            new_elim = list(range(0, low)) + list(range(high + 1, len(arr)))
            if track_steps:
                steps.append({
                    'type': 'eliminate',
                    'indices': list(range(old_low, mid + 1)),
                    'low': low,
                    'mid': mid,
                    'high': high,
                    'target': target,
                    'current_value': arr[mid],
                    'comparison': f'{arr[mid]} < {target} (Target is in right half)',
                    'comparisons': comparisons,
                    'eliminated_region': new_elim,
                    'found': False,
                    'final_index': None,
                    'description': f'{arr[mid]} < {target}: Eliminated left half [{old_low}..{mid}]. New search interval [{low}..{high}]',
                    'array_state': list(arr)
                })
        else:
            old_high = high
            high = mid - 1
            new_elim = list(range(0, low)) + list(range(high + 1, len(arr)))
            if track_steps:
                steps.append({
                    'type': 'eliminate',
                    'indices': list(range(mid, old_high + 1)),
                    'low': low,
                    'mid': mid,
                    'high': high,
                    'target': target,
                    'current_value': arr[mid],
                    'comparison': f'{arr[mid]} > {target} (Target is in left half)',
                    'comparisons': comparisons,
                    'eliminated_region': new_elim,
                    'found': False,
                    'final_index': None,
                    'description': f'{arr[mid]} > {target}: Eliminated right half [{mid}..{old_high}]. New search interval [{low}..{high}]',
                    'array_state': list(arr)
                })

    if found_idx == -1 and track_steps:
        steps.append({
            'type': 'not_found',
            'indices': [],
            'low': low,
            'mid': -1,
            'high': high,
            'target': target,
            'current_value': None,
            'comparison': 'low > high (Interval exhausted)',
            'comparisons': comparisons,
            'eliminated_region': list(range(len(arr))),
            'found': False,
            'final_index': -1,
            'description': f'Target {target} NOT FOUND. Interval exhausted after {comparisons} comparisons.',
            'array_state': list(arr)
        })

    return {
        'index': found_idx,
        'comparisons': comparisons,
        'found': found_idx != -1,
        'low_high_history': low_high_history,
        'steps': steps
    }
