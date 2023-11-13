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
    phermones = np.ones((len(nodes), hours))
    # change first column to be zeros EXCEPT at the head
    for i in range(len(nodes)):
        if (i != csv.index(head)):  # TODO: why the fuck is this index not working
            phermones[i][0] = 0
    
    # initalize optimized values
    best_crawl = crawl_class.Crawl([])
    best_payoff= 0

    while(t<100): # until convergence...
        for ant in range(len(n)):
            ant_crawl = crawl_class.Crawl([]) # initialize an empty crawl per ant
            probability = random.random()   # probability for ant to visit a bar
            for t in range(hours):
                for bar in range(len(nodes)):
                    limit = phermones[bar][t]   # chance of visiting the bar is based on the phermones
                    if (probability < limit):   # if probability is less than the limit, go to the bar
                        bar_chosen = phermones[bar][t] 
                        break
                    else:
                        probability -= limit   # increase the probability of going to a bar if the bar limit is too high

                # add bar stop to the path the ant is on
                ant_crawl.append(bar_chosen)
            
            # evaluate the ant's path to calculate payoff
            number = ant_crawl.evaluate_crawl   # TODO: does this number mean our payoff per path??
            concat_crawl = ant_crawl # TODO: concatenate the crawl

            # check the best crawl so far and update accordingly
            if (number > best_payoff):
                best_payoff = number
                best_crawl = concat_crawl
            
            # updating phermones
            # TODO: too much brain rn but have todo a for for the bars visited
            # then add the payoff/hyperparameter to the phermone for that bar

            # normalize the phermones in the bar
            phermones = np.norm(phermones)

    return best_crawl

                    