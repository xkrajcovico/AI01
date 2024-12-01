import time
from math import sqrt
import random
import tkinter
from GLOBAL_VARIABLES import*

def distanceGA(point1, point2):  # Distance between two points
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_fitness(tour):  # Fitness = total distance travelled
    total_distance = 0
    for i in range(len(tour)):
        total_distance += distanceGA(Verticies[tour[i]], Verticies[tour[(i + 1) % len(tour)]])
    return total_distance


def create_random_tour(num_vertices):  # Shuffle among all points and create one without repeating paths through shuffled tuple -> list
    tour = list(range(num_vertices))
    random.shuffle(tour)
    return tour


def initialize_population(pop_size, num_vertices):  # Create n individual paths for gen #0
    return [create_random_tour(num_vertices) for _ in range(pop_size)]


def tournament_selection(population, fitness_scores, k=5):  # Select 5 random individuals from generation, return best one for parent 
    selected = random.sample(list(zip(population, fitness_scores)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]  


def crossover(parent1, parent2):  # Crossover of two parents by random fraction of parent paths
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    child[start:end] = parent1[start:end]
    
    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]
    
    return child


def mutate(tour, mutation_rate):  # Mutate by shuffling lines from path
    for i in range(len(tour)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(tour) - 1)
            tour[i], tour[j] = tour[j], tour[i]
    return tour


def display_tour(canvas, best_tour):  # Create points and lines in tkinter
    canvas.delete("all")
    
    for i in range(len(best_tour)):
        canvas.create_line(
            (Verticies[best_tour[i]][0] + radius / 2) * constant,
            (Verticies[best_tour[i]][1] + radius / 2) * constant,
            (Verticies[best_tour[(i + 1) % len(best_tour)]][0] + radius / 2) * constant,
            (Verticies[best_tour[(i + 1) % len(best_tour)]][1] + radius / 2) * constant
        )

    for nod in Verticies:
        canvas.create_oval(
            nod[0] * constant, nod[1] * constant,
            (nod[0] + radius) * constant, (nod[1] + radius) * constant, fill="red"
        )

    canvas.update()  


def plot_fitness_graph(canvas, fitness_history):#plot a graph for statistics at the end of running the algorithm
    canvas.delete("graph")  
    max_fitness = max(fitness_history)
    min_fitness = min(fitness_history)
    
    width = 400
    height = 200
    graph_height = 125  

    canvas.create_line(50, 25 + graph_height, 50, 25, fill="black")
    canvas.create_line(50, graph_height+25, width+72,  graph_height+25, fill="black")

    for i in range(len(fitness_history)):
        x = (50 + (i / (len(fitness_history) - 1)) * width)
        y = (25 + graph_height - ((fitness_history[i] - min_fitness) / (max_fitness - min_fitness)) * graph_height)
        
        if i > 0:
            prev_x = (50 + ((i - 1) / (len(fitness_history) - 1)) * width)
            prev_y = (25 + graph_height - ((fitness_history[i - 1] - min_fitness) / (max_fitness - min_fitness)) * graph_height)
            canvas.create_line(prev_x, prev_y, x, y, fill="red", width=2)
        
        # canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", tags="graph")
    
    # Adjust the positions of the text
    canvas.create_text(50 + width / 2, 70 + graph_height, text="Generations", fill="black", font=("Arial", 10))
    canvas.create_text(20, 50 + graph_height / 2, text="Fitness", angle=90, fill="black", font=("Arial", 10))



def genetic_algorithm(canvas, graph_canvas): #canvas, graph_canvas                      main genetic algorithm function
    population = initialize_population(population_size, len(Verticies)) #create random tour
    #create local variables
    fitness_history = []  
    best_fitness = float('inf')
    stagnation_count = 0  

    for generation in range(max_generations):#go throug generations
        fitness_scores = [calculate_fitness(tour) for tour in population]
        new_population = []
        
        for _ in range(population_size):#create new population
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
        
        current_best_fitness = min(fitness_scores)#find best individual
        best_tour = population[fitness_scores.index(current_best_fitness)]

        fitness_history.append(current_best_fitness)
        

        if current_best_fitness < best_fitness:#calc stagnation
            best_fitness = current_best_fitness
            stagnation_count = 0  
        else:
            stagnation_count += 1  

        if stagnation_count >= stagnation_limit:#limit stagnation for efficienncy
            # print(f"Stopped early at generation {generation} due to stagnation.")
            break

        display_tour(canvas, best_tour)#display best individual

    plot_fitness_graph(graph_canvas, fitness_history)#if algorithm ends, print stats

    return current_best_fitness, best_tour#return lenght of the best solution

# ----------------------------------uncomment this to run----------------------------------
# Display
root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=250 * constant, width=250 * constant, background="#e9f7f7")#graph
canvas.pack(side=tkinter.LEFT)

graph_canvas = tkinter.Canvas(root, height=250, width=500,background="#e9f7f7")#stats
graph_canvas.pack(side=tkinter.RIGHT)

# Run simulated annealing and measure execution time
startGA = time.time()  # Start timer for genetic algorithm
outGA, best_tour= genetic_algorithm(canvas, graph_canvas) #canvas, graph_canvas
endGA = time.time() #end & print the timer
print(f"time: {endGA - startGA} s - distance: {outGA}")
print(f"best solution: {best_tour}")

root.mainloop()

