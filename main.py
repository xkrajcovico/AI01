import random
import time
from math import sqrt
import tkinter
from geneticAlgorithmFunctions import *
from simulatedAnnealingFunctions import *
from GLOBAL_VARIABLES import*

# Display
root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=250 * constant, width=250 * constant, background="#e9f7f7")#graph
canvas.pack(side=tkinter.LEFT)

graph_canvas = tkinter.Canvas(root, height=250, width=500,background="#e9f7f7")#stats
graph_canvas.pack(side=tkinter.RIGHT)

#------------------------------------------------------------
#---------------    GENETIC ALGORITHM   ---------------------
#------------------------------------------------------------
startGA = time.time()  # Start timer for genetic algorithm
outGA, best_tour= genetic_algorithm(canvas, graph_canvas) #canvas, graph_canvas
endGA = time.time() #end & print the timer
print(f"time: {endGA - startGA} s - distance: {outGA}")
print(f"best solution: {best_tour}")
# print(f"{endGA - startGA}, {outGA}")


# time.sleep(3)
#------------------------------------------------------------
#---------------    STIMULATED ANNEALING   ------------------
#------------------------------------------------------------
startSA = time.time()  # Start timer for genetic algorithm
outSA,best_solution = simulated_annealing(canvas,Verticies) #canvas, 
endSA = time.time() #end & print the timer
print(f"best solution: {best_solution}")
# print(f"time: {endSA - startSA} s - distance: {outSA}")
print(f"{endSA - startSA}, {outSA}")




graph_canvas.delete("all")
root.mainloop()
