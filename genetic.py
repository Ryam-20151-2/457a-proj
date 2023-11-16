import random
import copy

import classes
import crawl_class

def create_crawl_genetic(head: classes.Node, nodes: list[classes.Node], num_generations: int=100, num_parents: int=20, child_per_parent: int=4) -> list[classes.stop]:

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

            crawl_list.append(parent)
            crawl_list_eval.append(parent.evaluate_crawl())

            for j in range(0, child_per_parent):
                child = copy.deepcopy(parent)
                mutate_crawl(child, nodes=nodes)
                crawl_list.append(child)
                crawl_list_eval.append(child.evaluate_crawl())


        #sorts crawl list according to evaluated score        

        crawl_list_eval_sorted, crawl_list_sorted = list(zip(*sorted(zip(crawl_list_eval, crawl_list), reverse=True)))

        pass

        # zipped_list.sort(reverse=True)

        # crawl_list_eval = [x for x,y in zipped_list]
        # crawl_list = [y for x,y in zipped_list]

        #take top (num_parents) as parents of next generation
        #save best parent in each iteration to see progress

        parent_list = []
        count = 0
        while count < num_parents:
            parent_list.append(crawl_list_sorted[count])
            count += 1



    
    #take last element of best parent in order to find global best
    #since top sets are carried over as parents into the next gen, top set will be carried through the whole algorithm

    return parent_list[0]


def mutate_crawl(crawl: crawl_class.Crawl, nodes: list[classes.Node], prob_add: float=0.02, prob_remove: float=0.02, prob_swap_out: float=0.05, 
                 prob_swap_spots: float=0.02, prob_shift_time: float=1.0) -> list[classes.stop]:

    prob = random.random()
    if (prob < prob_add):
        return mutate_crawl(crawl=mutation_add(crawl, nodes=nodes), nodes=nodes, prob_add=(prob_add/2), prob_remove=prob_remove, 
                            prob_swap_out=prob_swap_out, prob_swap_spots=prob_swap_spots, prob_shift_time=prob_shift_time)
    
    prob = random.random()
    if (prob < prob_remove):
        return mutate_crawl(crawl=mutation_remove(crawl), nodes=nodes, prob_add=prob_add, prob_remove=(prob_remove/2), 
                            prob_swap_out=prob_swap_out, prob_swap_spots=prob_swap_spots, prob_shift_time=prob_shift_time)
    
    prob = random.random()
    if (prob < prob_swap_out):
        return mutate_crawl(crawl=mutation_swap_out(crawl, nodes=nodes), nodes=nodes, prob_add=prob_add, prob_remove=prob_remove, 
                            prob_swap_out=(prob_swap_out/2), prob_swap_spots=prob_swap_spots, prob_shift_time=prob_shift_time)
    
    prob = random.random()
    if (prob < prob_swap_spots):
        return mutate_crawl(crawl=mutation_swap_spots(crawl), nodes=nodes, prob_add=prob_add, prob_remove=prob_remove, 
                            prob_swap_out=prob_swap_out, prob_swap_spots=(prob_swap_spots/2), prob_shift_time=prob_shift_time)
    
    prob = random.random()
    if (prob < prob_shift_time):
        return mutate_crawl(crawl=mutation_shift_time(crawl), nodes=nodes, prob_add=prob_add, prob_remove=prob_remove, 
                            prob_swap_out=prob_swap_out, prob_swap_spots=prob_swap_spots, prob_shift_time=(prob_shift_time/2))
    
    return crawl

def mutation_add(crawl: crawl_class.Crawl, nodes: list[classes.Node]) -> crawl_class.Crawl:

    node = crawl.generate_new_node(nodes=nodes)
    num_stops = crawl.length()

    if (num_stops > 8):
        return crawl

    insert_location = random.randint(0, num_stops)
    crawl.insert(insert_location, classes.stop(node))
    crawl.balance_times()

    return crawl

def mutation_remove(crawl: crawl_class.Crawl) -> crawl_class.Crawl:

    num_stops = crawl.length()
    if (num_stops <= 2):
        return crawl

    delete_location = random.randint(0, num_stops - 1)
    crawl.remove(crawl[delete_location])

    return crawl

def mutation_swap_out(crawl: crawl_class.Crawl, nodes: list[classes.Node]) -> crawl_class.Crawl:

    num_stops = crawl.length()

    node = crawl.generate_new_node(nodes=nodes)
    swap_location = random.randint(0, num_stops - 1)

    crawl[swap_location].node = node

    return crawl

def mutation_swap_spots(crawl: crawl_class.Crawl) -> crawl_class.Crawl:

    num_stops = crawl.length()

    swap_location_one = random.randint(0, num_stops - 1)
    swap_location_two = random.randint(0, num_stops - 1)

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
        if (crawl[shift_location - 1].e_time < crawl[shift_location - 1].s_time):
            crawl[shift_location - 1].e_time = crawl[shift_location - 1].s_time
        crawl[shift_location].s_time = crawl[shift_location - 1].e_time

    elif (shift_duration > 0):

        crawl[shift_location].s_time += shift_duration
        if (crawl[shift_location].s_time > crawl[shift_location].e_time):
            crawl[shift_location].s_time = crawl[shift_location].e_time
        crawl[shift_location - 1].e_time = crawl[shift_location].s_time

    return crawl
