"""
ALGOX — Algorithm Recommendation Engine
Explainable, rule-based algorithmic decision engine derived from asymptotic bounds and empirical characteristics.
Does not use arbitrary machine learning heuristics; utilizes deterministic algorithmic logic.
"""
from typing import Dict, Any, List, Optional
from core.complexity import ALGORITHM_COMPLEXITY

def get_recommendation(
    problem_type: str,
    input_size: int,
    distribution: str,
    constraints: Optional[Dict[str, Any]] = None,
    priority: str = 'Balanced'
) -> Dict[str, Any]:
    """
    Evaluates algorithmic criteria and returns mathematically justified recommendations.
    """
    if constraints is None:
        constraints = {}

    req_in_place = constraints.get('in_place', False)
    req_stable = constraints.get('stable', False)
    is_nearly_sorted = constraints.get('nearly_sorted', False) or (distribution in ['Sorted', 'Nearly Sorted'])
    is_reverse_sorted = (distribution == 'Reverse Sorted')
    is_duplicate_heavy = constraints.get('heavy_duplicates', False) or (distribution == 'Duplicate Heavy')

    # Priority overrides from user
    if priority == 'Memory' or constraints.get('priority') == 'Memory':
        req_in_place = True
    if priority == 'Stability' or constraints.get('priority') == 'Stability':
        req_stable = True

    if problem_type == 'Searching':
        if distribution == 'Sorted' or constraints.get('is_sorted', False):
            return {
                'recommended': 'Binary Search',
                'paradigm': 'Divide and Conquer',
                'trade_off': 'Strict precondition: the input dataset must be sorted in advance. If the collection is unsorted and queried only once, the O(n log n) sorting phase will dominate the O(log n) search benefits.',
                'reasons': [
                    'The input array is already sorted, enabling O(log n) logarithmic halving of search space.',
                    f'For input size N={input_size:,}, Binary Search will require at most ~{max(1, input_size.bit_length())} comparisons.',
                    'Zero auxiliary space overhead (O(1) in-place pointers).',
                    'Optimal worst-case asymptotic bounds for comparison-based static search.'
                ],
                'alternatives': [
                    {
                        'name': 'Linear Search',
                        'reason': 'Requires scanning on average N/2 elements, which is vastly inferior to log₂(N) on sorted sequences.'
                    }
                ],
                'rule_applied': 'Sorted dataset precondition met → Binary Search.'
            }
        else:
            return {
                'recommended': 'Linear Search',
                'paradigm': 'Sequential / Brute Force',
                'trade_off': 'Linear complexity O(n) becomes prohibitive if frequent repeated searches are performed on static datasets without indexing.',
                'reasons': [
                    'The input is unsorted. Sorting first (O(n log n)) just to perform a single Binary Search (O(log n)) incurs higher total latency than scanning in O(n).',
                    'No preprocessing or auxiliary data structure allocation overhead required.',
                    'Operates seamlessly on arbitrary input sequences, non-contiguous collections, and live streams.'
                ],
                'alternatives': [
                    {
                        'name': 'Binary Search',
                        'reason': 'Unsorted data violates the fundamental bisection invariant. Sorting first requires O(n log n).'
                    }
                ],
                'rule_applied': 'Unsorted one-off query → Linear Search.'
            }

    # Sorting Recommendations
    # Priority: Simplicity
    if priority == 'Simplicity':
        if is_nearly_sorted or input_size <= 100:
            return {
                'recommended': 'Insertion Sort',
                'paradigm': 'Incremental / Adaptive',
                'trade_off': 'Will scale quadratically (O(n²)) if input size expands significantly or becomes completely inverted.',
                'reasons': [
                    'Extremely straightforward, readable implementation with minimal code footprint.',
                    'Zero recursion stack frames or heap memory management.',
                    'Operates in-place with O(1) auxiliary variables.'
                ],
                'alternatives': [
                    {'name': 'Bubble Sort', 'reason': 'Similar simplicity but performs significantly more redundant swaps.'},
                    {'name': 'Selection Sort', 'reason': 'Simple but always performs O(n²) comparisons even on sorted inputs.'}
                ],
                'rule_applied': 'Simplicity priority on small/ordered data → Insertion Sort.'
            }

    # Rule 1: Very small array (N <= 32)
    if input_size <= 32:
        return {
            'recommended': 'Insertion Sort',
            'paradigm': 'Incremental / Adaptive',
            'trade_off': 'Quadratic scaling makes it strictly confined to small subarrays (N <= 32); unsuitable as standalone sort on large datasets.',
            'reasons': [
                f'For tiny input sizes (N={input_size}), Insertion Sort has minimal constant overhead compared to recursive algorithms.',
                'Strictly in-place with O(1) auxiliary space.',
                'Completely stable — preserves identical key order.',
                'Low instruction cache pressure and branch mispredictions on modern processors.'
            ],
            'alternatives': [
                {
                    'name': 'Merge Sort',
                    'reason': 'Guaranteed O(n log n), but recursion and buffer allocation overhead exceeds benefits for N <= 32.'
                },
                {
                    'name': 'Quick Sort',
                    'reason': 'Partitioning setup and recursion frames add unnecessary constant factors for tiny N.'
                }
            ],
            'rule_applied': 'Small size threshold (N <= 32) → Insertion Sort.'
        }

    # Rule 2: Nearly sorted or sorted data
    if is_nearly_sorted:
        return {
            'recommended': 'Insertion Sort',
            'paradigm': 'Incremental / Adaptive',
            'trade_off': 'Performance drops sharply to O(n²) if the nearly-sorted assumption is violated and input has high inversion count.',
            'reasons': [
                'On pre-sorted or nearly-sorted data, Insertion Sort operates in near-linear time O(n).',
                'Inner while-loop terminates almost immediately for elements already near their final positions.',
                'Strictly in-place: O(1) auxiliary memory.',
                'Preserves original key ordering (Stable).'
            ],
            'alternatives': [
                {
                    'name': 'Merge Sort',
                    'reason': 'Runs in O(n log n) even on sorted data, requiring unnecessary divisions and O(n) memory.'
                },
                {
                    'name': 'Quick Sort',
                    'reason': 'Standard Quick Sort with rightmost pivot degrades to O(n²) worst-case on already sorted inputs.'
                }
            ],
            'rule_applied': 'Nearly-sorted distribution optimization → Insertion Sort.'
        }

    # Rule 3: Strict in-place requirement / Memory priority with guaranteed O(n log n)
    if (req_in_place or priority == 'Memory') and not req_stable:
        if is_reverse_sorted or priority == 'Worst-Case Guarantee':
            return {
                'recommended': 'Heap Sort',
                'paradigm': 'Heap-Based Approach',
                'trade_off': 'Non-contiguous heap child index traversal (2i+1, 2i+2) produces frequent CPU L1/L2 cache misses, running 2-3x slower than Quick Sort on uniform random memory.',
                'reasons': [
                    'Guaranteed O(n log n) runtime across best, average, and worst-case scenarios.',
                    'Strict O(1) auxiliary memory (does not use recursive call stack frames).',
                    'Immunized against Quick Sort’s quadratic O(n²) pitfall on reverse-sorted data.',
                    'Build-heap phase runs in linear O(n) time before extraction.'
                ],
                'alternatives': [
                    {
                        'name': 'Quick Sort',
                        'reason': 'May degenerate toward O(n²) if pivot choice aligns unfavorably with reverse ordering.'
                    },
                    {
                        'name': 'Merge Sort',
                        'reason': 'Requires O(n) auxiliary allocation, violating the strict in-place constraint.'
                    }
                ],
                'rule_applied': 'Strict in-place + worst-case bounds → Heap Sort.'
            }
        else:
            return {
                'recommended': 'Quick Sort',
                'paradigm': 'Divide and Conquer',
                'trade_off': 'Worst-case performance degrades to O(n²) on specific adversarial inputs or pre-sorted sequences without median-of-three or randomized pivot selection.',
                'reasons': [
                    'Fastest general-purpose sorting algorithm in practical execution benchmarks.',
                    'In-place operation (only O(log n) stack frame depth).',
                    'Optimal CPU cache line locality during sequential partition scans.',
                    'Significantly smaller constant factor overhead than Heap Sort.'
                ],
                'alternatives': [
                    {
                        'name': 'Heap Sort',
                        'reason': 'Guarantees O(n log n) worst-case with O(1) memory, but has higher constant factors due to cache misses.'
                    },
                    {
                        'name': 'Merge Sort',
                        'reason': 'Requires O(n) memory allocation, violating in-place requirement.'
                    }
                ],
                'rule_applied': 'General in-place high-performance sorting → Quick Sort.'
            }

    # Rule 4: Strict stability requirement / Stability priority
    if req_stable or priority == 'Stability':
        return {
            'recommended': 'Merge Sort',
            'paradigm': 'Divide and Conquer',
            'trade_off': 'Requires O(n) auxiliary array buffer memory allocation, which may be prohibitive on memory-constrained embedded systems.',
            'reasons': [
                'Guarantees stable sorting (relative order of identical keys is strictly preserved).',
                'Deterministic O(n log n) upper bound regardless of input order or distribution.',
                'Predictable comparison counts and parallelizable merge stages.',
                'Well suited for objects with secondary sort criteria.'
            ],
            'alternatives': [
                {
                    'name': 'Insertion Sort',
                    'reason': 'Also stable, but scales with O(n²), making it unviable for large N.'
                },
                {
                    'name': 'Quick Sort',
                    'reason': 'Standard partitioning swaps non-adjacent elements, destroying stability.'
                }
            ],
            'rule_applied': 'Stability requirement + large N → Merge Sort.'
        }

    # Rule 5: Heavy duplicates
    if is_duplicate_heavy:
        return {
            'recommended': 'Merge Sort',
            'paradigm': 'Divide and Conquer',
            'trade_off': 'Requires O(n) auxiliary memory allocation for buffering merge regions.',
            'reasons': [
                'Consistent O(n log n) performance immune to duplicate key skew.',
                'Preserves stability across large groups of identical values.',
                'Quick Sort standard Lomuto partition can degrade if many elements equal the pivot.'
            ],
            'alternatives': [
                {
                    'name': 'Heap Sort',
                    'reason': 'Maintains O(n log n) without auxiliary memory, but lacks stability.'
                },
                {
                    'name': 'Quick Sort',
                    'reason': 'Requires 3-way Dijkstra Dutch Flag partitioning to avoid quadratic degradation on duplicate-heavy data.'
                }
            ],
            'rule_applied': 'Duplicate-heavy keys without 3-way partition → Merge Sort.'
        }

    # Default general-purpose case (Balanced / Speed priority)
    return {
        'recommended': 'Quick Sort',
        'paradigm': 'Divide and Conquer',
        'trade_off': 'Worst-case execution degrades to O(n²) if partitions are pathological, and does not preserve stable relative ordering of equivalent keys.',
        'reasons': [
            'Empirically the fastest in-memory general-purpose sorting algorithm on modern processors.',
            'O(n log n) average time complexity with tight inner-loop instruction set.',
            'Minimal memory footprint: O(log n) recursion stack depth.',
            'Excellent CPU memory cache performance due to contiguous linear scan partitioning.'
        ],
        'alternatives': [
            {
                'name': 'Merge Sort',
                'reason': 'Guarantees O(n log n) in the worst case and provides stability, at the cost of O(n) memory allocation.'
            },
            {
                'name': 'Heap Sort',
                'reason': 'Guarantees O(n log n) in O(1) space, but runs 2-3x slower than Quick Sort on typical RAM.'
            }
        ],
        'rule_applied': 'General-purpose balanced throughput → Quick Sort.'
    }
