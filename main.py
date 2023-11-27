import random
import csv
import time_function
import classes
import crawl_class
import simulated_annealing
import genetic
import ILS
import ant_colony
#imports

# this is a setup funciton, it reads a csv and initializes all the nodes and returns a list and head    
def create():
    nodes = []
    length = 2
    
    with open('ex.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            nodes.append(classes.Node(row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])))

    head = nodes[random.randint(0,len(nodes)-1)]
    print(head.name)
    return head, nodes

def create_crawl(head, nodes):
    
    timer = time_function.Timer()
    
    timer.start("Simulated Annealing")
    crawl_sa = simulated_annealing.SimulatedAnnealingOptimizer(head=head, nodes=nodes, iterations=1000).simulated_annealing()
    timer.stop("Simulated Annealing")

    timer.start("Iterative Local Search")
    crawl_ILS = ILS.main_ILS(head, nodes,1000)
    timer.stop("Iterative Local Search")

    timer.start("Genetic Algorithm")
    crawl_ga = genetic.create_crawl_genetic(head, nodes)
    timer.stop("Genetic Algorithm")

    timer.start("Ant Colony")
    crawl_ant = ant_colony.ant_colony(head, nodes,200,100)
    timer.stop("Ant Colony")

    best_crawl = crawl_sa
    values = [(crawl_sa.evaluate_crawl(),"Simulated Annealing",crawl_sa),
              (crawl_ILS.evaluate_crawl(),"Iterative Local Search",crawl_ILS),
              (crawl_ga.evaluate_crawl(),"Genetic Algorithm",crawl_ga),
              (crawl_ant.evaluate_crawl(),"Ant Colony",crawl_ant)]
    values.sort()
    for x in values:
        print(x[1]+" has value: " + str(x[0]))
        print(f"{x[1]} took {timer.get_elapsed_time(x[1]):.2f} seconds to run")
        x[2].print_crawl_history()
        print("\n")
    print(values[3][1]+" is best")
    
    best_crawl = values[3][2]
        
    
    #add more shit based on your code
    #append stops to crawl, return crawl when complete
    #import your file and add your function here
    return best_crawl

def compare_crawls(head, nodes, number_of_tests):

    crawl_score_total = {}
    crawl_time_total = {}
    timer = time_function.Timer()
    
    for idx in range(number_of_tests):
        print(f'Run number: {idx+1}')

        timer.start("Simulated Annealing")
        crawl_sa = simulated_annealing.SimulatedAnnealingOptimizer(head=head, nodes=nodes, iterations=1000).simulated_annealing()
        timer.stop("Simulated Annealing")

        timer.start("Iterative Local Search")
        crawl_ILS = ILS.main_ILS(head, nodes,1000)
        timer.stop("Iterative Local Search")

        timer.start("Genetic Algorithm")
        crawl_ga = genetic.create_crawl_genetic(head, nodes)
        timer.stop("Genetic Algorithm")

        timer.start("Ant Colony")
        crawl_ant = ant_colony.ant_colony(head, nodes,200,100)
        timer.stop("Ant Colony")

        values = [(crawl_sa.evaluate_crawl(),"Simulated Annealing"),
            (crawl_ILS.evaluate_crawl(),"Iterative Local Search"),
            (crawl_ga.evaluate_crawl(),"Genetic Algorithm"),
            (crawl_ant.evaluate_crawl(),"Ant Colony")]

        # add score and time to total
        crawl_score_total = {x[1]: crawl_score_total.get(x[1], 0.0) + x[0] for x in values}
        crawl_time_total = {x[1]: crawl_time_total.get(x[1], 0.0) + timer.get_elapsed_time(x[1]) for x in values}
        
    # divide to get average score and compute average time
    crawl_score_total = {k: v / number_of_tests for k, v in crawl_score_total.items()}
    crawl_time_total = {k: v / number_of_tests for k, v in crawl_time_total.items()}
    
    # print crawl name, score, and time
    for name in crawl_score_total.keys():
        print(f"{name}: Average Score: {crawl_score_total[name]:.4f} Average Duration: {crawl_time_total[name]:.4f}")
    
# this the main, wild, don't touch it    
def main():
    batch_crawl = True
    head, nodes = create()

    if (batch_crawl):
        compare_crawls(head=head, nodes=nodes, number_of_tests=5)
        return
    crawl = create_crawl(head, nodes)
    crawl.print_crawl_history()

    if (crawl.isValid):
        val = crawl.evaluate_crawl()
        print(f"your crawl has value {val}")
    else:
        print("your crawl is shit")
    
#also the main                 kinda
if __name__ == "__main__":
    main()
    
