import random
import csv
#imports

#this class is for a stop, one stop is a node, representing a bar, and the times are when you arrive and leave
class stop:
    def __init__(self, node, s_time, e_time):
        self.node = node
        self.s_time = s_time # start time
        self.e_time = e_time # end time
    
#a node represents a bar, it has a name, an x-y location, peak fun, peak time, and deviation
class Node:
    def __init__(self, name, x_loc,y_loc,p_fun, p_time, t_dev):
        self.name = name
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.p_fun = p_fun
        self.p_time = p_time
        self.t_dev = t_dev
        self.weight = 0 # weight is to be used by any heuristic that may want to, we can add more if ya want
        
    def node_print(self): # print everything
        print(" " +self.name)
        print(" " +self.x_loc)
        print(" " +self.y_loc)
        print(" " +self.p_fun)
        print(" " +self.p_time)
        print(" " +self.t_dev)

# this is a setup funciton, it reads a csv and initializes all the nodes and returns a list and head    
def create():
    nodes = []
    length = 1
    
    with open('ex.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            nodes.append(Node(row[0],row[1],row[2],row[3],row[4],row[5]))

    head = nodes[random.randint(0,length)]
    head.node_print()
    return head, nodes

# this function is call to create a crawl in the form of a list. The list is returned, the list should start with the head
# and each stop should be added in order based on your algorithm
def create_crawl(head, nodes):
    crawl = []
    crawl.append(stop(head,0,1))
    #crawl.append(stop(head,2,3))
    #add more shit based on your code
    #append stops to crawl, return crawl when complete
    #import your file and add your function here
    return crawl

# this is the payoff function, given a stop it returns how good it is
def calc_payoff(stop):
    #idk JP's payoff math
    val = 1 # it isn't
    return val

# this is the penalty function for the distance between stops, gives a stop and the previous one a value is taken off of
# the payoff
def calc_distance_penalty(stop, prev_stop):
    #idk JP's penalty math
    val = 0.5 # it isn't
    return val

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
    