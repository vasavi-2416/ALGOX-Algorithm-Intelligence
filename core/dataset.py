"""
ALGOX — Dataset Generator Module
Generates real synthetic arrays across 5 mathematical distributions with metadata analysis.
"""
from typing import List, Dict, Any, Optional
import random
import statistics

DISTRIBUTIONS = [
    'Random',
    'Sorted',
    'Reverse Sorted',
    'Nearly Sorted',
    'Duplicate Heavy'
]

def generate_dataset(size: int, distribution: str = 'Random', seed: Optional[int] = None) -> List[int]:
    """
    Generates an integer dataset of length `size` according to specified distribution.
    Reproducible if seed is provided.
    """
    if size <= 0:
        return []

    rng = random.Random(seed)

    if distribution == 'Random':
        # Uniform random distribution of integers
        max_val = max(100, size * 5)
        return [rng.randint(1, max_val) for _ in range(size)]

    elif distribution == 'Sorted':
        # Strictly ascending sorted sequence with small non-negative random step intervals
        arr = []
        curr = rng.randint(1, 10)
        for _ in range(size):
            arr.append(curr)
            curr += rng.randint(1, 6)
        return arr

    elif distribution == 'Reverse Sorted':
        # Descending sorted sequence
        arr = []
        curr = size * 6 + rng.randint(10, 50)
        for _ in range(size):
            arr.append(curr)
            curr -= rng.randint(1, 6)
        return arr

    elif distribution == 'Nearly Sorted':
        # Sorted array with ~5% of elements swapped randomly
        arr = list(range(1, size + 1))
        arr = [x * 3 for x in arr]
        num_perturbations = max(1, int(size * 0.05))
        for _ in range(num_perturbations):
            idx1 = rng.randint(0, size - 1)
            idx2 = rng.randint(0, size - 1)
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
        return arr

    elif distribution == 'Duplicate Heavy':
        # Array with very few distinct keys, creating heavy duplicates
        num_distinct = max(2, min(5, max(2, size // 10)))
        distinct_pool = [rng.randint(10, 99) for _ in range(num_distinct)]
        return [rng.choice(distinct_pool) for _ in range(size)]

    else:
        # Fallback to Random
        max_val = max(100, size * 5)
        return [rng.randint(1, max_val) for _ in range(size)]


def get_dataset_info(arr: List[int]) -> Dict[str, Any]:
    """
    Computes real statistical and structural summary of the dataset.
    Never returns fabricated values.
    """
    if not arr:
        return {
            'size': 0,
            'min': 0,
            'max': 0,
            'mean': 0.0,
            'median': 0.0,
            'std_dev': 0.0,
            'unique_count': 0,
            'duplicate_count': 0,
            'duplicate_ratio': 0.0,
            'sortedness': 100.0,
            'is_sorted': True
        }

    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    mean_val = statistics.mean(arr)
    median_val = statistics.median(arr)
    std_val = statistics.stdev(arr) if n > 1 else 0.0
    unique_count = len(set(arr))
    duplicate_count = n - unique_count
    duplicate_ratio = round((duplicate_count / n) * 100, 2)
    in_order = sum(1 for i in range(n - 1) if arr[i] <= arr[i + 1])
    sortedness = round((in_order / (n - 1)) * 100, 2) if n > 1 else 100.0
    is_sorted = (in_order == n - 1) if n > 1 else True

    return {
        'size': n,
        'min': min_val,
        'max': max_val,
        'mean': round(mean_val, 2),
        'median': round(median_val, 2),
        'std_dev': round(std_val, 2),
        'unique_count': unique_count,
        'duplicate_count': duplicate_count,
        'duplicate_ratio': duplicate_ratio,
        'sortedness': sortedness,
        'is_sorted': is_sorted
    }
