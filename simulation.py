import tkinter as tk
import random
from models import Node
from dsa_core import build_adjacency_list, dijkstra_shortest_path

class SimulationApp:
    """
    Tkinter Application to visualize the Data Structures and Algorithms conceptually.
    Coordinates everything: Updates Nodes -> Updates Graph -> Runs Dijkstra -> Draws screen.
    Uses persistent canvas objects to prevent memory issues on macOS.
    """
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.root.title("Disaster-Time Communication System (DSA Visualization)")
        
        self.width = width
        self.height = height
        
        self.nodes = []
        self.num_nodes = 30 # Slightly reduced for better performance
        self.transmission_range = 150
        
        self.source_id = 0
        self.goal_id = self.num_nodes - 1
        
        self.is_running = True
        
        # Persistent storage for canvas item IDs
        self.node_ovals = {} # id -> canvas_id
        self.node_texts = {} # id -> canvas_id
        self.edge_lines = [] # list of pooled line IDs
        self.active_edge_count = 0
        
        self.setup_ui()
        self.init_nodes()
        self.root.after(500, self.update_simulation) # Delay initial start

    def setup_ui(self):
        control_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(control_frame, text="Pause / Resume", command=self.toggle_simulation).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Fail Random Node", command=self.fail_random_node, bg="#ffcccc").pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Reset Network", command=self.init_nodes).pack(side=tk.LEFT, padx=10)
        
        self.lbl_stats = tk.Label(control_frame, text="Initializing...", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.lbl_stats.pack(side=tk.RIGHT, padx=20)
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(padx=20, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Legend Frame
        legend_frame = tk.Frame(self.root)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        tk.Label(legend_frame, text="🔵 Source Node   🟣 Destination Node   🟢 Healthy   🔴 Low   ⚫ Dead", font=("Arial", 10)).pack()

    def init_nodes(self):
        """Initializes a new random list of nodes and creates their persistent canvas objects."""
        self.canvas.delete("all")
        self.node_ovals = {}
        self.node_texts = {}
        self.edge_lines = []
        self.active_edge_count = 0
        
        self.source_id = 0  # Reset to default source ID on reset
        self.nodes = []
        for i in range(self.num_nodes):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            node = Node(i, x, y, self.width, self.height)
            self.nodes.append(node)
            
        # Fix Source and Goal positions
        self.nodes[self.source_id].x, self.nodes[self.source_id].y = 50, self.height // 2
        self.nodes[self.nodes[self.source_id].node_id].dx = self.nodes[self.nodes[self.source_id].node_id].dy = 0
        self.nodes[self.goal_id].x, self.nodes[self.goal_id].y = self.width - 50, self.height // 2
        self.nodes[self.nodes[self.goal_id].node_id].dx = self.nodes[self.nodes[self.goal_id].node_id].dy = 0

        # Create physical nodes on canvas once
        for node in self.nodes:
            r = 10
            oval = self.canvas.create_oval(0, 0, 0, 0, width=1)
            text = self.canvas.create_text(0, 0, font=("Arial", 8))
            self.node_ovals[node.node_id] = oval
            self.node_texts[node.node_id] = text

    def toggle_simulation(self):
        self.is_running = not self.is_running
            
    def fail_random_node(self):
        healthy_nodes = [n for n in self.nodes if not n.failed and n.node_id not in (self.source_id, self.goal_id)]
        if healthy_nodes:
            random.choice(healthy_nodes).toggle_fail()
            
    def on_canvas_click(self, event):
        click_x, click_y = event.x, event.y
        
        clicked_node = None
        for node in self.nodes:
            if node.failed or node.node_id == self.goal_id:
                continue
            # Check distance between click coordinates and node coordinates
            dist = ((node.x - click_x) ** 2 + (node.y - click_y) ** 2) ** 0.5
            if dist <= 15:  # interaction radius threshold
                clicked_node = node
                break
                
        if clicked_node:
            old_source_id = self.source_id
            
            # Make the old source node mobile again (give it a random velocity)
            if old_source_id != clicked_node.node_id:
                old_node = self.nodes[old_source_id]
                old_node.dx = random.uniform(-1.5, 1.5)
                old_node.dy = random.uniform(-1.5, 1.5)
                
            # Make the new source node static at its clicked position
            self.source_id = clicked_node.node_id
            clicked_node.dx = 0
            clicked_node.dy = 0
            
            # Recalculate path immediately and redraw
            graph = build_adjacency_list(self.nodes, self.transmission_range)
            path, cost = dijkstra_shortest_path(graph, self.source_id, self.goal_id)
            self.draw(graph, path, cost)
            
    def get_color_for_battery(self, battery):
        if battery <= 0: return "#333333"
        r = min(255, int(255 * (2.0 * (100 - battery) / 100.0)))
        g = min(255, int(255 * (2.0 * battery / 100.0)))
        return f'#{r:02x}{g:02x}00'

    def update_simulation(self):
        if self.is_running:
            for node in self.nodes:
                node.move()
            graph = build_adjacency_list(self.nodes, self.transmission_range)
            path, cost = dijkstra_shortest_path(graph, self.source_id, self.goal_id)
            self.draw(graph, path, cost)
        
        self.root.after(100, self.update_simulation) 
        
    def draw(self, graph, path, cost):
        # Hide all existing lines first (pooling)
        for line in self.edge_lines:
            self.canvas.itemconfigure(line, state='hidden')
        self.active_edge_count = 0

        # 1. Draw Network Edges
        drawn_edges = set()
        for u, neighbors in graph.items():
            for v in neighbors:
                edge_id = tuple(sorted([u, v]))
                if edge_id not in drawn_edges:
                    drawn_edges.add(edge_id)
                    u_node, v_node = self.nodes[u], self.nodes[v]
                    self._draw_line(u_node.x, u_node.y, v_node.x, v_node.y, "#e0e0e0", 1, (2, 4))

        # 2. Draw Dijkstra Path
        if path:
            for i in range(len(path) - 1):
                u, v = self.nodes[path[i]], self.nodes[path[i+1]]
                self._draw_line(u.x, u.y, v.x, v.y, "blue", 4, None)

        # 3. Update Nodes
        for node in self.nodes:
            r = 12 if node.node_id in (self.source_id, self.goal_id) else 8
            color = self.get_color_for_battery(node.battery)
            outline = "blue" if node.node_id == self.source_id else "purple" if node.node_id == self.goal_id else "black"
            width = 3 if node.node_id in (self.source_id, self.goal_id) else 1
            
            # Move and update oval
            self.canvas.coords(self.node_ovals[node.node_id], node.x-r, node.y-r, node.x+r, node.y+r)
            self.canvas.itemconfigure(self.node_ovals[node.node_id], fill=color, outline=outline, width=width)
            self.canvas.tag_raise(self.node_ovals[node.node_id])
            
            # Update text
            self.canvas.coords(self.node_texts[node.node_id], node.x, node.y-15)
            txt = f"{int(node.battery)}%" if node.battery > 0 else "DEAD"
            self.canvas.itemconfigure(self.node_texts[node.node_id], text=txt, fill="red" if node.battery <=0 else "black")
            self.canvas.tag_raise(self.node_texts[node.node_id])

        # Update stats
        if path:
            self.lbl_stats.config(text=f"Connected | Hops: {len(path)-1} | Cost: {int(cost)}", fg="green")
        else:
            self.lbl_stats.config(text="DISCONNECTED", fg="red")

    def _draw_line(self, x1, y1, x2, y2, color, width, dash):
        """Uses a line from the pool or creates a new one if necessary."""
        if self.active_edge_count < len(self.edge_lines):
            line = self.edge_lines[self.active_edge_count]
            self.canvas.coords(line, x1, y1, x2, y2)
            self.canvas.itemconfigure(line, fill=color, width=width, dash=dash, state='normal')
        else:
            line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, dash=dash)
            self.edge_lines.append(line)
        self.active_edge_count += 1
        self.canvas.tag_lower(line)
