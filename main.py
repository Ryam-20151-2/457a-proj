import random
import csv
import payoffs
import classes
#imports

# this is a setup funciton, it reads a csv and initializes all the nodes and returns a list and head    
def create():
    nodes = []
    length = 1
    
    with open('ex.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            nodes.append(classes.Node(row[0],row[1],row[2],row[3],row[4],row[5]))

    head = nodes[random.randint(0,length)]
    head.node_print()
    return head, nodes

# this function is call to create a crawl in the form of a list. The list is returned, the list should start with the head
# and each stop should be added in order based on your algorithm
def create_crawl(head, nodes):
    crawl = []
    crawl.append(classes.stop(nodes[0],0,120))
    crawl.append(classes.stop(nodes[1],120,240))
    crawl.append(classes.stop(nodes[2],240,360))
    crawl.append(classes.stop(nodes[3],360,480))
    #add more shit based on your code
    #append stops to crawl, return crawl when complete
    #import your file and add your function here
    return crawl

# this is the payoff function, given a stop it returns how good it is
def calc_payoff(stop):
    return payoffs.calc_payoff(stop)

# this is the penalty function for the distance between stops, gives a stop and the previous one a value is taken off of
# the payoff
def calc_distance_penalty(stop, prev_stop):
    return payoffs.calc_distance_penatly(stop, prev_stop)

#this funciton is called to evalute a crawl, pass your list of stops and it will give back a float as your value
def evaluate_crawl(crawl):
    val = 0
    prev_stop = crawl[0]
    for x in crawl:
        val += calc_payoff(x)
        val -= calc_distance_penalty(x, prev_stop)
        prev_stop = x;
    return val

#this will be called to see if a crawl is valid and can be evaluated
# a valid crawl has more than one stop, it sorted, and has matching times
def is_valid(crawl: []):
    if(len(crawl) < 2):
        print("huh")
        return False
    
    last_stop = None
    for x in crawl:
        if(last_stop != None): 
            if(last_stop.e_time != x.s_time):
                return False
        last_stop = x
        
    return True
    
# this the main, wild, don't touch it    
def main():
    head, nodes = create()
    crawl = create_crawl(head, nodes)
    if (is_valid(crawl)):
        val = evaluate_crawl(crawl)
        print("your crawl has value "+ str(val))
    else:
        print("your crawl is shit")
    
#also the main                 kinda
if __name__ == "__main__":
    main()
    