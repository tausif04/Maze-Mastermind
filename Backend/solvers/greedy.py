# --- backend/solvers/greedy.py ---
import heapq

def heuristic(a, b, weight=1):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy) * weight  # Scaled Manhattan

def solve(maze, weights, start, end):
    rows, cols = len(maze), len(maze[0])
    open_set = [(heuristic(start, end), start, [start])]
    
    visited = {start}
    visited_in_order = []

  
    max_width = 1
    max_depth = 0

    while open_set:
     
        max_width = max(max_width, len(open_set) + 1) 

        _, (x, y), path = heapq.heappop(open_set)
        
        max_depth = max(max_depth, len(path))
        
 
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

                "tree_depth": max_depth,
                "tree_width": max_width
            }
            
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                priority = heuristic((nx, ny), end)
                heapq.heappush(open_set, (priority, (nx, ny), path + [(nx, ny)]))
                
    return {
        "pathFound": False,
        "pathCost": -1,
        "nodesExpanded": len(visited),
        "solution_path": [],
        "visited_nodes_in_order": visited_in_order,
        "tree_depth": max_depth,
        "tree_width": max_width
    }