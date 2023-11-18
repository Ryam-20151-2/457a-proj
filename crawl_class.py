import classes

import math
import random
import copy
import matplotlib.pyplot as plt

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
    
    def __str__(self) -> str:

        string = ""
        for stop in self.stops:
            string = string + f"{stop.node.name} from {stop.s_time} to {stop.e_time}\n"

        #print(string)
        return string
    
    def __lt__(self, other):
        return self.evaluate_crawl() < other.evaluate_crawl()

    #utility array functions
    def append(self, stop: classes.stop):
        return self.stops.append(stop)

    def extend(self, stop):
        return self.stops.extend(stop)

    def remove(self, stop: classes.stop):
        return self.stops.remove(stop)
    
    def insert(self, index: int, stop: classes.stop):
        return self.stops.insert(index, stop)

    def length(self):
        return len(self.stops)
        


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
        for stop in self.stops:
            val += stop.calc_payoff()
            val -= stop.calc_distance_penalty(prev_stop)
            prev_stop = stop
        return val



    #evenly balances times of a crawl throughout the crawl
    def balance_times(self):

        num_stops = self.length()

        for i in range(0, num_stops):
            self[i].s_time = math.floor((i * (self.end-self.start)) / num_stops) + self.start
            self[i].e_time = math.floor(((i+1) * (self.end-self.start)) / num_stops) + self.start
        
        return self
    

    #generates a node that is not already in the crawl
    def generate_new_node(self, nodes: list[classes.Node]) -> classes.Node:
        
        num_nodes = len(nodes)

        #finds bar not already on crawl and adds it to crawl
        node = None
        while (node == None):
            node_num = random.randint(0, num_nodes - 1)
            node = nodes[node_num]
            
            if (self.inCrawl(node)):
                node = None

        return node
    
    def concatenate(self):

        for stop in self:
            if (stop.s_time == stop.e_time):
                self.remove(stop)

        i = 0
        while i < self.length() - 1:
            if (self[i].node.name == self[i+1].node.name):
                self[i].e_time = self[i+1].e_time
                self.remove(self[i+1])
            else:
                i += 1
        return self
    

    #removes all crawl data and creates a new random crawl
    def randomize(self, head: classes.Node, nodes: list[classes.Node], num_stops: int = -1):

        self = Crawl([])
        self.append(classes.stop(node=head, s_time=0, e_time=0))        #creates crawl list with the first stop

        # if no required stops, randomly select number
        if num_stops == -1:
            num_stops = random.randint(2, 5)    #generates a random number for the stops
        
        # ensure stop count chosen is within bounds
        else:
            num_stops = max(num_stops,2)
            num_stops = min(num_stops, len(nodes))

        #adds random number of stops to the list
        for i in range(1, num_stops):

            new_node = self.generate_new_node(nodes)
            self.append(classes.stop(new_node,0,0))
        #sets the start and end times evenly spaced
        self.balance_times()

        return self
    
    # deep copy crawl
    def copy(self):
        return copy.deepcopy(self)

    # print crawl history
    def print_crawl_history(self):
        print("Crawl History:")
        for stop in self.stops:
            print(f"{stop.node.name} from {stop.s_time} to {stop.e_time}")

    def visualize_payoffs(self, t_start=0, t_end=480, show=True):
        
        t = []
        p = []
        for stop in self:
            t_s, p_s = stop.visualize_payoffs(t_start=t_start, t_end=t_end, show=False)
            t.extend(t_s)
            p.extend(p_s)

        if show:
            plt.plot(t, p, color="black")
            plt.xlabel("Time")
            plt.ylabel("Payoff")
            plt.show()
        return [t, p]

    def visualize_payoffs_cumulative(self, t_start=0, t_end=480, show=True):
        
        t, p = self.visualize_payoffs(t_start=t_start, t_end=t_end, show=False)

        

        max = len(t) - 1
        i = 0
        while i < max:
            if (t[i] == t[i+1]):
                p[i+1] += p[i]
                del p[i]
                del t[i]
                max -= 1
            i += 1

        stop = 0

        for i in range(1, len(p)):
            p[i] += p[i-1]
            if ((self[stop].e_time == i) and (stop < self.length() - 1)):
                p[i] -= self[stop].calc_distance_penalty(self[stop+1])
                stop += 1

        if show:
            plt.plot(t, p, color="black")
            plt.xlabel("Time")
            plt.ylabel("Payoff")
            plt.show()

        return [t, p]

        