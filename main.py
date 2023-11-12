import random
import csv
import classes
import crawl_class
#imports

# this is a setup funciton, it reads a csv and initializes all the nodes and returns a list and head    
def create():
    nodes = []
    length = 1
    
    with open('ex.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            nodes.append(classes.Node(row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])))

    head = nodes[random.randint(0,length)]
    head.node_print()
    return head, nodes

# this function is call to create a crawl in the form of a list. The list is returned, the list should start with the head
# and each stop should be added in order based on your algorithm
def create_crawl(head, nodes):
    crawl = crawl_class.Crawl([])
    crawl.append(classes.stop(nodes[0],0,120))
    crawl.append(classes.stop(nodes[1],120,240))
    crawl.append(classes.stop(nodes[2],240,360))
    crawl.append(classes.stop(nodes[3],360,480))
    #add more shit based on your code
    #append stops to crawl, return crawl when complete
    #import your file and add your function here
    return crawl
    
# this the main, wild, don't touch it    
def main():
    head, nodes = create()
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
    
