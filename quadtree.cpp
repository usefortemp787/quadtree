#include <iostream>
#include <vector>

class Point
{
public:
    double x;
    double y;
    Point(double x, double y)
        : x(x), y(y)
    {
    }
};
class Quadtree
{
private:
    static const int MAX_CAPACITY = 4;
    static const int MAX_DEPTH = 10;
    class QuadtreeNode
    {
    public:
        double xMin;
        double yMin;
        double xMax;
        double yMax;
        std::vector<Point> points;
        QuadtreeNode *nw;
        QuadtreeNode *ne;
        QuadtreeNode *sw;
        QuadtreeNode *se;
        QuadtreeNode(double xMin, double yMin, double xMax,
                     double yMax)
            : xMin(xMin), yMin(yMin), xMax(xMax), yMax(yMax), nw(nullptr), ne(nullptr), sw(nullptr), se(nullptr)
        {
        }
    };
    QuadtreeNode *root;
    void insertHelper(QuadtreeNode *node, const Point &Point,
                      int depth);
    void queryRangeHelper(QuadtreeNode *node,
                          const double &xMin,
                          const double &yMin,
                          const double &xMax,
                          const double &yMax,
                          std::vector<Point> &result) const;

public:
    Quadtree(double xMin, double yMin, double xMax,
             double yMax);
    ~Quadtree();
    void insert(const Point &Point);
    std::vector<Point> queryRange(const double &xMin,
                                  const double &yMin,
                                  const double &xMax,
                                  const double &yMax) const;
};
Quadtree::Quadtree(double xMin, double yMin, double xMax,
                   double yMax)
{
    root = new QuadtreeNode(xMin, yMin, xMax, yMax);
}
Quadtree::~Quadtree() {}

void Quadtree::insertHelper(QuadtreeNode *node,
                            const Point &Point, int depth)
{
    if (depth >= MAX_DEPTH || node == nullptr)
        return;
    if (node->points.size() < MAX_CAPACITY)
    {
        node->points.push_back(Point);
    }
    else
    {
        double xMid = (node->xMin + node->xMax) / 2.0;
        double yMid = (node->yMin + node->yMax) / 2.0;

        if (Point.x <= xMid)
        {
            if (Point.y <= yMid)
            {
                if (node->nw == nullptr)
                    node->nw = new QuadtreeNode(
                        node->xMin, node->yMin, xMid, yMid);
                insertHelper(node->nw, Point, depth + 1);
            }
            else
            {
                if (node->sw == nullptr)
                    node->sw = new QuadtreeNode(
                        node->xMin, yMid, xMid, node->yMax);
                insertHelper(node->sw, Point, depth + 1);
            }
        }
        else
        {
            if (Point.y <= yMid)
            {
                if (node->ne == nullptr)
                    node->ne = new QuadtreeNode(
                        xMid, node->yMin, node->xMax, yMid);
                insertHelper(node->ne, Point, depth + 1);
            }
            else
            {
                if (node->se == nullptr)
                    node->se = new QuadtreeNode(
                        xMid, yMid, node->xMax, node->yMax);
                insertHelper(node->se, Point, depth + 1);
            }
        }
    }
}
void Quadtree::insert(const Point &Point)
{
    insertHelper(root, Point, 0);
}
void Quadtree::queryRangeHelper(
    QuadtreeNode *node, const double &xMin,
    const double &yMin, const double &xMax,
    const double &yMax, std::vector<Point> &result) const
{
    if (node == nullptr)
        return;
    for (const Point &Point : node->points)
    {
        if (Point.x >= xMin && Point.x <= xMax && Point.y >= yMin && Point.y <= yMax)
            result.push_back(Point);
    }
    double xMid = (node->xMin + node->xMax) / 2.0;
    double yMid = (node->yMin + node->yMax) / 2.0;
    if (xMin <= xMid && yMin <= yMid)
        queryRangeHelper(node->nw, xMin, yMin, xMax, yMax,
                         result);
    if (xMin <= xMid && yMax >= yMid)
        queryRangeHelper(node->sw, xMin, yMin, xMax, yMax,
                         result);
    if (xMax >= xMid && yMin <= yMid)
        queryRangeHelper(node->ne, xMin, yMin, xMax, yMax,
                         result);
    if (xMax >= xMid && yMax >= yMid)
        queryRangeHelper(node->se, xMin, yMin, xMax, yMax,
                         result);
}
std::vector<Point>
Quadtree::queryRange(const double &xMin, const double &yMin,
                     const double &xMax,
                     const double &yMax) const
{
    std::vector<Point> result;
    queryRangeHelper(root, xMin, yMin, xMax, yMax, result);
    return result;
}
int main()
{
    Quadtree quadtree(0.0, 0.0, 100.0, 100.0);
    quadtree.insert(Point(20.0, 30.0));
    quadtree.insert(Point(40.0, 50.0));
    quadtree.insert(Point(60.0, 70.0));
    quadtree.insert(Point(80.0, 90.0));
    std::vector<Point> pointsInRange = quadtree.queryRange(0.0, 0.0, 50.0, 50.0);
    for (const Point &Point : pointsInRange)
    {
        std::cout << "Point: (" << Point.x << ", "
                  << Point.y << ")\n";
    }
    return 0;
}
