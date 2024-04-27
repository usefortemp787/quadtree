class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Quadtree:
    MAX_CAPACITY = 4
    MAX_DEPTH = 10

    class QuadtreeNode:
        def __init__(self, xMin, yMin, xMax, yMax):
            self.xMin = xMin
            self.yMin = yMin
            self.xMax = xMax
            self.yMax = yMax
            self.points = []
            self.nw = None
            self.ne = None
            self.sw = None
            self.se = None

    def __init__(self, xMin, yMin, xMax, yMax):
        self.root = self.QuadtreeNode(xMin, yMin, xMax, yMax)

    def insert(self, point):
        self.insertHelper(self.root, point, 0)

    def insertHelper(self, node, point, depth):
        if depth >= self.MAX_DEPTH or node is None:
            return
        if len(node.points) < self.MAX_CAPACITY:
            node.points.append(point)
        else:
            xMid = (node.xMin + node.xMax) / 2.0
            yMid = (node.yMin + node.yMax) / 2.0

            if point.x <= xMid:
                if point.y <= yMid:
                    if node.nw is None:
                        node.nw = self.QuadtreeNode(node.xMin, node.yMin, xMid, yMid)
                    self.insertHelper(node.nw, point, depth + 1)
                else:
                    if node.sw is None:
                        node.sw = self.QuadtreeNode(node.xMin, yMid, xMid, node.yMax)
                    self.insertHelper(node.sw, point, depth + 1)
            else:
                if point.y <= yMid:
                    if node.ne is None:
                        node.ne = self.QuadtreeNode(xMid, node.yMin, node.xMax, yMid)
                    self.insertHelper(node.ne, point, depth + 1)
                else:
                    if node.se is None:
                        node.se = self.QuadtreeNode(xMid, yMid, node.xMax, node.yMax)
                    self.insertHelper(node.se, point, depth + 1)

    def queryRange(self, xMin, yMin, xMax, yMax):
        result = []
        self.queryRangeHelper(self.root, xMin, yMin, xMax, yMax, result)
        return result

    def queryRangeHelper(self, node, xMin, yMin, xMax, yMax, result):
        if node is None:
            return
        for p in node.points:
            if xMin <= p.x <= xMax and yMin <= p.y <= yMax:
                result.append(p)
        xMid = (node.xMin + node.xMax) / 2.0
        yMid = (node.yMin + node.yMax) / 2.0
        if xMin <= xMid and yMin <= yMid:
            self.queryRangeHelper(node.nw, xMin, yMin, xMax, yMax, result)
        if xMin <= xMid and yMax >= yMid:
            self.queryRangeHelper(node.sw, xMin, yMin, xMax, yMax, result)
        if xMax >= xMid and yMin <= yMid:
            self.queryRangeHelper(node.ne, xMin, yMin, xMax, yMax, result)
        if xMax >= xMid and yMax >= yMid:
            self.queryRangeHelper(node.se, xMin, yMin, xMax, yMax, result)

# Example usage
quadtree = Quadtree(0.0, 0.0, 100.0, 100.0)
quadtree.insert(Point(20.0, 30.0))
quadtree.insert(Point(40.0, 50.0))
quadtree.insert(Point(60.0, 70.0))
quadtree.insert(Point(80.0, 90.0))
pointsInRange = quadtree.queryRange(0.0, 0.0, 50.0, 50.0)
for p in pointsInRange:
    print(f"Point: ({p.x}, {p.y})")
