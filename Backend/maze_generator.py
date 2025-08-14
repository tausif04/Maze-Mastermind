# import random
# from typing import List, Tuple

# def generate_maze_with_weights(size: Tuple[int, int]) -> Tuple[List[List[int]], List[List[int]]]:
#     width, height = size
#     width = width if width % 2 != 0 else width + 1
#     height = height if height % 2 != 0 else height + 1

#     maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
#     weights = [[1 for _ in range(width)] for _ in range(height)]  # Weights for each cell

#     def carve_passages(cx: int, cy: int):
#         directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
#         random.shuffle(directions)

#         for dx, dy in directions:
#             nx, ny = cx + dx, cy + dy
#             if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
#                 maze[cy + dy // 2][cx + dx // 2] = 0
#                 maze[ny][nx] = 0
#                 carve_passages(nx, ny)

#     # Start at a random odd cell
#     start_x = random.randrange(1, width, 2)
#     start_y = random.randrange(1, height, 2)
#     maze[start_y][start_x] = 0
#     carve_passages(start_x, start_y)

#     # Assign random weights to path cells
#     for y in range(height):
#         for x in range(width):
#             if maze[y][x] == 0:
#                 weights[y][x] = random.randint(1, 9)

#     return maze, weights

# // -- wilson algo --
import random
from typing import Dict, Tuple, Optional, List

def generate_maze_with_weights(size: Tuple[int, int]) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Generates a solvable maze using Wilson's Algorithm to create a
    Uniform Spanning Tree (UST), then assigns random weights to paths.
    """
    width, height = size
    width = width if width % 2 != 0 else width + 1
    height = height if height % 2 != 0 else height + 1
    
    maze: List[List[int]] = [[1 for _ in range(width)] for _ in range(height)]
    weights: List[List[int]] = [[1 for _ in range(width)] for _ in range(height)]

    in_maze: set[Tuple[int, int]] = set()
    first_x, first_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    in_maze.add((first_x, first_y))
    maze[first_y][first_x] = 0

    unvisited: List[Tuple[int, int]] = []
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            if (x, y) != (first_x, first_y):
                unvisited.append((x, y))
    
    random.shuffle(unvisited)

    while unvisited:
        start_x, start_y = unvisited.pop()
        path: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {(start_x, start_y): None}
        current_x, current_y = start_x, start_y

        while (current_x, current_y) not in in_maze:
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 < ny < height and 0 < nx < width:
                    path[(current_x, current_y)] = (dx, dy)
                    current_x, current_y = nx, ny
                    break
        
        cell_x, cell_y = start_x, start_y
        while (cell_x, cell_y) not in in_maze:
            in_maze.add((cell_x, cell_y))
            if (cell_x, cell_y) in unvisited:
                unvisited.remove((cell_x, cell_y))
            
            maze[cell_y][cell_x] = 0
            
            direction = path.get((cell_x, cell_y))
            if direction:
                dx, dy = direction
                maze[cell_y + dy // 2][cell_x + dx // 2] = 0
                cell_x += dx
                cell_y += dy
            else:
                break

    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:
                weights[y][x] = random.randint(1, 9)

    return maze, weights  
