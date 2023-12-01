import math
import random

import classes
import crawl_class

def create_crawl_genetic(head: classes.Node, nodes: list[classes.Node], num_generations: int=100, num_parents: int=10, child_per_parent: int=8) -> list[classes.stop]:

    #generate random parents given num_parents
    parent_list = []
    for i in range(0, num_parents):
        parent_list.append(crawl_class.Crawl(stops=[]).randomize(head=head, nodes=nodes))

    #begin iteration loop
    for i in range(0, num_generations):

        crawl_list = []             #reset crawl list for new generation
        crawl_list_eval = []

        #add parents and children to crawl list
        for parent in parent_list:

            crawl_list.append(parent.copy())
            crawl_list_eval.append(parent.evaluate_crawl())

            for j in range(0, child_per_parent):
                child = parent.copy()
                mutate_crawl(child, head=head, nodes=nodes)
                crawl_list.append(child.copy())
                crawl_list_eval.append(child.evaluate_crawl())


        #sorts crawl list according to evaluated score        
        crawl_list_eval_sorted, crawl_list_sorted = list(zip(*sorted(zip(crawl_list_eval, crawl_list), reverse=True)))

        parent_list = []
        count = 0
        guaranteed_spot = math.floor(num_parents/4)

        while count < guaranteed_spot:
            parent_list.append(crawl_list_sorted[count].copy())
            count += 1

        exclusion = []
        
        while count < num_parents:
            randNum = random.randint(guaranteed_spot, len(crawl_list_sorted)-1)
            
            while randNum in exclusion:
                randNum = random.randint(guaranteed_spot, len(crawl_list_sorted)-1)
           
            parent_list.append(crawl_list_sorted[randNum].copy())
            count += 1



    
    #take last element of best parent in order to find global best
    #since top sets are carried over as parents into the next gen, top set will be carried through the whole algorithm

    return parent_list[0]


def mutate_crawl(crawl: crawl_class.Crawl, head: classes.Node, nodes: list[classes.Node], prob_major_mutation: float=0.5, prob_shift_time: float=1.0) -> list[classes.stop]:

    prob = random.random()
    if (prob < prob_major_mutation):
        crawl = mutation_major(crawl=crawl, head=head, nodes=nodes)
    
    prob = random.random()
    while (prob < prob_shift_time):
        crawl = mutation_shift_time(crawl=crawl)
        prob_shift_time /= 2
        prob = random.random()
        
    return crawl


def mutation_major(crawl: crawl_class.Crawl, head: classes.Node, nodes: list[classes.Node], prob_add: float=0.2, prob_remove: float=0.2, 
                   prob_swap_out: float=0.2, prob_swap_spots: float=0.2) -> crawl_class.Crawl:

    prob = random.random()
    if (prob < prob_add):
        return mutation_add(crawl, nodes=nodes)
    
    prob -= prob_add
    if (prob < prob_remove):
        return mutation_remove(crawl)
    
    prob -= prob_remove
    if (prob < prob_swap_out):
        return mutation_swap_out(crawl, nodes=nodes)
    
    prob -= prob_swap_out
    if (prob < prob_swap_spots):
        return mutation_swap_spots(crawl)

    return crawl.randomize(head=head, nodes=nodes)

def mutation_add(crawl: crawl_class.Crawl, nodes: list[classes.Node]) -> crawl_class.Crawl:

    node = crawl.generate_new_node(nodes=nodes)
    num_stops = crawl.length()

    if (num_stops > 8):
        return crawl

    insert_location = random.randint(1, num_stops)
    crawl.insert(insert_location, classes.stop(node))
    crawl.balance_times()

    return crawl

def mutation_remove(crawl: crawl_class.Crawl) -> crawl_class.Crawl:

    num_stops = crawl.length()
    if (num_stops <= 2):
        return crawl

    delete_location = random.randint(1, num_stops - 1)
    crawl.remove(crawl[delete_location])

    return crawl

def mutation_swap_out(crawl: crawl_class.Crawl, nodes: list[classes.Node]) -> crawl_class.Crawl:

    num_stops = crawl.length()

    node = crawl.generate_new_node(nodes=nodes)
    swap_location = random.randint(1, num_stops - 1)

    crawl[swap_location].node = node

    return crawl

def mutation_swap_spots(crawl: crawl_class.Crawl) -> crawl_class.Crawl:

    num_stops = crawl.length()

    swap_location_one = random.randint(1, num_stops - 1)
    swap_location_two = random.randint(1, num_stops - 1)

    node_temp = crawl[swap_location_two].node

    crawl[swap_location_two].node = crawl[swap_location_one].node
    crawl[swap_location_one].node = node_temp

    return crawl

def mutation_shift_time(crawl: crawl_class.Crawl) -> crawl_class.Crawl:

    num_stops = crawl.length()

    shift_location = random.randint(1, num_stops - 1)
    shift_duration = random.randint(-20, 20)

    if (shift_duration < 0):

        crawl[shift_location - 1].e_time += shift_duration
        if (crawl[shift_location - 1].e_time <= crawl[shift_location - 1].s_time):
            crawl[shift_location - 1].e_time = crawl[shift_location - 1].s_time + 1
        crawl[shift_location].s_time = crawl[shift_location - 1].e_time

    elif (shift_duration > 0):

        crawl[shift_location].s_time += shift_duration
        if (crawl[shift_location].s_time >= crawl[shift_location].e_time):
            crawl[shift_location].s_time = crawl[shift_location].e_time - 1
        crawl[shift_location - 1].e_time = crawl[shift_location].s_time

    return crawl