import random
import csv

with open('ex.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
class Node:
    def __init__(self, name, p_fun, p_time, t_dev):
        self.name = name
        # self.x_loc = x_loc
        # self.y_loc = y_loc
        self.p_fun = p_fun
        self.p_time = p_time
        self.t_dev = t_dev
        self.nodes = [Node]
        self.weight = 0
        
    def node_print(self):
        print(self.name)
    
    def add_nodes(nodes_in):
        nodes = nodes_in
    #a name
    #a 4x1 list of values
    #ant colony pheramone int
    #weighting value
    def create_crawl(self):
        #implement this
        success = 1
        return success #return if it worked or not, 
    
def create():
    nodes = [Node]
    length = 10
    
    with open('ex.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            nodes.append(Node(row[0],row[1],row[2],row[3]))

    nodes[0].node_print()
    #head = nodes[random.randint(0,length)]
    head = Node("what",1,1,1)
    return head


    
def main():
    head = create()
    var = head.create_crawl()
    

        
if __name__ == "__main__":
    main()
    