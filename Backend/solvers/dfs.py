# --- backend/solvers/dfs.py ---
def solve(maze, weights, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]
    visited = {start}
    visited_in_order = []
    max_depth = 0
    
    max_stack_size = 1

    while stack:
        (x, y), path = stack.pop()
        
     
        max_depth = max(max_depth, len(path))
        max_stack_size = max(max_stack_size, len(stack) + 1) 
        
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
    
                "tree_width": max_stack_size
            }
            
     
        for dx, dy in reversed([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))
                
    return {"pathFound": False, "pathCost": -1, "nodesExpanded": len(visited), "solution_path": [], "visited_nodes_in_order": visited_in_order, "tree_depth": max_depth, "tree_width": max_stack_size}