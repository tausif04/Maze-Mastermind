# --- backend/solvers/bfs.py ---
from collections import deque

def solve(maze, weights, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = {start}
    visited_in_order = []

    # 1. Initialize a variable to track the max width
    max_queue_size = 1

    while queue:
        # 2. Update the max width at the beginning of each level's expansion
        #    This is the most accurate point for a level-by-level (BFS) approach.
        max_queue_size = max(max_queue_size, len(queue))

        (x, y), path = queue.popleft()
        if (x, y) != start:
            visited_in_order.append((x,y))
        
        if (x, y) == end:
            path_cost = sum(weights[ny][nx] for nx, ny in path)
            return {
                "pathFound": True,
                "pathCost": path_cost,
                "nodesExpanded": len(visited),
                "solution_path": path,
                "visited_nodes_in_order": visited_in_order,
                "tree_depth": len(path),
                # 3. Use the correct max width
                "tree_width": max_queue_size
            }

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
                
    return {"pathFound": False, "pathCost": -1, "nodesExpanded": len(visited), "solution_path": [], "visited_nodes_in_order": visited_in_order, "tree_depth": 0, "tree_width": max_queue_size}