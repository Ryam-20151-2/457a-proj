import payoffs
import classes

class Crawl:
    def __init__(self, stops: []):
        self.stops = stops
    
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
    
    #this funciton is called to evalute a crawl, pass your list of stops and it will give back a float as your value
    def evaluate_crawl(self):
        val = 0
        prev_stop = self.stops[0]
        for x in self.stops:
            val += payoffs.calc_payoff(x)
            val -= payoffs.calc_distance_penatly(x, prev_stop)
            prev_stop = x
        return val
    
    def append(self, stop: classes.stop):
        self.stops.append(stop)