import random
import matplotlib.pyplot as plt
import classes
import crawl_class
import itertools
import copy

##############################################################################################################
############ Local Search Algorithm ##########################################################
##############################################################################################################
def local_search(head: classes.Node, nodes) -> crawl_class.Crawl:
    # all times
    times = [[0,120],[120,240],[240,360],[360,480]]

    #first nodes
    stops = []
    #add head
    stops.append(make_stop(head,times[0]))
    for x in range(len(nodes)):
        stops.append(make_stop(nodes[x], times[x+1]))

    testCrawl = crawl_class.Crawl(stops)
    bestCrawl = testCrawl
    currPayoff = testCrawl.evaluate_crawl()
    bestPayoff = currPayoff
    #get all permutations
    perumuatations = itertools.permutations(nodes)
    #for each permutations, get the best order
    for x in list(perumuatations):
        stops = []
        stops.append(make_stop(head, times[0]))
        
        for y in range(len(x)):
            stops.append(make_stop(x[y], times[y+1]))

        testCrawl = crawl_class.Crawl(stops)
        currPayoff = testCrawl.evaluate_crawl()
        #check if new crawl is better than best crawl
        if(currPayoff > bestPayoff):
            bestPayoff = currPayoff
            bestCrawl = testCrawl

    #adjust times of best crawl

    bestTime = 0
    testCrawl = copy.deepcopy(bestCrawl)
    #adjust times!
    for x in range(len(testCrawl.stops)-1):
        posChange = True
        #if decreasing time is good, keep doing it
        while(posChange):
            adjust_stop_time(testCrawl[x], testCrawl[x+1], -10)
            if(testCrawl.evaluate_crawl() > bestCrawl.evaluate_crawl()):
                bestCrawl = copy.deepcopy(testCrawl)
            else:
                posChange = False
        #if increasing time is good, keep doing it
        while(not(posChange)):
            adjust_stop_time(testCrawl[x], testCrawl[x+1],10)
            if(testCrawl.evaluate_crawl() > bestCrawl.evaluate_crawl()):
                bestCrawl = copy.deepcopy(testCrawl)
            else:
                posChange = True
    #return best crawl found
    return bestCrawl

#adjust some times!
def adjust_stop_time(stop1, stop2, time_shift):
    #make sure we don't go for 0 or negative time
    if(not((stop1.e_time - stop1.s_time) <= 10 or (stop2.e_time - stop2.s_time) <= 10 )):
        stop1.e_time = stop1.e_time+time_shift
        stop2.s_time = stop2.s_time+time_shift

#make a stop!
def make_stop(bar: classes.Node, times: [int]) -> classes.stop:
    return classes.stop(bar, times[0],times[1])

##############################################################################################################
############ Iterative Local Search Algorithm ################################################################
##############################################################################################################
def iterative_local_search(max_itr, head, nodes) -> crawl_class.Crawl:
  
    bestCrawl = crawl_class.Crawl([]).randomize(head, nodes)
    # run for specified amount
    for x in range(0, max_itr):
        nodes2Pass = set()
        #ensure the head isn't added to our list
        nodes2Pass.add(head)

        while(len(nodes2Pass) != 4):
            nodes2Pass.add(nodes[random.randrange(0,len(nodes)-1,1)])

        #remove head from our list
        nodes2Pass.remove(head)
        nodes2Pass = list(nodes2Pass)
        #call local search
        currCrawl = local_search(head,nodes2Pass)
        #check if new crawl is better than old, update if it is
        if(currCrawl.evaluate_crawl() > bestCrawl.evaluate_crawl()):
            bestCrawl = currCrawl
    # return the best crawl
    return bestCrawl

def main_ILS(head, nodes, itr):
    # call iterative search
    return iterative_local_search(itr, head, nodes)

    #do some stuff idk
