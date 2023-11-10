

#this class is for a stop, one stop is a node, representing a bar, and the times are when you arrive and leave
class stop:
    def __init__(self, node, s_time: float, e_time: float):
        self.node = node
        self.s_time = s_time # start time
        self.e_time = e_time # end time
    
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
        

       

        