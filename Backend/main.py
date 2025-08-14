from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import time
import json
import os

from maze_generator import generate_maze_with_weights
from solvers.bfs import solve as bfs_solve
from solvers.dfs import solve as dfs_solve
from solvers.a_star import solve as a_star_solve
from solvers.greedy import solve as greedy_solve
from utils.hash_utils import generate_hash

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class GenerateRequest(BaseModel):
    size: int

class SolveRequest(BaseModel):
    maze: list
    weights: list
    start_point: tuple
    end_point: tuple
    algorithms: list[str]
    size: int

@app.post("/generate-maze")
def generate_maze_endpoint(data: GenerateRequest):
    start_point = (1, 1)
    end_point_coord = data.size - 2 if data.size % 2 != 0 else data.size - 3
    end_point = (end_point_coord, end_point_coord)
    
    maze, weights = generate_maze_with_weights((data.size, data.size))
    if end_point[1] < len(maze) and end_point[0] < len(maze[0]):
        maze[end_point[1]][end_point[0]] = 0

    return {
        "maze": maze,
        "weights": weights,
        "start_point": start_point,
        "end_point": end_point
    }

@app.post("/solve-maze")
def solve_maze_endpoint(data: SolveRequest):
    maze_id = str(uuid.uuid4())
    maze_structure_hash = generate_hash(data.maze)

    # --- Configurable weights for the scoring components ---
    W_TIME = 0.5  # How much speed matters (0.0 to 1.0)
    W_NODES = 0.5 # How much node efficiency matters (0.0 to 1.0)

    solvers = {
        'BFS': bfs_solve, 
        'DFS': dfs_solve, 
        'A*': a_star_solve, 
        'Greedy': greedy_solve,
    }
    results = {}

    # 1. Run all solvers and gather their raw performance metrics
    for algo_name in data.algorithms:
        solver_func = solvers.get(algo_name)
        if not solver_func:
            continue

        start_time = time.time()
        result = solver_func(data.maze, data.weights, data.start_point, data.end_point)
        end_time = time.time()

        time_taken = max((end_time - start_time) * 1000, 0.1)
        result["timeTaken"] = round(time_taken, 2)
        result["nodesExpanded"] = result.get("nodesExpanded", 1) or 1
        results[algo_name] = result

    if not results:
        return {"results": {}}

    # 2. Find the 'best' (minimum) values from this run for normalization
    # Only consider successful runs for finding the best node count
    successful_results = [r for r in results.values() if r.get("pathFound")]
    
    min_time = min(r['timeTaken'] for r in results.values())
    min_nodes = min(r['nodesExpanded'] for r in successful_results) if successful_results else float('inf')

    # 3. Calculate the new efficiency score for each algorithm
    for algo_name, result in results.items():
        
        # Calculate a time_score (0-1), where 1 is best
        time_score = min_time / result['timeTaken']
        
        # Calculate a node_score (0-1), only for successful runs
        node_score = 0
        if result.get("pathFound"):
            # Avoid division by zero if min_nodes is infinity (no successes)
            node_score = min_nodes / result['nodesExpanded'] if min_nodes != float('inf') else 0
        
        # Combine the individual scores using your weights
        final_score = (W_TIME * time_score) + (W_NODES * node_score)
        
        # Scale to 100 for a clean display score
        result["efficiencyScore"] = round(final_score * 100, 2)

    # The rest of your function (saving to a file) remains the same...
    for algo_name, result in results.items():
        full_metrics = {
            "maze_id": maze_id,
            "size": f"{data.size}x{data.size}",
            "start_point": data.start_point,
            "end_point": data.end_point,
            "algorithm_name": algo_name,
            "maze_structure_hash": maze_structure_hash,
            **result
        }
        data_folder_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_folder_path, exist_ok=True)
        file_path = os.path.join(data_folder_path, 'maze_results.json')
        try:
            with open(file_path, 'a') as f:
                f.write(json.dumps(full_metrics) + '\n')
        except IOError as e:
            print(f"Error writing to data file: {e}")

    return {"results": results}


@app.get("/get-dataset")
def get_dataset():
    data_folder_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    file_path = os.path.join(data_folder_path, 'maze_results.json')
    if not os.path.exists(file_path): return []
    dataset = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip(): dataset.append(json.loads(line))
        return dataset
    except IOError as e:
        print(f"Error reading data file: {e}")
        return {"error": "Could not read dataset file"}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)