"""
ALGOX — Graph Algorithms Module
Implements BFS, DFS, Dijkstra, Prim, and Kruskal using real graph data structures.
"""
from typing import List, Dict, Any, Tuple, Set, Optional
from collections import deque
import heapq

# Default graph topology with 6 nodes and weighted edges
DEFAULT_GRAPH = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('D', 6), ('E', 3)]
}

# Node coordinate positions for Plotly 2D layout visualization
NODE_POSITIONS = {
    'A': (0.0, 1.0),
    'B': (1.0, 2.0),
    'C': (1.0, 0.0),
    'D': (2.5, 2.0),
    'E': (2.5, 0.0),
    'F': (3.5, 1.0)
}

def bfs(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, Any]:
    visited = set()
    queue = deque([start])
    visited.add(start)
    traversal_order = []
    steps = []

    steps.append({
        'step_num': 0,
        'current_node': start,
        'visited': list(visited),
        'frontier': list(queue),
        'edge': None,
        'description': f'Enqueued start node {start}'
    })

    while queue:
        u = queue.popleft()
        traversal_order.append(u)
        steps.append({
            'step_num': len(steps),
            'current_node': u,
            'visited': list(visited),
            'frontier': list(queue),
            'edge': None,
            'description': f'Dequeued node {u}, processing adjacent neighbors'
        })

        for v, weight in sorted(graph.get(u, []), key=lambda x: x[0]):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                steps.append({
                    'step_num': len(steps),
                    'current_node': v,
                    'visited': list(visited),
                    'frontier': list(queue),
                    'edge': (u, v),
                    'description': f'Discovered unvisited neighbor {v} via edge ({u}-{v}, w={weight}); added to queue'
                })

    return {
        'traversal_order': traversal_order,
        'visited': list(visited),
        'steps': steps
    }


def dfs(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, Any]:
    visited = set()
    traversal_order = []
    steps = []

    def _dfs_visit(u: str):
        visited.add(u)
        traversal_order.append(u)
        steps.append({
            'step_num': len(steps),
            'current_node': u,
            'visited': list(visited),
            'frontier': [],
            'edge': None,
            'description': f'Visiting node {u}'
        })

        for v, weight in sorted(graph.get(u, []), key=lambda x: x[0]):
            if v not in visited:
                steps.append({
                    'step_num': len(steps),
                    'current_node': v,
                    'visited': list(visited),
                    'frontier': [],
                    'edge': (u, v),
                    'description': f'Traversing unvisited edge ({u}->{v}, w={weight})'
                })
                _dfs_visit(v)

    _dfs_visit(start)

    return {
        'traversal_order': traversal_order,
        'visited': list(visited),
        'steps': steps
    }


def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, Any]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]
    visited = set()
    steps = []

    steps.append({
        'step_num': 0,
        'current_node': start,
        'distances': dict(distances),
        'visited': list(visited),
        'description': f'Initialized Dijkstra from start node {start} (distance = 0)'
    })

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        steps.append({
            'step_num': len(steps),
            'current_node': u,
            'distances': dict(distances),
            'visited': list(visited),
            'description': f'Settled node {u} with minimum distance {curr_dist}'
        })

        for v, weight in graph.get(u, []):
            if v not in visited:
                new_dist = curr_dist + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    heapq.heappush(pq, (new_dist, v))
                    steps.append({
                        'step_num': len(steps),
                        'current_node': v,
                        'distances': dict(distances),
                        'visited': list(visited),
                        'edge': (u, v),
                        'description': f'Relaxed edge ({u}-{v}, w={weight}): Updated dist[{v}] = {new_dist}'
                    })

    # Build paths from start to each node
    paths = {}
    for node in graph:
        path = []
        curr = node
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        paths[node] = path if path[0] == start else []

    return {
        'distances': {k: (v if v != float('inf') else -1) for k, v in distances.items()},
        'previous': previous,
        'paths': paths,
        'steps': steps
    }


def prim(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, Any]:
    visited = set([start])
    mst_edges = []
    total_weight = 0
    steps = []

    # Priority queue storing (weight, from_node, to_node)
    edges = []
    for to_node, weight in graph.get(start, []):
        heapq.heappush(edges, (weight, start, to_node))

    steps.append({
        'step_num': 0,
        'current_node': start,
        'visited': list(visited),
        'mst_edges': list(mst_edges),
        'total_weight': 0,
        'description': f'Prim MST started from root node {start}. Added adjacent edges to priority queue.'
    })

    while edges and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges)
        if v in visited:
            steps.append({
                'step_num': len(steps),
                'current_node': v,
                'visited': list(visited),
                'mst_edges': list(mst_edges),
                'total_weight': total_weight,
                'rejected_edge': (u, v, weight),
                'description': f'Skipped edge ({u}-{v}, w={weight}) because {v} is already in the tree (creates cycle)'
            })
            continue

        visited.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight

        steps.append({
            'step_num': len(steps),
            'current_node': v,
            'visited': list(visited),
            'mst_edges': list(mst_edges),
            'total_weight': total_weight,
            'accepted_edge': (u, v, weight),
            'description': f'Added edge ({u}-{v}, w={weight}) to MST. Total weight now: {total_weight}'
        })

        for next_node, next_w in graph.get(v, []):
            if next_node not in visited:
                heapq.heappush(edges, (next_w, v, next_node))

    return {
        'mst_edges': mst_edges,
        'total_weight': total_weight,
        'steps': steps
    }


class UnionFind:
    def __init__(self, nodes: List[str]):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, u: str) -> str:
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u: str, v: str) -> bool:
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return False
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        return True


def kruskal(graph: Dict[str, List[Tuple[str, int]]]) -> Dict[str, Any]:
    nodes = list(graph.keys())
    # Extract unique undirected edges
    seen_edges = set()
    all_edges = []
    for u in graph:
        for v, w in graph[u]:
            edge_key = tuple(sorted([u, v]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                all_edges.append((w, edge_key[0], edge_key[1]))

    # Sort edges non-decreasingly by weight
    all_edges.sort(key=lambda x: x[0])

    uf = UnionFind(nodes)
    mst_edges = []
    rejected_edges = []
    total_weight = 0
    steps = []

    steps.append({
        'step_num': 0,
        'mst_edges': list(mst_edges),
        'rejected_edges': list(rejected_edges),
        'total_weight': 0,
        'description': f'Kruskal MST started. Sorted {len(all_edges)} total edges by weight.'
    })

    for w, u, v in all_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            steps.append({
                'step_num': len(steps),
                'accepted_edge': (u, v, w),
                'mst_edges': list(mst_edges),
                'rejected_edges': list(rejected_edges),
                'total_weight': total_weight,
                'description': f'ACCEPTED edge ({u}-{v}, w={w}): Connects disjoint components without cycle.'
            })
            if len(mst_edges) == len(nodes) - 1:
                break
        else:
            rejected_edges.append((u, v, w))
            steps.append({
                'step_num': len(steps),
                'rejected_edge': (u, v, w),
                'mst_edges': list(mst_edges),
                'rejected_edges': list(rejected_edges),
                'total_weight': total_weight,
                'description': f'REJECTED edge ({u}-{v}, w={w}): Both nodes already belong to same component (cycle detected).'
            })

    return {
        'mst_edges': mst_edges,
        'rejected_edges': rejected_edges,
        'total_weight': total_weight,
        'steps': steps
    }
