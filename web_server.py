import http.server
import socketserver
import json
import threading
import time
import random
import webbrowser
import urllib.parse
from models import Node
from dsa_core import build_adjacency_list, build_source_optimized_graph, dijkstra_shortest_path

# Simulation Configuration
WIDTH, HEIGHT = 800, 600
NUM_NODES = 60
TRANSMISSION_RANGE = 180
SOURCE_ID = 0
GOAL_ID = NUM_NODES - 1

class GlobalState:
    def __init__(self):
        self.nodes = []
        self.user_source_id = None
        self.init_nodes()
        self.lock = threading.Lock()
        self.is_running = True
        self.is_paused = False

    def init_nodes(self):
        self.nodes = []
        self.user_source_id = None
        for i in range(NUM_NODES):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            self.nodes.append(Node(i, x, y, WIDTH, HEIGHT))
        
        # Goal (Destination) setup: Static and Immortal Base Station
        goal = self.nodes[GOAL_ID]
        goal.x, goal.y = WIDTH - 50, HEIGHT // 2
        goal.dx = goal.dy = 0
        goal.is_static = True
        goal.is_immortal = True

    def update(self):
        while self.is_running:
            if not self.is_paused:
                with self.lock:
                    for node in self.nodes:
                        node.move()
            time.sleep(0.1) # 10 FPS updates

state = GlobalState()

class SimulationHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path_only = parsed_url.path

        if path_only == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path_only == '/data':
            with state.lock:
                current_source_id = state.user_source_id
                # Fallback to dynamic farthest node if no valid user source node is selected
                if current_source_id is None or current_source_id >= len(state.nodes):
                    dest = state.nodes[GOAL_ID]
                    max_dist = -1
                    current_source_id = 0
                    for node in state.nodes:
                        if not node.failed and node.node_id != GOAL_ID:
                            d = node.distance_to(dest)
                            if d > max_dist:
                                max_dist = d
                                current_source_id = node.node_id
                    # Use normal MST when no source is manually selected
                    graph = build_adjacency_list(state.nodes, TRANSMISSION_RANGE)
                else:
                    # Use source-optimized graph when user manually selects a source
                    graph = build_source_optimized_graph(state.nodes, TRANSMISSION_RANGE, current_source_id, GOAL_ID)
                
                path, cost = dijkstra_shortest_path(graph, current_source_id, GOAL_ID)
                
                data = {
                    "nodes": [n.to_dict() for n in state.nodes],
                    "edges": graph,
                    "path": path,
                    "cost": cost if cost != float('inf') else None,
                    "source_id": current_source_id,
                    "goal_id": GOAL_ID,
                    "transmission_range": TRANSMISSION_RANGE
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif path_only == '/set_source':
            query_params = urllib.parse.parse_qs(parsed_url.query)
            if 'id' in query_params:
                try:
                    node_id = int(query_params['id'][0])
                    with state.lock:
                        if 0 <= node_id < len(state.nodes):
                            state.user_source_id = node_id
                except ValueError:
                    pass
            self.send_response(200)
            self.end_headers()
        elif path_only == '/fail_random':
            with state.lock:
                healthy = [n for n in state.nodes if not n.failed and n.node_id not in (SOURCE_ID, GOAL_ID)]
                if healthy:
                    random.choice(healthy).toggle_fail()
            self.send_response(200)
            self.end_headers()
        elif path_only == '/fail_path':
            with state.lock:
                current_source_id = state.user_source_id
                # Fallback to dynamic farthest node if no valid user source node is selected
                if current_source_id is None or current_source_id >= len(state.nodes):
                    dest = state.nodes[GOAL_ID]
                    max_dist = -1
                    current_source_id = 0
                    for node in state.nodes:
                        if not node.failed and node.node_id != GOAL_ID:
                            d = node.distance_to(dest)
                            if d > max_dist:
                                max_dist = d
                                current_source_id = node.node_id
                
                graph = build_adjacency_list(state.nodes, TRANSMISSION_RANGE)
                path, cost = dijkstra_shortest_path(graph, current_source_id, GOAL_ID)
                
                # Fail a random node from the path (excluding source and destination)
                if path and len(path) > 2:
                    failurable = [n for n in path[1:-1] if not state.nodes[n].failed]
                    if failurable:
                        node_id = random.choice(failurable)
                        state.nodes[node_id].toggle_fail()
            self.send_response(200)
            self.end_headers()
        elif path_only == '/toggle_pause':
            with state.lock:
                state.is_paused = not state.is_paused
            self.send_response(200)
            self.end_headers()
        elif path_only == '/fail':
            with state.lock:
                healthy = [n for n in state.nodes if not n.failed and n.node_id not in (SOURCE_ID, GOAL_ID)]
                if healthy:
                    random.choice(healthy).toggle_fail()
            self.send_response(200)
            self.end_headers()
        elif path_only == '/reset':
            with state.lock:
                state.init_nodes()
            self.send_response(200)
            self.end_headers()
        else:
            super().do_GET()

def run_server():
    PORT = 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SimulationHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start simulation thread
    sim_thread = threading.Thread(target=state.update, daemon=True)
    sim_thread.start()
    
    # Start web server
    run_server()
