import payoffs
import classes

import math
import random

class Crawl:
    def __init__(self, stops: [], start: int=0, end: int=480):
        self.stops = stops
        self.start = start
        self.end = end



    #overloading
    def __getitem__(self, key):
        return self.stops[key]
    
    def __setitem__(self, key, value):
        self.stops[key] = value
        return value
    
    def __delitem__(self, key):
        value = self.stops[key]
        del self.stops[key]
        return value
    
    def __contains__(self, key):
        return (key in self.stops)
    


    #utility array functions
    def append(self, stop: classes.stop):
        self.stops.append(stop)

    def length(self):
        return self.stops.length()
        


    #this will be called to see if a crawl is valid and can be evaluated
    # a valid crawl has more than one stop, it sorted, and has matching times
    def isValid(self):
        if(len(self.stops) < 2):
            return False
    
        last_stop = None
        for x in self.stops:
            if(last_stop != None): 
                if(last_stop.e_time != x.s_time):
                    return False
            last_stop = x
            
        return True
    
    #function for finding if a node is already in a crawl
    def inCrawl(self, node: classes.Node) -> bool:
        
        for stop in self:
            if (stop.node.name == node.name):
                return True

        return False
    


    #this funciton is called to evalute a crawl, pass your list of stops and it will give back a float as your value
    def evaluate_crawl(self):
        val = 0
        prev_stop = self.stops[0]
        for x in self.stops:
            val += payoffs.calc_payoff(x)
            val -= payoffs.calc_distance_penatly(x, prev_stop)
            prev_stop = x
        return val



    #evenly balances times of a crawl throughout the crawl
    def balance_times(self):

        num_stops = self.length()

        for i in range(0, self.length()):
            self[i].s_time = math.floor((i * (self.end-self.start)) / num_stops) + self.start
            self[i].e_time = math.floor(((i+1) * (self.end-self.start)) / num_stops) + self.start
        
        return self
    

    #generates a node that is not already in the crawl
    def generate_new_node(self, nodes: list[classes.Node]) -> classes.Node:
        
        num_nodes = nodes.length()

        #finds bar not already on crawl and adds it to crawl
        node = None
        while (node == None):
            node_num = random.randint(0, num_nodes - 1)
            node = nodes[node_num]
            
            if (self.inCrawl(node)):
                node = None

        return node
    

    #removes all crawl data and creates a new random crawl
    def randomize(self, head: classes.Node, nodes: list[classes.Node]):

        self = Crawl()
        self.append(classes.stop(node=head, s_time=0, e_time=0))        #creates crawl list with the first stop

        num_stops = random.randint(2, 5)    #generates a random number for the stops

        #adds random number of stops to the list
        for i in range(1, num_stops):

            new_node = self.generate_new_node(nodes)
            self.append(classes.stop(nodes[new_node]))

        #sets the start and end times evenly spaced
        self.balance_times()

        return self

    