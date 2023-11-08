import random
import csv

with open('ex.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')


class stop:
    def __init__(self, node, s_time, e_time):
        self.node = node
        self.s_time = s_time
        self.e_time = e_time
    
    def evalute():
        payoff = 12
        return payoff
      
class Node:
    def __init__(self, name, x_loc,y_loc,p_fun, p_time, t_dev):
        self.name = name
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.p_fun = p_fun
        self.p_time = p_time
        self.t_dev = t_dev
        self.weight = 0
        
    def node_print(self):
        print(" " +self.name)
        print(" " +self.x_loc)
        print(" " +self.y_loc)
        print(" " +self.p_fun)
        print(" " +self.p_time)
        print(" " +self.t_dev)

    #a name
    #ant colony pheramone int
    #weighting value 
    
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


def create_crawl(head, nodes):
    crawl = []
    crawl.append(stop(head,0,2))
    crawl.append(stop(head,2,3))
    #add more shit based on your code
    return crawl

def payoff(stop):
    #idk JP's payoff math
    val2 = stop
    val = 1 # it isn't
    return val

def evaluate_crawl(crawl):
    val = 0
    for x in crawl:
        val += payoff(x)
    return val
    
def main():
    head, nodes = create()
    crawl = create_crawl(head, nodes)
    val = evaluate_crawl(crawl)
    print("your crawl has value "+ str(val))
    
  
if __name__ == "__main__":
    main()
    