# Disaster-Time Communication System - Run Guide

This project contains a web browser visualizer for simulating a power-efficient communication backbone using a Minimum Spanning Tree (MST) and Dijkstra's algorithm for shortest-path routing.

---

## Prerequisites

Make sure you have **Python 3** installed on your system.

---

## Web Browser Visualizer

This is a web-based dashboard using an HTML5 Canvas and a Python HTTP API backend.

### How to Run

Navigate to your project directory in your terminal and run:

```bash
python3 main.py
```

You can also run:

```bash
python3 web_server.py
```

Once the server starts, it will output:

```text
Server started at http://localhost:8080
```

It should automatically open a browser window at `http://localhost:8080`. If it does not, open that address manually.

### How to Interact

- **Change Starting Node**: Hover over any healthy node and click it.
- **Dijkstra Shortest Path**: The shortest path is drawn as a glowing light blue line to the destination base station.
- **Network Status & Metrics**: The stats card updates in real time.
- **Simulate Node Failure**: Click "Fail Random Node" or "Fail Path Node".
- **Reset Network**: Click "Reset Network" to generate a new topology.
