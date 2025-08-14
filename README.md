# 🧩 Maze Master Mind

Maze Master Mind is an interactive maze generation and solving application built with **FastAPI** (backend) and **Vite + React** (frontend).  
It supports multiple solving algorithms and ranks them based on an `efficiencyScore`.

## 📌 Features
- **Maze Generation**  
  - Generates mazes with weighted paths
  - Adjustable size and complexity
    
- **Maze Solving**  
  - BFS (Breadth-First Search)  
  - DFS (Depth-First Search)  
  - A* Search  
  - Greedy Best-First Search

- **Algorithm Ranking**  
  - Calculates `efficiencyScore` for each algorithm
  - Ranks them from most to least efficient

- **Visualization**  
  - Interactive frontend built with **Vite + React**
  - Real-time API calls to backend
  - Responsive maze rendering

- **Cloud Integration** (Azure)  
  - Application Insights  
  - Cosmos DB  
  - Azure Container Registry  
  - Azure Machine Learning Workspace  
  - Key Vault & Virtual Network

## 🛠️ Tech Stack

### **Frontend**
- [React](https://react.dev/) (Vite)
- JavaScript/TypeScript
- Tailwind CSS (optional, for styling)
- Axios / Fetch API

### **Backend**
- [FastAPI](https://fastapi.tiangolo.com/)
- Python 3.10+
- Pydantic v2
- Custom algorithm modules in `solvers/` and `utils/`
