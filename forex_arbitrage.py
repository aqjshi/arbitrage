import os
import json
import math

# Initialize empty dictionaries and lists for vertices and edges
forex_data = {}
vertices = set()
edges = []

# Load all JSON files in the 'forex' folder
for filename in os.listdir('forex'):
    if filename.endswith('.json'):
        with open(os.path.join('forex', filename), 'r') as file:
            # Identify base currency from filename, excluding '_exchange_rates.json' suffix
            base_currency = filename.split('_')[0]
            vertices.add(base_currency)  # Add base currency to vertex set
            
            # Parse the JSON file for exchange rates
            data = json.load(file)
            forex_data[base_currency] = data.get('conversion_rates', {})

            # Add edges from base_currency to each target currency in conversion rates
            for target_currency, rate in forex_data[base_currency].items():
                edges.append((base_currency, target_currency, rate))
                vertices.add(target_currency)

# Apply logarithmic transformation to edge weights to use Bellman-Ford for arbitrage detection
def apply_log_weight(edges):
    return [(u, v, -math.log(rate)) for u, v, rate in edges]

# Bellman-Ford algorithm to detect negative-weight cycles and log arbitrage transactions
def bellman_ford(vertices, edges, start_vertex):
    # Initialize distances and predecessors
    distance = {v: float('inf') for v in vertices}
    predecessor = {v: None for v in vertices}
    distance[start_vertex] = 0

    # Relax edges |V| - 1 times
    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u

    # Check for negative-weight cycles
    for u, v, weight in edges:
        if distance[u] + weight < distance[v]:
            return trace_arbitrage_cycle(predecessor, v, edges)
    
    return False

# Helper function to trace the arbitrage cycle
def trace_arbitrage_cycle(predecessor, start, edges):
    cycle = []
    visited = set()
    current = start

    # Backtrack to find the cycle
    while current not in visited:
        visited.add(current)
        current = predecessor[current]

    # Capture the cycle
    cycle_start = current
    while True:
        cycle.append(current)
        current = predecessor[current]
        if current == cycle_start:
            cycle.append(current)
            break

    # Log the sequence of transactions and calculate profit starting with 1 USD
    log_arbitrage_cycle(cycle[::-1], edges)  # Reverse the cycle for correct order
    return cycle[::-1]  # Return the detected cycle

# Function to log and calculate the profit of the arbitrage cycle
def log_arbitrage_cycle(cycle, edges):
    amount = 1  # Start with 1 unit of the initial currency
    print("\nArbitrage Cycle Detected:")
    print(f"Starting with {amount} unit of {cycle[0]}")

    for i in range(len(cycle) - 1):
        u, v = cycle[i], cycle[i+1]
        rate = next(rate for x, y, rate in edges if x == u and y == v)
        amount *= math.exp(-rate)
        print(f"Convert {u} to {v} at rate {math.exp(-rate):.4f}, New amount: {amount:.6f}")

    print(f"Ending with {amount:.6f} units of {cycle[0]}")
    if amount > 1:
        print("Arbitrage opportunity confirmed!\n")
    else:
        print("No profitable arbitrage in this cycle.\n")

# Function to find arbitrage opportunities starting from 1 USD
def find_arbitrage(vertices, edges):
    # Apply logarithmic transformation to the exchange rates
    log_edges = apply_log_weight(edges)
    
    start_vertex = "USD"  # Start arbitrage search from "USD"
    if start_vertex in vertices:
        print(f"Checking for arbitrage starting at {start_vertex}")
        if bellman_ford(vertices, log_edges, start_vertex):
            print(f"Arbitrage opportunity detected starting from {start_vertex}!")
            return
    print("No arbitrage opportunities detected.\n")

# Run the arbitrage detection function
find_arbitrage(vertices, edges)
