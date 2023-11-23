
import math
import matplotlib.pyplot as plt
import numpy as np


#this class is for a stop, one stop is a node, representing a bar, and the times are when you arrive and leave
class stop:
    def __init__(self, node, s_time: float=0, e_time: float=0):
        self.node = node
        self.s_time = s_time # start time
        self.e_time = e_time # end time

    #calculatess distance penalty between nodes
    def calc_distance_penalty(self, other):

        return self.node.calc_distance_penalty(other.node)

    def calc_payoff_step(self, time: int):

        return self.node.calc_payoff_step(time)         


    #calculates payoff of a stop
    def calc_payoff(self):

        payoff = 0      #initializes payoff

        #loops through for each time step you are at the bar
        for i in range(self.s_time, self.e_time):           
            payoff += self.calc_payoff_step(i)
        
        #punishes payoff slightly for being too long/small of a stop
        delta = self.e_time - self.s_time
        
        timePun = 0
        if (delta > 150):
            timePun = delta-120
        elif (delta < 90):
            timePun = 90 - delta

        den = 1 + 0.01*timePun
        payoff = payoff / den
        return payoff
    
    def visualize_payoffs(self, t_start=0, t_end=480, show=True):
        
        t, p = self.node.visualize_payoffs(t_start=t_start, t_end=t_end, show=False)
        den = 1 + 0.005*abs(120 - (self.e_time - self.s_time))

        for p_i in p:
            p_i /= den

        p_f = [p_i for t_i, p_i in zip(t, p) if (t_i >= self.s_time and t_i <= self.e_time)]
        t_f = [t_i for t_i in t if (t_i >= self.s_time and t_i <= self.e_time)]

        if show:
            plt.plot(t, p, color="black")
            plt.title(self.node.name)
            plt.xlabel("Time")
            plt.ylabel("Payoff")
            plt.fill_between(y1=p_f, x=t_f, facecolor='green', alpha=.5)
            plt.show()
        return [t_f, p_f]
    
    def visualize_payoffs_cumulative(self, t_start=0, t_end=480, show=True):
        t, p = self.visualize_payoffs(t_start=t_start, t_end=t_end, show=False)

        t_t = []
        p_t = []

        for i in range(0, t_end - t_start + 1):
            t_t.append(i + t_start)
            p_i = 0
            if i in t:
                index = t.index(i)
                p_i = p[index]
            if i == 0:
                p_t.append(p_i)
            else:
                p_t.append(p_t[i-1] + p_i)

        if show:
            plt.plot(t_t, p_t, color="black")
            plt.title(self.node.name)
            plt.xlabel("Time")
            plt.ylabel("Payoff")
            plt.show()
        return [t_t, p_t]
    
#a node represents a bar, it has a name, an x-y location, peak fun, peak time, and deviation
class Node:
    def __init__(self, name, lat: float,longatude: float,p_fun:float , p_time:float, t_dev:float):
        self.name = name
        self.lat = lat
        self.long = longatude
        self.p_fun = p_fun
        self.p_time = p_time
        self.t_dev = t_dev
        self.weight = 0 # weight is to be used by any heuristic that may want to, we can add more if ya want
        
    def node_print(self): # print everything
        print(" " +self.name)
        print(" " +str(self.lat))
        print(" " +str(self.long))
        print(" " +str(self.p_fun))
        print(" " +str(self.p_time))
        print(" " +str(self.t_dev))

    #calculates distance between nodes
    def calc_distance(self, other):

        R = 6371                    #earths rad in km

        #variable priming
        lat1 = self.lat * math.pi/180                 
        lat2 = other.lat * math.pi/180
        
        delta_lat = (self.lat-other.lat) * math.pi/180
        delta_long = (self.long-other.long) * math.pi/180

        a = (math.sin(delta_lat/2) ** 2) + (math.cos(lat1) * math.cos(lat2) * (math.sin(delta_long/2) ** 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c             #distance in km
    
    #calculatess distance penalty between nodes
    def calc_distance_penalty(self, other):

        distance = self.calc_distance(other)

        return 150 * (distance ** 1.2)

    def calc_payoff_step(self, time: int):

        #is a normal distribution with 
        #       peak value p_fun
        #       peak arrival time p_time
        #       standard deviation t_dev

        arg = (time - float(self.p_time)) / float(self.t_dev)     #(t - mu / stdev)
        arg = -0.5 * (arg ** 2)                     #argument to exponential
        return (float(self.p_fun) * math.exp(arg))         


    def visualize_payoffs(self, t_start=0, t_end=480, show=True):

        t = list(range(t_start, t_end+1))
        p = []
        for elem in t:
            p.append(self.calc_payoff_step(time=elem))
        
        if show:
            plt.plot(t, p, color="black")
            plt.title(self.name)
            plt.xlabel("Time")
            plt.ylabel("Payoff")
            plt.show()

        return [t, p]

       

        