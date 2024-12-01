import time
from math import sqrt, exp
import random
import tkinter
from GLOBAL_VARIABLES import *


def distanceSA(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def total_path_length(tour):
    length = 0
    for i in range(len(tour) - 1):
        length += distanceSA(Verticies[tour[i]], Verticies[tour[i + 1]])
    length += distanceSA(Verticies[tour[-1]], Verticies[tour[0]])  # Return to starting point
    return length



def delta_path_length(tour, i, j):
    n = len(tour)

    if i == j:
        return 0

    if i > j:
        i, j = j, i

    if i == j - 1:
        orig_dist = distanceSA(Verticies[tour[i]], Verticies[tour[j]]) + distanceSA(Verticies[tour[j]], Verticies[tour[(j + 1) % n]])
        new_dist = distanceSA(Verticies[tour[i]], Verticies[tour[(j + 1) % n]]) + distanceSA(Verticies[tour[j]], Verticies[tour[i]])
    else:
        orig_dist = (
            distanceSA(Verticies[tour[i]], Verticies[tour[i - 1]]) + distanceSA(Verticies[tour[i]], Verticies[tour[(i + 1) % n]]) +
            distanceSA(Verticies[tour[j]], Verticies[tour[j - 1]]) + distanceSA(Verticies[tour[j]], Verticies[tour[(j + 1) % n]])
        )
        new_dist = (
            distanceSA(Verticies[tour[j]], Verticies[tour[i - 1]]) + distanceSA(Verticies[tour[j]], Verticies[tour[(i + 1) % n]]) +
            distanceSA(Verticies[tour[i]], Verticies[tour[j - 1]]) + distanceSA(Verticies[tour[i]], Verticies[tour[(j + 1) % n]])
        )

    return new_dist - orig_dist




def edges_cross(p1, p2, q1, q2):
    def orientation(p, q, r):
        # Helper function to find the orientation of ordered triplet (p, q, r)
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0: return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise
    
    def on_segment(p, q, r):
        # Check if point q lies on line segment pr
        if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
            return True
        return False

    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases (collinear points)
    if o1 == 0 and on_segment(p1, q1, p2): return True
    if o2 == 0 and on_segment(p1, q2, p2): return True
    if o3 == 0 and on_segment(q1, p1, q2): return True
    if o4 == 0 and on_segment(q1, p2, q2): return True

    return False


def optimalizationOfCrossingEdges(tour):  # tour is a list of indices
    n = len(tour)
    for i in range(n - 1):
        for j in range(i + 2, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if edges_cross(Verticies[tour[i]], Verticies[tour[i + 1]], Verticies[tour[j]], Verticies[tour[(j + 1) % n]]):
                tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
    return tour



def display_solution(canvas, tour): 
    canvas.delete("all")  # Clear the canvas

    for i in range(len(tour)):
        current_vertex_idx = tour[i]
        next_vertex_idx = tour[(i + 1) % len(tour)]  # Wrap around to the starting city

        # Get the coordinates of the current and next cities from Verticies
        current_vertex = Verticies[current_vertex_idx]
        next_vertex = Verticies[next_vertex_idx]

        canvas.create_line(
            (current_vertex[0] + radius / 2) * constant,
            (current_vertex[1] + radius / 2) * constant,
            (next_vertex[0] + radius / 2) * constant,
            (next_vertex[1] + radius / 2) * constant
        )

    # Draw vertices
    for idx in tour:
        vertex = Verticies[idx]
        canvas.create_oval(
            vertex[0] * constant, vertex[1] * constant,
            (vertex[0] + radius) * constant, (vertex[1] + radius) * constant,
            fill="red"
        )

    canvas.update()  # Update the canvas to show changes



def simulated_annealing(canvas,vertices):  # canvas,
    current_solution = list(range(len(vertices)))  # Use indices
    random.shuffle(current_solution)  # Shuffle to get a random initial solution
    current_length = total_path_length(current_solution)
    best_solution = current_solution[:]
    best_length = current_length
    temperature = initial_temperature
    iteration = 0

    while temperature > lowPoint:
        iteration += 1
        # Create a new solution by swapping two vertices randomly
        new_solution = current_solution[:]
        i, j = random.sample(range(len(new_solution)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        # Calculate the delta change in path length
        delta_length = delta_path_length(current_solution, i, j)
        new_length = current_length + delta_length

        # Accept new solution based on probability
        if new_length < current_length or exp((current_length - new_length) / temperature) > random.random():
            current_solution = new_solution[:]
            current_length = new_length

        # optimization to remove crossings (optional)
        current_solution = optimalizationOfCrossingEdges(current_solution)
        current_length = total_path_length(current_solution)

        # Update the best solution found so far
        if current_length < best_length:
            best_solution = current_solution[:]
            best_length = current_length
        
        # Cool down the temperature
        temperature *= cooling_rate
        
        # Optionally, update the canvas if you want to visualize every few iterations
        if iteration % displayIteration == 0:
            display_solution(canvas, current_solution)
    
    return best_length, best_solution

# ----------------------------------uncomment this to run----------------------------------
# Display
root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=250 * constant, width=250 * constant, background="#e9f7f7")  # graph
canvas.pack(side=tkinter.LEFT)

# Run simulated annealing and measure execution time
start = time.time()
outSA, best_solution = simulated_annealing(canvas,Verticies) #canvas, 
end = time.time()

# Print the results
print(f" length: {outSA},time: {end - start} seconds")
print(f" best solution: {best_solution}")

# Display final solution
display_solution(canvas,best_solution)

root.mainloop()
