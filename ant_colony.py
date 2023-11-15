import random
import csv
import classes
import crawl_class
import payoffs
import main
import numpy as np

def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix/norm  # normalized matrix
    return matrix

def ant_colony():
    # initalizing a random head nodes, and all nodes that can be used in the crawl optimization
    head, nodes = main.create()

    t = 0 # iteration for ant colony algorithm
    n = 1000 # number of ants
    hours = 8 # length of crawl in hours
    gamma = 2000 # hyperparameter
    time_elapsed = np.zeros(n) # time elapsed for each ant, initially zero

    # creating a 2D array to hold the phermones with the bars and the times, initally zero
    phermones = np.ones((len(nodes), hours))
    # change first column to be zeros EXCEPT at the head
    for bar in nodes:
        if (bar != head): 
            phermones[nodes.index(bar)][0] = 0

    # initalize optimized values
    best_crawl = crawl_class.Crawl([])
    best_payoff= 0

    while(t<100): # until convergence...
        for ant in range(n):
            ant_crawl = crawl_class.Crawl([]) # initialize an empty crawl per ant
            probability = random.random()   # probability for ant to visit a bar
            for t in range(hours):
                random.shuffle(nodes) # randomly iterate through bars so the first bar isnt always chosen first
                for bar in range(len(nodes)): 
                    limit = phermones[bar][t]   # chance of visiting the bar is based on the phermones
                    if (probability < limit):   # if probability is less than the limit, go to the bar
                        bar_chosen = bar
                        time_chosen = t
                        break
                    else:
                        probability -= limit   # increase the probability of going to a bar if the bar limit is too high

                # add bar stop to the path the ant is on
                if (ant_crawl.stops == []):
                    prev_stop_endtime = 0
                else:
                    prev_stop_endtime = ant_crawl.stops[-1].e_time
                ant_crawl.append(classes.stop(nodes[bar_chosen], (prev_stop_endtime)//60, (prev_stop_endtime//60)+time_chosen))
            
            # evaluate the ant's path to calculate payoff
            crawl_payoff = ant_crawl.evaluate_crawl()  

            # check the best crawl so far and update accordingly
            if (crawl_payoff > best_payoff):
                best_payoff = crawl_payoff
                best_crawl = ant_crawl
            
            # updating phermones
            for stop in ant_crawl.stops:
                    print(stop.node.name)
                    phermones[nodes.index(stop.node)][int((stop.e_time-stop.s_time)/60)] += best_payoff/gamma

            # normalize the phermones in the bar
            phermones = normalize_2d(phermones)

    return best_crawl