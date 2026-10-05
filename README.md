Swarm-Based Path Planning with Obstacles
Swarm Intelligence Lab — Assignment 1
Student Information

Name: Shayan Malik

Roll Number: 94

Random Seed: 94

Course: Swarm Intelligence Lab

Assignment: Assignment 1 — Swarm-Based Path Planning with Obstacles

Project Description

This project implements Particle Swarm Optimization (PSO) to find a short path from a start point to a goal point on a 2D grid while avoiding randomly generated obstacles.

The problem instance is generated programmatically using the student's roll number as the random seed. For this project, the seed is 94, which makes the generated grid, obstacles, start point, and goal point specific to this assignment.

Approach

The algorithm uses Particle Swarm Optimization to search for a suitable path.

Each particle represents a candidate path containing several intermediate waypoints. During each iteration, particles update their velocities and positions using:

Inertia

Personal best position

Global best position

Each candidate path is evaluated using a cost function based mainly on path length. A large penalty is added when a waypoint lies on an obstacle or outside the grid.

The particle with the best cost becomes the global best solution. After the maximum number of iterations, the best path found by PSO is displayed and visualized.

Problem Generation

The grid size and obstacle locations are generated programmatically.

The random seed is:

94


The seed ensures that the same student gets the same problem instance when the program is executed again.

The start and goal points are selected from free cells so that they are not placed on obstacles.

PSO Parameters

The implementation uses:

Number of particles: 50

Number of waypoints: 12

Maximum iterations: 300

Initial inertia weight: 0.7

Cognitive coefficient: 1.5

Social coefficient: 1.5

Technologies Used

Python

NumPy

Matplotlib

Git and GitHub

How to Run
1. Install Python

Python 3 or later is required.

2. Install the required libraries

Open a terminal in the project folder and run:

python -m pip install -r requirements.txt

3. Run the program
python main.py


The program prints the generated problem information, the best path, path length, and PSO cost.

It also generates visualizations of the final path and PSO convergence.

Output

The final path visualization contains:

Black cells — obstacles

Green circle — start point

Red star — goal point

Blue line — path found by PSO

The program also generates a convergence graph showing how the best PSO cost changes over the iterations.

Project Files
swarm-pathplanning-94/
│
├── main.py
├── requirements.txt
├── final_path.png
├── pso_convergence.png
├── flow_diagram.jpg
└── README.md

## Hand-Drawn Flow Diagram

The algorithm flow diagram is drawn by hand on paper and photographed for inclusion in this repository.

![Hand-Drawn PSO Flow Diagram](flow_diagram.jpg)

Conclusion

Particle Swarm Optimization was used to search for a short path between a randomly generated start and goal point while considering obstacles in a 2D grid.

The use of roll number 94 as the random seed makes the generated problem instance unique to the student.

Author

Shayan Malik
Roll Number: 94