import classes
import crawl_class

import random
import numpy as np

def normalize_2d(matrix):
    r, c = np.shape(matrix)
    c_sum = np.sum(matrix, axis=0) # list of each column's summed elements
    for i in range(0, c):
        for j in range(0, r):
            matrix[j][i] /= c_sum[i]
    return matrix

def choose_row(vector, prob):
    for i in range(0, len(vector)): 
        if (prob <= vector[i]):
            return i
        else:
            prob -= vector[i]
    return -1

def ant_colony(head, nodes, num_iter=100, ants_per_iter=50):
    hours = 8 # length of crawl in hours
    gamma = 500 # hyperparameter

    # creating a 2D array to hold the phermones with the bars and the times, initally zero
    phermones = np.ones((len(nodes), hours))
    # change first column to be zeros EXCEPT at the head
    for bar in nodes:
        if (bar != head): 
            phermones[nodes.index(bar), 0] = 0
    
    phermones = normalize_2d(phermones)

    # initalize optimized values
    best_crawl = crawl_class.Crawl([])
    best_payoff= 0
    total_payoff= 0

    for k in range(0, num_iter):
        crawl_list = [] # list of crawl objects that all the ants go to (each ant does 1 crawl each - comparing the ant's crawls)
        crawl_list_eval = [] # list of crawl object payoffs from each ant's crawl
        for i in range(0, ants_per_iter):
            crawl_list.append(crawl_class.Crawl([])) # initalizing empty crawl per ant
        
        stop_index = []
        for ant in crawl_list:
            stop_index_ant = [] # list of all the stops that the ant goes to the crawl as indicies refering to the order of nodes
            
            for c in range(0, hours):
                r_num = random.random()   # probability for ant to visit a bar (between 0 and 1)
                row = phermones[:, c] # all the element in column number 'c'
                index = choose_row(vector=row, prob=r_num) # index of the node (i.e. bar) we want to go to
                stop_index_ant.append(index)
                node = nodes[index] # node object the ant is going to

                stop = classes.stop(node=node, s_time=(c*60), e_time=((c+1)*60)) # convert to minutes
                ant.append(stop=stop)

            # evaluate the ant's path to calculate payoff
            ant.concatenate()
            crawl_list_eval.append(ant.evaluate_crawl())
            stop_index.append(stop_index_ant) # keeps track of the nodes the ants visited (to avoid updating nodes that ants didn't go to)

        maxVal = max(crawl_list_eval) # max payoff
        minVal = min(crawl_list_eval) # min payoff
        maxIndex = crawl_list_eval.index(maxVal) # getting the index of the max payoff

        if maxVal > best_payoff: # updating the best
            best_crawl = crawl_list[maxIndex]
            best_payoff = maxVal

        avgPayoff = sum(crawl_list_eval) / len(crawl_list_eval)
        delta_payoff = maxVal - minVal
        if delta_payoff == 0: # avoid diving by zero in first iteration
            delta_payoff = 0.1

        # updating phermones
        for i in range(0, len(crawl_list_eval)):
            benefit = (crawl_list_eval[i] - avgPayoff) / delta_payoff

            for j in range(0, len(stop_index[i])):
                phermones[stop_index[i][j], j] += benefit/gamma
                
        # normalize the phermones in the bar
        phermones = normalize_2d(phermones)

    return best_crawl.copy()