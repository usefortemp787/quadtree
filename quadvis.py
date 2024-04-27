import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point:
    def _init_(self, x, y):
        self.x = x
        self.y = y

class Node:
    def _init_(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points

class QTree:
    def _init_(self, k, n):
        self.threshold = k
        self.points = [Point(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]
        self.root = Node(0, 0, 10, 10, self.points)

    def add_point(self, x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points
    
    def subdivide(self):
        self._recursive_subdivide(self.root, self.threshold)
    
    def visualize(self):
        self._visualize_recursive(self.root, 0)

    def _recursive_subdivide(self, node, k):
        if len(node.points) <= k:
            return
        
        w_ = float(node.width / 2)
        h_ = float(node.height / 2)

        p = self.contains(node.x0, node.y0, w, h_, node.points)
        x1 = Node(node.x0, node.y0, w_, h_, p)
        self._recursive_subdivide(x1, k)

        p = self.contains(node.x0, node.y0 + h, w_, h_, node.points)
        x2 = Node(node.x0, node.y0 + h_, w_, h_, p)
        self._recursive_subdivide(x2, k)

        p = self.contains(node.x0 + w, node.y0, w_, h_, node.points)
        x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
        self._recursive_subdivide(x3, k)

        p = self.contains(node.x0 + w, node.y0 + h_, w_, h_, node.points)
        x4 = Node(node.x0 + w_, node.y0 + h_, w_, h_, p)
        self._recursive_subdivide(x4, k)

        node.children = [x1, x2, x3, x4]

    def _contains(self, x, y, w, h, points):
        pts = []
        for point in points:
            if x <= point.x <= x + w and y <= point.y <= y + h:
                pts.append(point)
        return pts

    def _visualize_recursive(self, node, depth):
        if not node.children:
            plt.gca().add_patch(patches.Rectangle((node.x0, node.y0), node.width, node.height, fill=False, edgecolor='black'))
            return
        for child in node.children:
            self._visualize_recursive(child, depth + 1)

# Example usage:
qtree = QTree(4, 50)
qtree.subdivide()
qtree.visualize()

# Plot points with random colors
colors = [(random.random(), random.random(), random.random()) for _ in range(len(qtree.get_points()))]
plt.scatter([p.x for p in qtree.get_points()], [p.y for p in qtree.get_points()], color=colors)

plt.gca().set_aspect('equal', adjustable='box')
plt.title("Quadtree Visualization")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()