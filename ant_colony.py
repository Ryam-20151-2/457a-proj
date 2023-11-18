import classes
import crawl_class

import random
import numpy as np

def normalize_2d(matrix):
    r, c = np.shape(matrix)
    for i in range(0, c):
        sum = np.sum(matrix[:, i])
        for j in range(0, r):
            matrix[j, i] /= sum

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

    # initalize optimized values
    best_crawl = crawl_class.Crawl([])
    best_payoff= 0
    total_payoff= 0


    phermones = normalize_2d(phermones)

    pass

    for k in range(0, num_iter):

        crawl_list = []
        crawl_list_eval = []
        for i in range(0, ants_per_iter):
            crawl_list.append(crawl_class.Crawl([]))
        
        stop_index = []
        for ant in crawl_list:

            r_num = random.random()   # probability for ant to visit a bar
            stop_index_ant = []
            
            for c in range(hours):
                #random.shuffle(nodes) # randomly iterate through bars so the first bar isnt always chosen first

                row = phermones[:, c]
                index = choose_row(vector=row, prob=r_num)
                stop_index_ant.append(index)
                node = nodes[index]

                stop = classes.stop(node=node, s_time=(c*60), e_time=((c+1)*60))
                ant.append(stop=stop)

                # for bar in range(len(nodes)): 
                #     limit = phermones[bar][c]   # chance of visiting the bar is based on the phermones
                #     if (probability < limit):   # if probability is less than the limit, go to the bar
                #         bar_chosen = bar
                #         time_chosen = c
                #         break
                #     else:
                #         probability -= limit   # increase the probability of going to a bar if the bar limit is too high

                # add bar stop to the path the ant is on
                # if (ant_crawl.stops == []):
                #     prev_stop_endtime = 0
                # else:
                #     prev_stop_endtime = ant_crawl.stops[-1].e_time
                # ant_crawl.append(classes.stop(nodes[bar_chosen], (prev_stop_endtime)//60, (prev_stop_endtime//60)+time_chosen))
            
            # evaluate the ant's path to calculate payoff
            ant.concatenate()
            crawl_list_eval.append(ant.evaluate_crawl())
            stop_index.append(stop_index_ant)

        maxVal = max(crawl_list_eval)
        minVal = min(crawl_list_eval)
        maxIndex = crawl_list_eval.index(maxVal)

        if maxVal > best_payoff:
            best_crawl = crawl_list[maxIndex]
            best_payoff = maxVal

        avgPayoff = sum(crawl_list_eval) / len(crawl_list_eval)
        delta_payoff = maxVal - minVal
        if delta_payoff == 0:
            delta_payoff = 0.1

        # updating phermones
        for i in range(0, len(crawl_list_eval)):
            benefit = (crawl_list_eval[i] - avgPayoff) / delta_payoff

            for j in range(0, len(stop_index[i])):
                phermones[stop_index[i][j], j] += benefit/gamma
                
        # normalize the phermones in the bar
        phermones = normalize_2d(phermones)

    return best_crawl.copy()