import hashlib
import json
def generate_hash(maze):
    maze_str = json.dumps(maze, sort_keys=True)
    return hashlib.md5(maze_str.encode()).hexdigest()