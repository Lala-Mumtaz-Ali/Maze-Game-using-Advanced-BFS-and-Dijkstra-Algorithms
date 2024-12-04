import heapq



# Directions for Up, Down, Left, Right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # U, D, L, R

def dijkstra(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Priority Queue for Dijkstra's algorithm (stores (cost, x, y))
    pq = []

    # Initialize distances and previous node trackers
    dist = [[float('inf')] * cols for _ in range(rows)]
    prev = [[None] * cols for _ in range(rows)]

    # Start position
    start_x, start_y = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c].getText() == 'S':  # Find the start
                start_x, start_y = c, r
                dist[start_y][start_x] = 0  # Starting point has distance 0
                heapq.heappush(pq, (0, start_x, start_y))  # Push the start into the priority queue
                print(f"Start found at ({start_x}, {start_y})")  # Debugging line
                break
    # End position
    end_x, end_y = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c].getText() == 'E':  # Find the end
                end_x, end_y = c, r
                print(f"End found at ({end_x}, {end_y})")  # Debugging line
                break

    # Ensure 'E' was found
    if end_x is None or end_y is None:
        print("End point 'E' not found.")
        return [], float('inf')  # Return an empty path and infinity weight if no end point is found

    print("Starting Dijkstra's Algorithm...")
    finalx = end_x
    finaly = end_y
    # Dijkstra's algorithm
    while pq:
        current_dist, x, y = heapq.heappop(pq)

        # If we've reached the end, no need to process further
        if x == end_x and y == end_y:
            print(f"Reached end at ({end_x}, {end_y}) with distance: {current_dist}")  # Debugging line
            break

        # Explore neighbors
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx].getText() != '#':
                # Use the weight of the current cell to determine the cost of the move
                weight = grid[ny][nx].weight  # Get the weight of the neighbor cell
                new_dist = current_dist + weight  # Use the weight for each move
                if new_dist < dist[ny][nx]:
                    dist[ny][nx] = new_dist
                    prev[ny][nx] = (x, y)
                    heapq.heappush(pq, (new_dist, nx, ny))
                    print(f"Updated dist[{ny}][{nx}] to {new_dist} from ({x}, {y})")  # Debugging line

    # Debug: Print the distance grid
    print("Final Distance Grid:")
    for row in dist:
        print(row)

    if dist[finalx][finaly] == 0:
        if dist[finaly][finalx] != 0:
            temp = finalx
            finalx = finaly
            finaly = temp
    
    # Reconstruct path by backtracking from the end
    path = []
    print(f"Backtracking from end: ({end_x}, {end_y})")
    while prev[end_y][end_x] is not None:
        prev_x, prev_y = prev[end_y][end_x]
        if prev_x == end_x:
            if prev_y < end_y:
                path.append('D')  # Move Down
            else:
                path.append('U')  # Move Up
        elif prev_y == end_y:
            if prev_x < end_x:
                path.append('R')  # Move Right
            else:
                path.append('L')  # Move Left
        end_x, end_y = prev_x, prev_y


    

    path.reverse()  # The path was backtracked, so reverse it
    total_weight = dist[finalx][finaly]  # The total weight of the shortest path

    # If the end point is still infinity, no path exists
    if total_weight == float('inf'):
        path = []

    

    print(f"End found at ({finalx}, {finaly})")
    print(f"Shortest path: {''.join(path)} with total weight: {total_weight}")  # Debugging line
    return ''.join(path), total_weight
