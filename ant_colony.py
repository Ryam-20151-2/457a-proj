import random
import csv
import classes
import crawl_class
import payoffs
import main
import numpy as np

def ant_colony():
    # initalizing a random head nodes, and all nodes that can be used in the crawl optimization
    head, nodes = main.create()

    t = 0 # iteration for ant colony algorithm
    n = 1000 # number of ants
    hours = 8 # length of crawl in hours
    p = 0.5 # hyperparameter
    time_elapsed = np.zeros(n) # time elapsed for each ant, initially zero

    # creating a 2D array to hold the phermones with the bars and the times, initally zero
    phermones = np.zeros((len(nodes), hours))
    
    # initalize optimized values
    best_crawl = crawl_class.Crawl([])
    best_payoff= 0

    while(t<100): # until convergence...
        for ant in range(len(n)):
            ant_crawl = crawl_class.Crawl([]) # initialize an empty crawl per ant
            while(time_elapsed[ant] < 480): # crawl for each ant ends when the end time is met
                total_path_payoff = ant_crawl.evaluate_crawl()
                best_payoff = best_crawl.evaluate_crawl()
                if t == 0: # for the first iteration
                    bar_index = nodes.index(head) # start at the head node
                    hours_index = 0 # start at time zero
                else: # for all other non-zero iterations
                    print("TODO")
                    hours_index = random.gauss()
                    bar_index = random.guass(phermones[bar_index][0])# TODO: bar_index - pick based off probability
                    # TODO: hours_index - pick based off proabaility???
                phermones[bar_index][hours_index] += total_path_payoff # update phermone trail at the indicies the ant travelled to
                ant_crawl.append(classes.stop(nodes[bar_index],time_start,time_end)) # TODO: update the ant's crawl with the node, and times the ant travelled to
                if total_path_payoff < best_payoff: # update the best cost and path parameters
                    best_payoff = total_path_payoff
                    best_crawl = ant_crawl
                time_elapsed[ant] += time_end - time_start # TODO: update the elapsed time of the ant
        for i in phermones: # for every stop/time combination in the 2D array..
            for j in i:
                j = (1-p)*j # evaporate every pheromones value
        t += 1 # go to the next iteration
    return best_crawl




                    