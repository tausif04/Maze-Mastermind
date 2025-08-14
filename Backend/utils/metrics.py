def calculate_metrics(solver_output, time_taken):
    """
    Calculates time-based metrics and merges them with a solver's output.
    `solver_output` is a dictionary returned by the solver.
    """
    metrics = solver_output.copy()
    metrics["timeTaken"] = round(time_taken * 1000, 2)
    nodes_expanded = metrics.get("nodesExpanded", 0)
    if nodes_expanded > 0:
        metrics["efficiencyScore"] = round((1 / (nodes_expanded * max(time_taken, 1e-9))) * 10000, 2)
    else:
        metrics["efficiencyScore"] = 0
    return metrics