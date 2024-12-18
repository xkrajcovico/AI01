import random
# Important variables
CONSTANT = 3
RADIUS = 6
NUMBER_OF_VERTICIES = 20
SLEEP_TIME = 0.1


#gen alg variables
POPULATION_SIZE = 512
MUTATION_RATE = 0.001
MAX_GENERATIONS = 1000
STAGNATION_LIMIT = 7 


# #SA variables
# initial_temperature = 512  # Start with a higher temperature for more exploration
# cooling_rate = 0.9965       # Slower cooling for better convergence
# lowPoint = 0.2
# displayIteration = 100

#SA variables
INITIAL_TEMPERATURE = 1000  # Start with a higher temperature for more exploration
COOLING_RATE = 0.999       # Slower cooling for better convergence
LOW_POINT = 0.2
DISPLAY_ITERATION = 100

def generate_unique_vertices(num_vertices, min_val, max_val):
    vertices = set()
    while len(vertices) < num_vertices:
        x = random.randrange(min_val, max_val)
        y = random.randrange(min_val, max_val)
        vertices.add((x, y))  
    return list(vertices)

verticies = generate_unique_vertices(NUMBER_OF_VERTICIES, 10, 200)
# verticies = [[60, 200],
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