"""
ALGOX — Algorithm Complexity Metadata Registry
Covers exactly 13 core algorithms across Sorting, Searching, and Graph domains.
"""

ALGORITHM_COMPLEXITY = {   'BFS': {   'advantages': ['Guarantees shortest path in unweighted graphs', 'Level-by-level discovery', 'Complete'],
               'algorithm': 'BFS',
               'applications': [   'Unweighted shortest path',
                                   'Connected components',
                                   'Social network degrees of separation'],
               'average': 'O(V + E)',
               'best': 'O(V + E)',
               'category': 'Graph',
               'description': 'Explores graph level-by-level from source using a FIFO queue, visiting vertices in '
                              'increasing distance order.',
               'disadvantages': ['Requires O(V) space for queue and visited set', 'High memory on wide graphs'],
               'how_it_works': 'Enqueues source, marks visited. Dequeues vertex, explores unvisited neighbors, '
                               'enqueues them.',
               'in_place': False,
               'limitations': ['Requires O(V) space for queue and visited set', 'High memory on wide graphs'],
               'paradigm': 'Graph Traversal / Level-order',
               'problem_type': 'Graph Traversal / Unweighted Shortest Path',
               'pseudocode': 'procedure bfs(G: graph, start: vertex):\n'
                             '    visited = {start}\n'
                             '    queue = [start]\n'
                             '    while queue is not empty:\n'
                             '        u = queue.pop_front()\n'
                             '        for each neighbor v of u:\n'
                             '            if v not in visited:\n'
                             '                visited.add(v)\n'
                             '                queue.push_back(v)',
               'related': ['DFS', 'Dijkstra'],
               'space': 'O(V)',
               'stable': True,
               'use_cases': [   'Unweighted shortest path',
                                'Connected components',
                                'Social network degrees of separation'],
               'worst': 'O(V + E)'},
    'Binary Search': {   'advantages': [   'O(log n) lookup: 1 million items in <= 20 steps',
                                           'O(1) space iterative',
                                           'Range queries basis'],
                         'algorithm': 'Binary Search',
                         'applications': [   'Static lookup tables and database indexes',
                                             'Numerical bisection',
                                             'Dictionary search'],
                         'average': 'O(log n)',
                         'best': 'O(1)',
                         'category': 'Searching',
                         'description': 'Searches a sorted array by repeatedly bisecting the search interval and '
                                        'eliminating half the elements.',
                         'disadvantages': [   'Requires sorted array',
                                              'Requires O(1) random-access indexing',
                                              'Sorting cost dominates if searching once'],
                         'how_it_works': 'Calculates mid. If A[mid]==target found. If A[mid]<target search right half. '
                                         'Else search left half.',
                         'in_place': True,
                         'limitations': [   'Requires sorted array',
                                            'Requires O(1) random-access indexing',
                                            'Sorting cost dominates if searching once'],
                         'paradigm': 'Divide and Conquer',
                         'problem_type': 'Binary Searching / Bisection',
                         'pseudocode': 'procedure binary_search(A: sorted_list, target):\n'
                                       '    lo = 0; hi = length(A) - 1\n'
                                       '    while lo <= hi:\n'
                                       '        mid = lo + (hi - lo) // 2\n'
                                       '        if A[mid] == target: return mid\n'
                                       '        else if A[mid] < target: lo = mid + 1\n'
                                       '        else: hi = mid - 1\n'
                                       '    return -1',
                         'related': ['Linear Search', 'Interpolation Search'],
                         'space': 'O(1)',
                         'stable': True,
                         'use_cases': [   'Static lookup tables and database indexes',
                                          'Numerical bisection',
                                          'Dictionary search'],
                         'worst': 'O(log n)'},
    'Bubble Sort': {   'advantages': [   'Simple to implement',
                                         'Stable sort',
                                         'Adaptive: O(n) on sorted data',
                                         'In-place'],
                       'algorithm': 'Bubble Sort',
                       'applications': ['Education', 'Tiny arrays (N < 20)', 'Nearly sorted data'],
                       'average': 'O(n²)',
                       'best': 'O(n)',
                       'category': 'Sorting',
                       'description': 'Repeatedly compares and swaps adjacent elements until sorted. Each pass bubbles '
                                      'the largest unsorted element to its position.',
                       'disadvantages': [   'O(n²) average/worst case',
                                            'Poor cache performance',
                                            'Impractical for large datasets'],
                       'how_it_works': 'Iterates n times. In each pass, compares adjacent pairs and swaps if '
                                       'unordered. Optimized with early exit if no swaps occur.',
                       'in_place': True,
                       'limitations': [   'O(n²) average/worst case',
                                          'Poor cache performance',
                                          'Impractical for large datasets'],
                       'paradigm': 'Brute Force / Exchange',
                       'problem_type': 'Comparison Sorting',
                       'pseudocode': 'procedure bubble_sort(A: list):\n'
                                     '    n = length(A)\n'
                                     '    for i = 0 to n - 1:\n'
                                     '        swapped = false\n'
                                     '        for j = 0 to n - i - 2:\n'
                                     '            if A[j] > A[j+1]:\n'
                                     '                swap(A[j], A[j+1])\n'
                                     '                swapped = true\n'
                                     '        if not swapped: break',
                       'related': ['Selection Sort', 'Insertion Sort'],
                       'space': 'O(1)',
                       'stable': True,
                       'use_cases': ['Education', 'Tiny arrays (N < 20)', 'Nearly sorted data'],
                       'worst': 'O(n²)'},
    'DFS': {   'advantages': [   'Lower memory on deep sparse graphs',
                                 'Foundation for topological sort',
                                 'Cycle detection'],
               'algorithm': 'DFS',
               'applications': ['Topological sorting', 'Cycle detection', 'Maze solving'],
               'average': 'O(V + E)',
               'best': 'O(V + E)',
               'category': 'Graph',
               'description': 'Explores graph as deeply as possible along each branch before backtracking, using a '
                              'stack.',
               'disadvantages': ['Does not yield shortest path', 'Can get stuck in deep paths', 'Stack overflow risk'],
               'how_it_works': 'Marks node visited. Recursively explores first unvisited neighbor. Backtracks at dead '
                               'end.',
               'in_place': False,
               'limitations': ['Does not yield shortest path', 'Can get stuck in deep paths', 'Stack overflow risk'],
               'paradigm': 'Graph Traversal / Depth-first',
               'problem_type': 'Graph Traversal / Cycle & Topological Analysis',
               'pseudocode': 'procedure dfs(G: graph, u: vertex, visited: set):\n'
                             '    visited.add(u)\n'
                             '    for each neighbor v of u:\n'
                             '        if v not in visited:\n'
                             '            dfs(G, v, visited)',
               'related': ['BFS', 'Tarjan SCC'],
               'space': 'O(V)',
               'stable': True,
               'use_cases': ['Topological sorting', 'Cycle detection', 'Maze solving'],
               'worst': 'O(V + E)'},
    'Dijkstra': {   'advantages': [   'Exact shortest paths for non-negative weights',
                                      'O((V+E)logV) with binary heap',
                                      'Single-source all-destinations'],
                    'algorithm': 'Dijkstra',
                    'applications': [   'GPS road navigation',
                                        'Network routing protocols (OSPF)',
                                        'Robotic motion planning'],
                    'average': 'O((V + E) log V)',
                    'best': 'O((V + E) log V)',
                    'category': 'Graph',
                    'description': 'Computes single-source shortest paths on weighted graphs with non-negative edge '
                                   'weights using a min-heap.',
                    'disadvantages': [   'Fails on negative edge weights',
                                         'Cannot handle dynamic fluctuating weights easily'],
                    'how_it_works': 'Initializes dist[source]=0, others infinity. Greedily extracts min-dist vertex '
                                    'from heap, relaxes incident edges.',
                    'in_place': False,
                    'limitations': [   'Fails on negative edge weights',
                                       'Cannot handle dynamic fluctuating weights easily'],
                    'paradigm': 'Greedy / Shortest Path',
                    'problem_type': 'Single-Source Shortest Path',
                    'pseudocode': 'procedure dijkstra(G: graph, source: vertex):\n'
                                  '    dist = {v: inf for v in V}; dist[source] = 0\n'
                                  '    pq = [(0, source)]\n'
                                  '    while pq is not empty:\n'
                                  '        d, u = heappop(pq)\n'
                                  '        if d > dist[u]: continue\n'
                                  '        for each (v, weight) in G[u]:\n'
                                  '            if dist[u] + weight < dist[v]:\n'
                                  '                dist[v] = dist[u] + weight\n'
                                  '                heappush(pq, (dist[v], v))',
                    'related': ['BFS', 'Bellman-Ford', 'A* Search'],
                    'space': 'O(V)',
                    'stable': True,
                    'use_cases': ['GPS road navigation', 'Network routing protocols (OSPF)', 'Robotic motion planning'],
                    'worst': 'O((V + E) log V)'},
    'Heap Sort': {   'advantages': [   'Guaranteed O(n log n) with strictly O(1) auxiliary space',
                                       'Iterative, no recursion',
                                       'No quadratic degradation'],
                     'algorithm': 'Heap Sort',
                     'applications': [   'Real-time systems requiring bounded RAM and time',
                                         'Embedded systems',
                                         'Top-K order statistics'],
                     'average': 'O(n log n)',
                     'best': 'O(n log n)',
                     'category': 'Sorting',
                     'description': 'Builds binary max-heap from array, then repeatedly extracts root maximum to array '
                                    'end.',
                     'disadvantages': [   'Not stable',
                                          'Poor cache locality due to index jumps',
                                          'Slower than Quick Sort in practice'],
                     'how_it_works': 'Phase 1: Build max-heap in O(n). Phase 2: For each element, swap root with tail, '
                                     'sift-down root in O(log n).',
                     'in_place': True,
                     'limitations': [   'Not stable',
                                        'Poor cache locality due to index jumps',
                                        'Slower than Quick Sort in practice'],
                     'paradigm': 'Heap-based / Selection',
                     'problem_type': 'Comparison Sorting',
                     'pseudocode': 'procedure heap_sort(A: list):\n'
                                   '    build_max_heap(A)\n'
                                   '    for i = length(A) - 1 down to 1:\n'
                                   '        swap(A[0], A[i])\n'
                                   '        max_heapify(A, 0, i)',
                     'related': ['Quick Sort', 'Priority Queue'],
                     'space': 'O(1)',
                     'stable': False,
                     'use_cases': [   'Real-time systems requiring bounded RAM and time',
                                      'Embedded systems',
                                      'Top-K order statistics'],
                     'worst': 'O(n log n)'},
    'Insertion Sort': {   'advantages': [   'Highly adaptive: O(n) best-case',
                                            'Stable',
                                            'Low overhead on small arrays',
                                            'Online algorithm'],
                          'algorithm': 'Insertion Sort',
                          'applications': [   'Nearly sorted datasets',
                                              'Small subarrays in hybrid sorts (Timsort)',
                                              'Streaming input'],
                          'average': 'O(n²)',
                          'best': 'O(n)',
                          'category': 'Sorting',
                          'description': 'Builds sorted array one element at a time by inserting each element into its '
                                         'relative position within sorted prefix.',
                          'disadvantages': ['O(n²) average and worst-case', 'Excessive shifts on reverse-ordered data'],
                          'how_it_works': 'Maintains sorted prefix. For element A[i], shifts larger preceding elements '
                                          'right, then drops A[i] in slot.',
                          'in_place': True,
                          'limitations': ['O(n²) average and worst-case', 'Excessive shifts on reverse-ordered data'],
                          'paradigm': 'Incremental / Adaptive',
                          'problem_type': 'Comparison Sorting',
                          'pseudocode': 'procedure insertion_sort(A: list):\n'
                                        '    n = length(A)\n'
                                        '    for i = 1 to n - 1:\n'
                                        '        key = A[i]\n'
                                        '        j = i - 1\n'
                                        '        while j >= 0 and A[j] > key:\n'
                                        '            A[j+1] = A[j]\n'
                                        '            j = j - 1\n'
                                        '        A[j+1] = key',
                          'related': ['Bubble Sort', 'Shell Sort'],
                          'space': 'O(1)',
                          'stable': True,
                          'use_cases': [   'Nearly sorted datasets',
                                           'Small subarrays in hybrid sorts (Timsort)',
                                           'Streaming input'],
                          'worst': 'O(n²)'},
    'Kruskal': {   'advantages': [   'Efficient for sparse graphs (E << V²)',
                                     'Naturally handles disconnected graphs',
                                     'Simple edge-centric architecture'],
                   'algorithm': 'Kruskal',
                   'applications': [   'Civil infrastructure routing',
                                       'Single-linkage hierarchical clustering',
                                       'Image segmentation'],
                   'average': 'O(E log E)',
                   'best': 'O(E log E)',
                   'category': 'Graph',
                   'description': 'Finds Minimum Spanning Tree by sorting edges by weight and greedily accepting edges '
                                  'connecting disjoint components using Union-Find.',
                   'disadvantages': [   'Requires sorting all edges upfront O(E log E)',
                                        'Slightly slower than Prim on dense graphs'],
                   'how_it_works': 'Sorts edge list. Uses Disjoint Set Union (DSU). For each edge, if '
                                   'Find(u)!=Find(v), adds edge to MST and unions sets.',
                   'in_place': False,
                   'limitations': [   'Requires sorting all edges upfront O(E log E)',
                                      'Slightly slower than Prim on dense graphs'],
                   'paradigm': 'Greedy / Minimum Spanning Tree',
                   'problem_type': 'Minimum Spanning Tree / Forest (Edge-Centric)',
                   'pseudocode': 'procedure kruskal(G: graph):\n'
                                 '    edges = sort_all_edges_by_weight(G)\n'
                                 '    dsu = DisjointSetUnion(V)\n'
                                 '    mst_edges = []\n'
                                 '    for each (u, v, w) in edges:\n'
                                 '        if dsu.find(u) != dsu.find(v):\n'
                                 '            mst_edges.append((u, v, w))\n'
                                 '            dsu.union(u, v)\n'
                                 '            if len(mst_edges) == V - 1: break',
                   'related': ['Prim', 'Union-Find'],
                   'space': 'O(V)',
                   'stable': True,
                   'use_cases': [   'Civil infrastructure routing',
                                    'Single-linkage hierarchical clustering',
                                    'Image segmentation'],
                   'worst': 'O(E log E)'},
    'Linear Search': {   'advantages': [   'No preprocessing required',
                                           'Works on unsorted data and linked lists',
                                           'Trivial to implement'],
                         'algorithm': 'Linear Search',
                         'applications': ['One-off search on small unsorted data', 'Searching linked lists or streams'],
                         'average': 'O(n)',
                         'best': 'O(1)',
                         'category': 'Searching',
                         'description': 'Scans each element sequentially from start to end until target is found or '
                                        'collection exhausted.',
                         'disadvantages': ['O(n) time makes repeated queries slow', 'Scales poorly'],
                         'how_it_works': 'Checks A[i] == target for i=0..n-1. Returns index on match, -1 on failure. '
                                         'Works on unsorted collections.',
                         'in_place': True,
                         'limitations': ['O(n) time makes repeated queries slow', 'Scales poorly'],
                         'paradigm': 'Sequential / Brute Force',
                         'problem_type': 'Sequential Searching',
                         'pseudocode': 'procedure linear_search(A: list, target):\n'
                                       '    for i = 0 to length(A) - 1:\n'
                                       '        if A[i] == target: return i\n'
                                       '    return -1',
                         'related': ['Binary Search'],
                         'space': 'O(1)',
                         'stable': True,
                         'use_cases': ['One-off search on small unsorted data', 'Searching linked lists or streams'],
                         'worst': 'O(n)'},
    'Merge Sort': {   'advantages': [   'Guaranteed O(n log n) across all inputs',
                                        'Stable',
                                        'Predictable with zero worst-case degradation',
                                        'Parallelizable'],
                      'algorithm': 'Merge Sort',
                      'applications': [   'Sorting linked lists',
                                          'External sorting on disk',
                                          'Guaranteed deterministic performance'],
                      'average': 'O(n log n)',
                      'best': 'O(n log n)',
                      'category': 'Sorting',
                      'description': 'Recursively divides array into halves, sorts each half, and merges sorted '
                                     'subarrays in linear time.',
                      'disadvantages': [   'Requires O(n) auxiliary space',
                                           'Higher constant factor than Quick Sort',
                                           'Cache-unfriendly'],
                      'how_it_works': 'Divides array at midpoint until base case. Merges sorted halves using an '
                                      'auxiliary buffer.',
                      'in_place': False,
                      'limitations': [   'Requires O(n) auxiliary space',
                                         'Higher constant factor than Quick Sort',
                                         'Cache-unfriendly'],
                      'paradigm': 'Divide and Conquer',
                      'problem_type': 'Comparison Sorting',
                      'pseudocode': 'procedure merge_sort(A: list):\n'
                                    '    if length(A) <= 1: return A\n'
                                    '    mid = length(A) // 2\n'
                                    '    left = merge_sort(A[0..mid-1])\n'
                                    '    right = merge_sort(A[mid..end])\n'
                                    '    return merge(left, right)',
                      'related': ['Quick Sort', 'Timsort'],
                      'space': 'O(n)',
                      'stable': True,
                      'use_cases': [   'Sorting linked lists',
                                       'External sorting on disk',
                                       'Guaranteed deterministic performance'],
                      'worst': 'O(n log n)'},
    'Prim': {   'advantages': [   'Faster on dense graphs (O(E log V))',
                                  'Maintains single connected tree throughout',
                                  'Greedy cut property'],
                'algorithm': 'Prim',
                'applications': ['Electrical grid and pipe routing', 'Metric TSP approximation', 'Cluster analysis'],
                'average': 'O(E log V)',
                'best': 'O(E log V)',
                'category': 'Graph',
                'description': 'Finds Minimum Spanning Tree in connected weighted graph by greedily adding cheapest '
                               'edge connecting tree to unvisited vertex.',
                'disadvantages': ['Requires connected graph', 'More complex priority queue maintenance than Kruskal'],
                'how_it_works': 'Starts with arbitrary vertex in MST. Uses min-heap of boundary edges. Extracts '
                                'min-weight edge to unvisited vertex, adds to MST.',
                'in_place': False,
                'limitations': ['Requires connected graph', 'More complex priority queue maintenance than Kruskal'],
                'paradigm': 'Greedy / Minimum Spanning Tree',
                'problem_type': 'Minimum Spanning Tree (Vertex-Centric)',
                'pseudocode': 'procedure prim(G: graph, start: vertex):\n'
                              '    in_mst = {start}\n'
                              '    pq = [(w, start, v) for v, w in G[start]]\n'
                              '    mst_edges = []\n'
                              '    while pq and len(in_mst) < V:\n'
                              '        w, u, v = heappop(pq)\n'
                              '        if v in in_mst: continue\n'
                              '        in_mst.add(v); mst_edges.append((u, v, w))\n'
                              '        for next_v, weight in G[v]:\n'
                              '            if next_v not in in_mst:\n'
                              '                heappush(pq, (weight, v, next_v))',
                'related': ['Kruskal', 'Dijkstra'],
                'space': 'O(V)',
                'stable': True,
                'use_cases': ['Electrical grid and pipe routing', 'Metric TSP approximation', 'Cluster analysis'],
                'worst': 'O(E log V)'},
    'Quick Sort': {   'advantages': [   'Fast in practice with small constant factors',
                                        'In-place O(log n) stack',
                                        'Cache-friendly'],
                      'algorithm': 'Quick Sort',
                      'applications': [   'General-purpose sorting standard libraries',
                                          'Large uniform numeric arrays',
                                          'In-memory arrays'],
                      'average': 'O(n log n)',
                      'best': 'O(n log n)',
                      'category': 'Sorting',
                      'description': 'Partitions array relative to a pivot element, then recursively sorts both '
                                     'partitions.',
                      'disadvantages': [   'O(n²) worst-case on unbalanced partitions',
                                           'Not stable',
                                           'Recursive stack overhead'],
                      'how_it_works': 'Chooses pivot. Partitions array in-place so smaller elements precede pivot and '
                                      'larger follow. Recursively sorts partitions.',
                      'in_place': True,
                      'limitations': [   'O(n²) worst-case on unbalanced partitions',
                                         'Not stable',
                                         'Recursive stack overhead'],
                      'paradigm': 'Divide and Conquer',
                      'problem_type': 'Comparison Sorting',
                      'pseudocode': 'procedure quick_sort(A: list, lo, hi):\n'
                                    '    if lo < hi:\n'
                                    '        p = partition(A, lo, hi)\n'
                                    '        quick_sort(A, lo, p - 1)\n'
                                    '        quick_sort(A, p + 1, hi)',
                      'related': ['Merge Sort', 'Heap Sort'],
                      'space': 'O(log n)',
                      'stable': False,
                      'use_cases': [   'General-purpose sorting standard libraries',
                                       'Large uniform numeric arrays',
                                       'In-memory arrays'],
                      'worst': 'O(n²)'},
    'Selection Sort': {   'advantages': [   'At most O(n) swaps',
                                            'In-place',
                                            'Predictable runtime independent of initial order'],
                          'algorithm': 'Selection Sort',
                          'applications': ['Systems where memory writes are expensive', 'Small datasets'],
                          'average': 'O(n²)',
                          'best': 'O(n²)',
                          'category': 'Sorting',
                          'description': 'Divides array into sorted and unsorted regions. Repeatedly finds minimum in '
                                         'unsorted and appends to sorted region.',
                          'disadvantages': ['Always O(n²) comparisons', 'Not stable', 'Non-adaptive'],
                          'how_it_works': 'In pass i, scans i..n-1 to find minimum element index, then swaps with '
                                          'index i. Exactly n(n-1)/2 comparisons.',
                          'in_place': True,
                          'limitations': ['Always O(n²) comparisons', 'Not stable', 'Non-adaptive'],
                          'paradigm': 'Brute Force / Selection',
                          'problem_type': 'Comparison Sorting',
                          'pseudocode': 'procedure selection_sort(A: list):\n'
                                        '    n = length(A)\n'
                                        '    for i = 0 to n - 1:\n'
                                        '        min_idx = i\n'
                                        '        for j = i + 1 to n - 1:\n'
                                        '            if A[j] < A[min_idx]:\n'
                                        '                min_idx = j\n'
                                        '        if min_idx != i:\n'
                                        '            swap(A[i], A[min_idx])',
                          'related': ['Bubble Sort', 'Insertion Sort', 'Heap Sort'],
                          'space': 'O(1)',
                          'stable': False,
                          'use_cases': ['Systems where memory writes are expensive', 'Small datasets'],
                          'worst': 'O(n²)'}}
