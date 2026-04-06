# """
# rl_route_qlearning.py

# Tabular Q-learning for small-scale delivery route optimization:
# - State: (current_node, visited_mask)
# - Action: choose next node to visit
# - Reward: negative distance for each move (shorter routes => higher total reward)
# - Penalty for returning to depot early
# - Episode ends when agent has visited all nodes and returned to depot

# Works well for N up to ~8 (state space grows as N * 2^N).
# """

import numpy as np
import random
from itertools import permutations, combinations
import math

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


# Create sample problem

def make_distance_matrix(coords):
    n = len(coords)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                D[i, j] = 0.0
            else:
                D[i, j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return D

# Example: 6 locations (0 = depot)
N = 6
coords = [
    (50, 50),  # depot
    (60, 60),
    (65, 40),
    (40, 65),
    (30, 50),
    (55, 30),
]
dist_matrix = make_distance_matrix(coords)


# Q-learning setup

num_nodes = N
ALL_VISITED_MASK = (1 << num_nodes) - 1 

# Q-table: shape (num_nodes, 2^num_nodes)
Q = np.zeros((num_nodes, 1 << num_nodes))  # Q[current_node, visited_mask]

# hyperparameters
alpha = 0.1        # learning rate
gamma = 0.95       # discount factor
epsilon = 0.9      # initial exploration prob
min_epsilon = 0.01
epsilon_decay = 0.9995
n_episodes = 40000
max_steps_per_episode = 4 * num_nodes

def allowed_actions(current, visited_mask):
    """Return list of candidate next nodes (cannot stay in same node)."""
    actions = []
    for node in range(num_nodes):
        if node == current:
            continue
        actions.append(node)
    return actions

def is_all_targets_visited(visited_mask):
    """We consider nodes 1..(N-1) as targets; depot index 0 is considered visited initially."""
    # A simple approach: check that bits for nodes 1..N-1 are set
    needed_mask = 0
    for i in range(1, num_nodes):
        needed_mask |= (1 << i)
    return (visited_mask & needed_mask) == needed_mask

def step(current, visited_mask, action):
    """
    Take action (move to action node).
    Returns: next_current, next_visited_mask, reward, done
    """
    dist = dist_matrix[current, action]
    reward = -dist  # negative distance as cost; we want to maximize reward (minimize total distance)
    next_visited = visited_mask | (1 << action)

    done = False
    # If agent returns to depot (node 0) before visiting all, heavy penalty (discourage)
    if action == 0 and not is_all_targets_visited(next_visited):
        reward += -50.0  # big penalty
        # we do NOT end episode; agent can continue, but it's suboptimal
    # Episode ends when we've visited all targets and are back at depot
    if action == 0 and is_all_targets_visited(next_visited):
        done = True
        reward += 100.0  # bonus for finishing (encourage completing route)
    return action, next_visited, reward, done


# Training loop

for episode in range(n_episodes):
    current = 0  # start at depot
    visited = 1 << 0  # mark depot as visited
    for step_idx in range(max_steps_per_episode):
        # choose action
        if random.random() < epsilon:
            action = random.choice(allowed_actions(current, visited))
        else:
            # greedy among allowed actions
            actions = allowed_actions(current, visited)
            q_values = [Q[a, visited] for a in actions]
            max_q = max(q_values)
            # pick randomly among ties
            best_actions = [a for a, qv in zip(actions, q_values) if abs(qv - max_q) < 1e-8]
            action = random.choice(best_actions)

        next_current, next_visited, reward, done = step(current, visited, action)

        # Q update: Q[current, visited] = (1-alpha)*Q + alpha*(reward + gamma*max_a' Q[next_current, next_visited])
        # but when next state is terminal, future value = 0
        if done:
            future_val = 0.0
        else:
            # consider allowed actions from next_current
            next_actions = allowed_actions(next_current, next_visited)
            future_val = max([Q[a, next_visited] for a in next_actions]) if next_actions else 0.0

        old_q = Q[current, visited]
        Q[current, visited] = (1 - alpha) * old_q + alpha * (reward + gamma * future_val)

        current, visited = next_current, next_visited

        if done:
            break

    # decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)


# Derive greedy route from Q-table

def get_greedy_route_from_q():
    route = [0]
    current = 0
    visited = 1 << 0
    steps = 0
    while True:
        steps += 1
        actions = allowed_actions(current, visited)
        # pick best Q
        q_vals = [Q[a, visited] for a in actions]
        max_q = max(q_vals)
        best_actions = [a for a, qv in zip(actions, q_vals) if abs(qv - max_q) < 1e-8]
        action = random.choice(best_actions)
        route.append(action)
        visited |= (1 << action)
        current = action
        # if finished visiting all and back at depot, stop
        if current == 0 and is_all_targets_visited(visited):
            break
        if steps > num_nodes * 3:
            # fallback: break to prevent infinite loops
            break
    return route

def route_cost(route):
    cost = 0.0
    for i in range(len(route) - 1):
        cost += dist_matrix[route[i], route[i+1]]
    return cost

learned_route = get_greedy_route_from_q()
learned_cost = route_cost(learned_route)

print("Learned greedy route (including depot returns):", learned_route)
print("Learned route total distance: {:.3f}".format(learned_cost))


# Optional: brute-force optimal route for comparison (small N)

def brute_force_tsp():
    nodes = list(range(1, num_nodes))
    best_route = None
    best_cost = float('inf')
    for perm in permutations(nodes):
        route = [0] + list(perm) + [0]
        c = route_cost(route)
        if c < best_cost:
            best_cost = c
            best_route = route
    return best_route, best_cost

opt_route, opt_cost = brute_force_tsp()
print("Optimal (brute-force) route:", opt_route)
print("Optimal route total distance: {:.3f}".format(opt_cost))

# show improvement
improvement = (opt_cost - learned_cost) / opt_cost * 100.0
print("Learned vs Optimal improvement (negative means worse than optimum): {:.2f}%".format(improvement))
