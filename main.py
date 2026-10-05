import random
import math
import numpy as np
import matplotlib.pyplot as plt

SEED = 94
random.seed(SEED)
np.random.seed(SEED)

GRID_SIZE = 20
OBSTACLE_PERCENTAGE = 0.20

all_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

num_obstacles = int(GRID_SIZE * GRID_SIZE * OBSTACLE_PERCENTAGE)

obstacles = set(random.sample(all_cells, num_obstacles))

free_cells = [cell for cell in all_cells if cell not in obstacles]

start = random.choice(free_cells)

goal = random.choice(free_cells)

while goal == start:
    goal = random.choice(free_cells)

NUM_PARTICLES = 50
NUM_WAYPOINTS = 12
MAX_ITERATIONS = 300

INERTIA_WEIGHT = 0.7
COGNITIVE_COEFFICIENT = 1.5
SOCIAL_COEFFICIENT = 1.5

VELOCITY_LIMIT = 2.0


def distance(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2
        + (point1[1] - point2[1]) ** 2
    )


def is_collision(point):
    x, y = point

    if x < 0 or x >= GRID_SIZE:
        return True

    if y < 0 or y >= GRID_SIZE:
        return True

    cell = (int(round(x)), int(round(y)))

    return cell in obstacles


def path_cost(path):
    total_distance = 0
    collision_penalty = 0

    previous = start

    for point in path:
        total_distance += distance(previous, point)

        if is_collision(point):
            collision_penalty += 1000

        previous = point

    total_distance += distance(previous, goal)

    if is_collision(goal):
        collision_penalty += 1000

    return total_distance + collision_penalty


def create_particle():
    position = np.random.uniform(
        0,
        GRID_SIZE - 1,
        size=(NUM_WAYPOINTS, 2)
    )

    velocity = np.random.uniform(
        -1,
        1,
        size=(NUM_WAYPOINTS, 2)
    )

    return position, velocity


def smooth_path(path):
    if len(path) == 0:
        return path

    cleaned = [path[0]]

    for point in path[1:]:
        if distance(cleaned[-1], point) > 0.5:
            cleaned.append(point)

    return cleaned


particles = []

for _ in range(NUM_PARTICLES):

    position, velocity = create_particle()

    cost = path_cost(position)

    particle = {
        "position": position,
        "velocity": velocity,
        "best_position": position.copy(),
        "best_cost": cost
    }

    particles.append(particle)


global_best_particle = min(
    particles,
    key=lambda particle: particle["best_cost"]
)

global_best_position = global_best_particle["best_position"].copy()
global_best_cost = global_best_particle["best_cost"]

cost_history = []

for iteration in range(MAX_ITERATIONS):

    for particle in particles:

        r1 = np.random.random((NUM_WAYPOINTS, 2))
        r2 = np.random.random((NUM_WAYPOINTS, 2))

        cognitive = (
            COGNITIVE_COEFFICIENT
            * r1
            * (particle["best_position"] - particle["position"])
        )

        social = (
            SOCIAL_COEFFICIENT
            * r2
            * (global_best_position - particle["position"])
        )

        particle["velocity"] = (
            INERTIA_WEIGHT * particle["velocity"]
            + cognitive
            + social
        )

        particle["velocity"] = np.clip(
            particle["velocity"],
            -VELOCITY_LIMIT,
            VELOCITY_LIMIT
        )

        particle["position"] += particle["velocity"]

        particle["position"] = np.clip(
            particle["position"],
            0,
            GRID_SIZE - 1
        )

        current_cost = path_cost(particle["position"])

        if current_cost < particle["best_cost"]:

            particle["best_cost"] = current_cost

            particle["best_position"] = (
                particle["position"].copy()
            )

        if current_cost < global_best_cost:

            global_best_cost = current_cost

            global_best_position = (
                particle["position"].copy()
            )

    cost_history.append(global_best_cost)

    INERTIA_WEIGHT *= 0.995


best_waypoints = [
    tuple(point)
    for point in global_best_position
]

best_waypoints = smooth_path(best_waypoints)

final_path = [start] + best_waypoints + [goal]

final_length = 0

for i in range(len(final_path) - 1):

    final_length += distance(
        final_path[i],
        final_path[i + 1]
    )

print("=" * 60)
print("SWARM INTELLIGENCE LAB - ASSIGNMENT 1")
print("PSO-Based Path Planning with Obstacles")
print("=" * 60)

print(f"Random Seed / Roll Number : {SEED}")
print(f"Grid Size                 : {GRID_SIZE} x {GRID_SIZE}")
print(f"Number of Obstacles       : {len(obstacles)}")
print(f"Start Point               : {start}")
print(f"Goal Point                : {goal}")
print(f"Number of Particles       : {NUM_PARTICLES}")
print(f"Maximum Iterations        : {MAX_ITERATIONS}")
print(f"Final Path Length         : {final_length:.2f}")
print(f"Final PSO Cost            : {global_best_cost:.2f}")

print("\nBest Path:")

for i, point in enumerate(final_path):
    print(f"{i + 1}. ({point[0]:.2f}, {point[1]:.2f})")

print("=" * 60)

fig, ax = plt.subplots(figsize=(9, 9))

for obstacle in obstacles:

    x, y = obstacle

    rectangle = plt.Rectangle(
        (x - 0.5, y - 0.5),
        1,
        1,
        color="black"
    )

    ax.add_patch(rectangle)

path_x = [point[0] for point in final_path]
path_y = [point[1] for point in final_path]

ax.plot(
    path_x,
    path_y,
    color="blue",
    linewidth=2.5,
    marker="o",
    markersize=4,
    label="PSO Path"
)

ax.scatter(
    start[0],
    start[1],
    color="green",
    s=180,
    marker="o",
    edgecolors="black",
    label="Start",
    zorder=5
)

ax.scatter(
    goal[0],
    goal[1],
    color="red",
    s=180,
    marker="*",
    edgecolors="black",
    label="Goal",
    zorder=5
)

ax.set_xlim(-0.5, GRID_SIZE - 0.5)
ax.set_ylim(-0.5, GRID_SIZE - 0.5)

ax.set_xticks(range(GRID_SIZE))
ax.set_yticks(range(GRID_SIZE))

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

ax.set_aspect("equal")

ax.set_title(
    f"PSO Path Planning | Roll No. {SEED}\n"
    f"Path Length = {final_length:.2f}"
)

ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")

ax.legend()

plt.tight_layout()

plt.savefig(
    "final_path.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.figure(figsize=(9, 5))

plt.plot(
    cost_history,
    color="purple",
    linewidth=2
)

plt.title("PSO Convergence")

plt.xlabel("Iteration")

plt.ylabel("Best Cost")

plt.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "pso_convergence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
