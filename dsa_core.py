import heapq

class PriorityQueue:
    """
    A custom wrapper around heapq to explicitly demonstrate the use of priority queues 
    for Dijkstra's algorithm. It handles storing elements sorted by prioriy (cost).
    """
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        # We push a tuple of (priority, item). heapq automatically sorts by the first element.
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class UnionFind:
    """Helper for Kruskal's MST algorithm."""
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

def build_adjacency_list(nodes, transmission_range):
    """
    Builds a Power-Efficient Backbone using Kruskal's Minimum Spanning Tree.
    This ensures minimum connectivity with NO redundant cycles.
    """
    potential_edges = []
    active_nodes = [n.node_id for n in nodes if not n.failed]
    
    # Identify all possible signal links
    for i in range(len(nodes)):
        if nodes[i].failed: continue
        for j in range(i + 1, len(nodes)):
            if nodes[j].failed: continue
            
            dist = nodes[i].distance_to(nodes[j])
            if dist <= transmission_range:
                # Weight prioritizing high battery and short distance
                penalty = (100 - nodes[i].battery) + (100 - nodes[j].battery)
                weight = dist + penalty
                potential_edges.append((weight, nodes[i].node_id, nodes[j].node_id))
    
    # Kruskal's Logic: Sort by weight and pick edges that don't form cycles
    potential_edges.sort()
    uf = UnionFind(active_nodes)
    mst_edges = []
    for weight, u, v in potential_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            
    # Build the final graph dictionary
    graph = {node_id: {} for node_id in active_nodes}
    for u, v, w in mst_edges:
        graph[u][v] = w
        graph[v][u] = w
        
    return graph

def dijkstra_shortest_path(graph, start_id, goal_id):
    """
    Implements Dijkstra's algorithm to find the optimal route from start to goal.
    Uses the custom Priority Queue and Adjacency List to guarantee O((V+E) log V).
    
    Returns: (list_of_node_ids_in_path, total_cost)
    """
    if start_id not in graph or goal_id not in graph:
        return [], float('inf')
        
    frontier = PriorityQueue()
    frontier.put(start_id, 0)
    
    came_from = {}
    cost_so_far = {}
    
    came_from[start_id] = None
    cost_so_far[start_id] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        # Early exit if we reach the goal
        if current == goal_id:
            break
            
        for next_node, weight in graph[current].items():
            new_cost = cost_so_far[current] + weight
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put(next_node, priority) # DSA Core: Using Priority Queue
                came_from[next_node] = current
                
    # Goal not reached due to lack of network connectivity (partitioned network)
    if goal_id not in came_from:
        return [], float('inf')
        
    # Reconstruct path backwards from goal
    current = goal_id
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
        
    path.reverse()
    return path, cost_so_far[goal_id]
