import math
import random

class Node:
    """
    Represents a mobile device in the ad-hoc network.
    """
    def __init__(self, node_id, x, y, max_x, max_y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        
        # Velocity for movement
        self.dx = random.uniform(-1.5, 1.5)
        self.dy = random.uniform(-1.5, 1.5)
        
        self.max_battery = 100.0
        self.battery = random.uniform(40.0, 100.0)
        self.failed = False
        
        # New specialized roles
        self.is_static = False
        self.is_immortal = False
        
    def move(self):
        """Updates the position of the node for the next simulation frame."""
        if self.failed or self.is_static:
            return
            
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off edges
        if self.x <= 0 or self.x >= self.max_x:
            self.dx *= -1
            self.x = max(0, min(self.max_x, self.x))
        if self.y <= 0 or self.y >= self.max_y:
            self.dy *= -1
            self.y = max(0, min(self.max_y, self.y))
            
        # Drain battery slowly over time
        # Random drain rate to make simulation dynamic
        drain_rate = random.uniform(0.005, 0.02)
        self.drain_battery(drain_rate)

    def drain_battery(self, amount):
        if not self.failed and not self.is_immortal:
            self.battery -= amount
            if self.battery <= 0:
                self.battery = 0
                self.failed = True

    def toggle_fail(self):
        """Manually toggle a node's operational state simulating sudden failure or repair."""
        self.failed = not self.failed
        if not self.failed and self.battery <= 0:
            self.battery = 100.0 # Reset battery on manual revival
            
    def distance_to(self, other_node):
        """Calculates Euclidean distance to another node."""
        return math.hypot(self.x - other_node.x, self.y - other_node.y)

    def to_dict(self):
        """Returns a serializable dictionary representation of the node."""
        return {
            "id": self.node_id,
            "x": self.x,
            "y": self.y,
            "battery": self.battery,
            "failed": self.failed
        }

