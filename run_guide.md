# Disaster-Time Communication System - Run Guide

This project contains two visualizers for simulating a power-efficient communication backbone using a Minimum Spanning Tree (MST) and Dijkstra's algorithm for shortest-path routing.

1. **Tkinter Desktop GUI Visualizer**
2. **Web Browser Visualizer (HTML5 Canvas)**

---

## Prerequisites

Make sure you have **Python 3** installed on your system. 

If you are using macOS and need to install/update Python or Tkinter:
- Python 3 usually includes Tkinter out of the box.
- If you encounter a Tkinter-related issue, you can install/fix it via Homebrew:
  ```bash
  brew install python tcl-tk
  ```

---

## 1. Tkinter Desktop GUI Visualizer

This is a native desktop application that visualizes the nodes, routing, and battery drain state.

### How to Run:
Navigate to your project directory in your terminal and run:
```bash
python3 main.py
```

### How to Interact:
- **Change Starting Node**: Click on any **healthy (green/orange) node** on the canvas. The clicked node will become the new starting node (marked in blue with a thick outline) and will become static. The old starting node will resume moving.
- **Dijkstra Shortest Path**: The shortest path from the starting node to the destination server (purple node) is calculated and highlighted with a **blue path**.
- **Pause / Resume**: Click the "Pause / Resume" button at the top to pause or resume node movement.
- **Fail Random Node**: Click "Fail Random Node" to simulate a communication node failure (turns black/DEAD).
- **Reset Network**: Click "Reset Network" to generate a brand new network topology with new random node positions and reset the starting node to Node 0.

---

## 2. Web Browser Visualizer

This is a modern web-based dashboard utilizing an HTML5 Canvas and an HTTP API backend.

### How to Run:
Navigate to your project directory in your terminal and run:
```bash
python3 web_server.py
```

Once the server starts, it will output:
```
Server started at http://localhost:8080
```
It should also automatically open a new browser window/tab at `http://localhost:8080`. If it does not, manually open your web browser and navigate to [http://localhost:8080](http://localhost:8080).

### How to Interact:
- **Change Starting Node**: Hover over any **healthy node** (your cursor will change to a pointer) and **click** it. The system will immediately update the starting node (marked in blue) and recalculate the path.
- **Dijkstra Shortest Path**: The shortest path is drawn as a glowing **light blue line** to the destination base station (purple node).
- **Network Status & Metrics**: The stats card on the right-hand side updates in real-time, showing:
  - Network Status (`CONNECTED` or `PARTITIONED`)
  - Path Hops (number of jumps between nodes)
  - Min Cost Path (power metric total)
- **Simulate Node Failure**: Click "Simulate Node Failure" to fail a random healthy node.
- **Reset Network**: Click "Reset Network" to generate a new set of nodes and clear the manual starting node selection.
