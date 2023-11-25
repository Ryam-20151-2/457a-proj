import random
import sys
import crawl_class
import numpy as np
from scipy.special import logsumexp

class SimulatedAnnealingOptimizer:
    def __init__(self, head, nodes, max_stops = 8, iterations = 1000, temperature = 100, temperature_decrement_method = 'slow', alpha = 0.8, beta = 0.2, view_iteration_counter = False):
        # initalize parameters
        self.head = head
        self.nodes = nodes
        self.iterations = iterations
        self.current_crawl = crawl_class.Crawl([]).randomize(head=self.head, nodes=self.nodes, num_stops=max_stops)
        self.current_crawl_fun = self.current_crawl.evaluate_crawl()
        self.best_crawl = self.current_crawl.copy()
        self.best_crawl_fun = self.best_crawl.evaluate_crawl()
        self.number_of_stops = self.current_crawl.length()
        self.temperature_outer = temperature
        self.temperature_local = temperature
        self.temperature_decrement_method = temperature_decrement_method
        self.alpha = alpha # temp cooling rate
        self.beta = beta # hyper parameter
        self.view_counter = view_iteration_counter
        self.innerCounter = 0
        self.iterations_since_last_best = 0
        self.best_changed = False

    def decrement_temperature(self, temperature, method):
        if method == 'linear':
            return temperature - self.alpha
        elif method == 'geometric':
            return temperature * self.alpha
        elif method == 'slow':
            return temperature / (1 + (self.beta * temperature))
        else:
            return 0

    # replace a bar in crawl with one not already in the crawl
    def __find_another_bar(self, stop_idx):
        
        # don't replace first bar
        if stop_idx==0 or stop_idx > self.number_of_stops-1:
            return self.current_crawl

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
        
        # duration added to stop end, removed from next stop start, stay at stop for at least 1 min
        duration_to_change  = random.randint(1, 10) * random.choice([-1, 1])

        # saturate new time to not exceed non-changing stop times
        if (potential_crawl.stops[stop_idx].e_time + duration_to_change < potential_crawl.stops[stop_idx].s_time):
            duration_to_change = potential_crawl.stops[stop_idx].e_time - potential_crawl.stops[stop_idx].s_time
        
        # saturate new time to not exceed non-changing stop times
        if (potential_crawl.stops[stop_idx+1].s_time + duration_to_change > potential_crawl.stops[stop_idx+1].e_time):
            duration_to_change = potential_crawl.stops[stop_idx+1].e_time - potential_crawl.stops[stop_idx+1].s_time

        # if first stop, don't modify starttime
        if stop_idx == 0:
            if potential_crawl.stops[0].e_time + duration_to_change < 1:
                duration_to_change = 1 - potential_crawl.stops[0].e_time
        
        # modify times
        potential_crawl.stops[stop_idx].e_time += duration_to_change
        potential_crawl.stops[stop_idx+1].s_time += duration_to_change

        # if stop end time is equal to stop start time, remove stop
        potential_crawl.concatenate()
        self.number_of_stops = potential_crawl.length()

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
        Delta_E = self.current_crawl_fun - potentialCrawlFun

        # if potential crawl is more fun than current crawl, update current
        if (Delta_E <= 0):
            self.current_crawl_fun = potentialCrawlFun
            self.current_crawl = potential_crawl
                        
            # if current crawl is more fun than best crawl, update best
            if self.current_crawl_fun > self.best_crawl_fun:
                self.best_crawl = self.current_crawl.copy()
                self.best_crawl_fun = self.best_crawl.evaluate_crawl()
                self.best_changed = True

        else:
            # SIMULATED ANNEALING:
            # ensure no divide by 0 error
            if self.temperature_local > 0:

                # check if payoff is within acceptable bounds based on temperature
                u = random.uniform(0, 1)

                # simulate annealing temperature comparison
                log_sum_exp_term = -Delta_E/ self.temperature_local
                if u <= np.exp(log_sum_exp_term):
                    self.current_crawl_fun = potentialCrawlFun
                    self.current_crawl = potential_crawl

    # wrapper to modify crawl by changing bars
    def swap_stop(self, stop_idx_to_swap):
        self.__modify_crawl("bar",stop_idx_to_swap)

    # wrapper to modify crawl by changing times
    def adjust_times(self,stop_idx_to_modify):
        self.__modify_crawl("time",stop_idx_to_modify)

    def local_simulated_annealing(self, max_iterations):

        for _ in range(max_iterations):

            self.innerCounter+=1
            # for each stop in crawl, modify bar and times
            for stop_idx in range (0,self.number_of_stops):
                self.swap_stop(stop_idx)
                self.adjust_times(stop_idx)
           
            if self.best_changed:
                self.iterations_since_last_best = 0
                self.best_changed = False
            else:
                self.iterations_since_last_best += 1

            self.temperature_local = self.decrement_temperature(self.temperature_local, self.temperature_decrement_method)

    def simulated_annealing(self):
        max_temp = 0.75
        outerCounter = 0

        for _ in range(self.iterations):
            outerCounter+=1
            if self.temperature_outer > max_temp:
                # generate a random crawl, and evaluate it
                self.current_crawl = crawl_class.Crawl([]).randomize(head=self.head, nodes=self.nodes, num_stops=self.number_of_stops)
                self.current_crawl_fun = self.current_crawl.evaluate_crawl()
                self.local_simulated_annealing(max(int(self.iterations*0.01),10))
            
            else:
                # do deeper digging on the best one
                self.current_crawl = self.best_crawl.copy()
                self.current_crawl_fun = self.current_crawl.evaluate_crawl()
                self.local_simulated_annealing(max(self.iterations-self.innerCounter, 10))
                break

            self.temperature_outer = self.decrement_temperature(self.temperature_outer, self.temperature_decrement_method)

        if (self.view_counter):
            print(f"SA: Outer (high temp crawl randomize) counter: {outerCounter}, Inner (total) counter: {self.innerCounter}")
            print(f"SA: Iterations since last best: {self.iterations_since_last_best}")
        
        return self.best_crawl
