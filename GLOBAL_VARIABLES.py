import random
# Important variables
constant = 3
radius = 6
NumberOfVerticies = 20
SleepTime = 0.1


#gen alg variables
population_size = 512
mutation_rate = 0.001
max_generations = 1000
stagnation_limit = 7 


# #SA variables
# initial_temperature = 512  # Start with a higher temperature for more exploration
# cooling_rate = 0.9965       # Slower cooling for better convergence
# lowPoint = 0.2
# displayIteration = 100

#SA variables
initial_temperature = 1000  # Start with a higher temperature for more exploration
cooling_rate = 0.999       # Slower cooling for better convergence
lowPoint = 0.2
displayIteration = 100

def generate_unique_vertices(num_vertices, min_val, max_val):
    vertices = set()
    while len(vertices) < num_vertices:
        x = random.randrange(min_val, max_val)
        y = random.randrange(min_val, max_val)
        vertices.add((x, y))  
    return list(vertices)

Verticies = generate_unique_vertices(NumberOfVerticies, 10, 200)
# Verticies = [[60, 200],
# [180, 200],
# [100, 180],
# [140, 180],
# [20, 160],
# [80, 160],
# [200, 160],
# [140, 140],
# [40, 120],
# [120, 120],
# [180, 100],
# [60, 80],
# [100, 80],
# [180, 60],
# [20, 40],
# [100, 40],
# [200, 40],
# [20, 20],
# [60, 20],
# [160, 20]]