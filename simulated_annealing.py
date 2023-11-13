import random
import sys
import crawl_class
import numpy as np
from scipy.special import logsumexp

class SimulatedAnnealingOptimizer:
    def __init__(self, head, nodes, iterations = 1000, temperature = 3, temperature_decrement_method = 'linear', alpha = 0.1, beta = 0.9, debug = False):
        # initalize parameters
        self.head = head
        self.nodes = nodes
        self.iterations = iterations
        self.best_crawl_fun = float('-inf')
        self.current_crawl_fun = float('-inf')
        self.temperature = temperature
        self.temperature_decrement_method = temperature_decrement_method
        self.alpha = alpha # temp cooling rate
        self.beta = beta # hyper parameter
        self.debug = debug # debug for printing results

    # replace a bar in crawl with one not already in the crawl
    def __find_another_bar(self, stop_idx):
        
        # duplicate current crawl
        crawl_class.Crawl: potential_crawl 
        potential_crawl = self.current_crawl.copy()

        # make a list of all bars currently in the crawl
        node_name_list = [stop.node.name for stop in potential_crawl.stops]

        # make a list of all bars not in the crawl
        nearby_bars = []
        for bar in self.nodes:
            if bar.name not in node_name_list:
                nearby_bars.append(bar)
        
        # select a bar not in the crawl, and replace the bar
        new_bar = random.choice(nearby_bars)
        potential_crawl.stops[stop_idx].node = new_bar

        return potential_crawl
    
    # modify a stop's time in the crawl (both stop end time and next stop start time)
    def __modify_time(self, stop_idx):

        # duplicate current crawl
        crawl_class.Crawl: potential_crawl 
        potential_crawl = self.current_crawl.copy()

        # if last stop, don't modify endtime
        if stop_idx+1 >= potential_crawl.length():
            return potential_crawl
        
        # duration added to stop end, removed from next stop start
        duration_to_change  = random.randint(1, 10) * random.choice([-1, 1])
        potential_crawl.stops[stop_idx].e_time += duration_to_change
        potential_crawl.stops[stop_idx+1].s_time += duration_to_change

        return potential_crawl  

    # checks if modified crawl is better than current or acceptable based on temperature
    def __modify_crawl(self, to_modify, stop_idx):
        
        # updates the potential crawl based on changing bar or time
        if to_modify == "bar":
            potential_crawl = self.__find_another_bar(stop_idx)
        elif to_modify == "time":
            potential_crawl = self.__modify_time(stop_idx)
        else:
            sys.exit('Verify stop/time modify input in Simulated Annealing')

        # evaluate fun of potential crawl
        potentialCrawlFun = potential_crawl.evaluate_crawl() 
        Delta_E = potentialCrawlFun - self.current_crawl_fun 

        # if potential crawl is more fun than current crawl, update current
        if (Delta_E > 0):
            self.current_crawl_fun = potentialCrawlFun
            self.current_crawl = potential_crawl

            # if current crawl is more fun than best crawl, update best
            if self.current_crawl_fun > self.best_crawl_fun:
                self.best_crawl = self.current_crawl.copy()
                self.best_crawl_fun = self.best_crawl.evaluate_crawl()
        else:
            # SIMULATED ANNEALING:

            # check if payoff is within acceptable bounds based on temperature
            u = random.uniform(0, 1)

            # ensure no divide by 0 error
            if self.temperature > 0:

                # using log sum exp trick to prevent overflow, evaluate payoff criteria
                # if potential crawl fun is within acceptable bounds, update current
                log_sum_exp_term = -Delta_E / self.temperature
                if u <= np.exp(logsumexp([0, -log_sum_exp_term])):
                    self.current_crawl_fun = potentialCrawlFun
                    self.current_crawl = potential_crawl

    # wrapper to modify crawl by changing bars
    def swap_stop(self, stop_idx_to_swap):
        self.__modify_crawl("bar",stop_idx_to_swap)
    
    # wrapper to modify crawl by changing times
    def adjust_times(self,stop_idx_to_modify):
        self.__modify_crawl("time",stop_idx_to_modify)

    def simulated_annealing(self):
        
        # initalize crawl
        self.current_crawl = crawl_class.Crawl([]).randomize(head=self.head, nodes=self.nodes)
        self.current_crawl_fun = self.current_crawl.evaluate_crawl()
        self.best_crawl = self.current_crawl.copy()
        self.best_crawl_fun = self.best_crawl.evaluate_crawl()
        number_of_stops = self.current_crawl.length()

        itr = 0

        # debug, will print start conitions
        if self.debug:
            print("Start Current Crawl")
            self.current_crawl.print_crawl_history()
            print(self.current_crawl_fun, "\n")

        # iterate 
        while (itr < self.iterations):

            # for each stop in crawl, modify bar and times
            for stop_idx in range (0,number_of_stops):
                self.swap_stop(stop_idx)
                self.adjust_times(stop_idx)

            itr += 1

            # temperature decrement method
            if self.temperature_decrement_method == 'linear':
                self.temperature = self.temperature - self.alpha  # Linear reduction rule
            elif self.temperature_decrement_method == 'geometric':
                self.temperature = self.temperature * self.alpha  # Geometric reduction rule
            elif self.temperature_decrement_method == 'slow':
                self.temperature = self.temperature / (1 + (self.beta * self.temperature))  # Slow-decrease rule
            else:
                self.temperature = 0

        #  debug, will print end conitions
        if self.debug:
            print("End Current Crawl")
            self.current_crawl.print_crawl_history()
            print(self.current_crawl_fun, "\n")
            
            print("Best Crawl")
            self.best_crawl.print_crawl_history()
            print(self.best_crawl_fun, "\n")

        # return best crawl
        return self.best_crawl
