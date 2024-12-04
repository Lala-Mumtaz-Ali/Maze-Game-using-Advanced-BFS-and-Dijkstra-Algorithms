#include <iostream>
#include <queue>
#include <vector>

using namespace std;

class Graph {
private:
    int V; // Number of vertices
    vector<vector<int>> adjList; // Adjacency list representation

public:
    Graph(int vertices) : V(vertices), adjList(vertices) {}

    void addEdge(int v, int w) {
        adjList[v].push_back(w);
    }

    void BFS(int start) {
        vector<bool> visited(V, false); // Mark all vertices as not visited
        queue<int> q; // Create a queue for BFS

        visited[start] = true; // Mark the current node as visited and enqueue it
        q.push(start);

        while (!q.empty()) {
            start = q.front(); // Dequeue a vertex from the queue and print it
            cout << start << " ";
            q.pop();

            // Get all adjacent vertices of the dequeued vertex. If an adjacent vertex has not been visited,
            // mark it visited and enqueue it.
            for (const auto& neighbor : adjList[start]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
};

int main() {
    // Example usage:
    Graph g(6);

    // Adding edges to the graph
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);
    g.addEdge(2, 4);
    g.addEdge(3, 5);
    g.addEdge(4, 5);

    cout << "BFS starting from vertex 0:" << endl;
    g.BFS(0);

    return 0;
}
