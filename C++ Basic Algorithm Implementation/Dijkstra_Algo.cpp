#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// A pair representing (distance, vertex)
typedef pair<int, int> pii;

// Function to find the shortest paths from the source to all vertices
vector<int> dijkstra(int start, const vector<vector<pii>> &graph)
{
    int n = graph.size();                              // Number of vertices
    vector<int> dist(n, INT_MAX);                      // Distance from source to each vertex
    priority_queue<pii, vector<pii>, greater<pii>> pq; // Min-heap for priority queue

    // Initialize the source vertex
    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty())
    {
        int current_dist = pq.top().first; // Distance to the current vertex
        int current_vertex = pq.top().second;
        pq.pop();

        // Skip processing if we already found a shorter path
        if (current_dist > dist[current_vertex])
        {
            continue;
        }

        // Explore neighbors
        for (const auto &neighbor : graph[current_vertex])
        {
            int next_vertex = neighbor.first;
            int weight = neighbor.second;
            int new_dist = current_dist + weight;

            // Update if a shorter path is found
            if (new_dist < dist[next_vertex])
            {
                dist[next_vertex] = new_dist;
                pq.push({new_dist, next_vertex});
            }
        }
    }

    return dist; // Return the distance array
}

int main()
{
    // Hardcoded graph as an adjacency list
    // Vertex 0 connects to vertex 1 (weight 2) and vertex 2 (weight 4)
    // Vertex 1 connects to vertex 2 (weight 1) and vertex 3 (weight 7)
    // Vertex 2 connects to vertex 4 (weight 3)
    // Vertex 3 connects to vertex 4 (weight 1)
    vector<vector<pii>> graph = {
        {{1, 2}, {2, 4}},         // Neighbors of vertex 0
        {{0, 2}, {2, 1}, {3, 7}}, // Neighbors of vertex 1
        {{0, 4}, {1, 1}, {4, 3}}, // Neighbors of vertex 2
        {{1, 7}, {4, 1}},         // Neighbors of vertex 3
        {{2, 3}, {3, 1}}          // Neighbors of vertex 4
    };

    int start = 0; // Hardcoded starting vertex

    // Run Dijkstra's algorithm
    vector<int> distances = dijkstra(start, graph);

    // Output shortest distances
    cout << "Shortest distances from vertex " << start << ":\n";
    for (int i = 0; i < distances.size(); ++i)
    {
        cout << "Vertex " << i << ": " << (distances[i] == INT_MAX ? -1 : distances[i]) << endl;
    }

    return 0;
}
