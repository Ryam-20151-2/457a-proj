#this class is for a stop, one stop is a node, representing a bar, and the times are when you arrive and leave
class stop:
    def __init__(self, node, s_time: float, e_time: float):
        self.node = node
        self.s_time = s_time # start time
        self.e_time = e_time # end time
    
#a node represents a bar, it has a name, an x-y location, peak fun, peak time, and deviation
class Node:
    def __init__(self, name, x_loc: float,y_loc: float,p_fun:float , p_time:float, t_dev:float):
        self.name = name
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.p_fun = p_fun
        self.p_time = p_time
        self.t_dev = t_dev
        self.weight = 0 # weight is to be used by any heuristic that may want to, we can add more if ya want
        
    def node_print(self): # print everything
        print(" " +self.name)
        print(" " +self.x_loc)
        print(" " +self.y_loc)
        print(" " +self.p_fun)
        print(" " +self.p_time)
        print(" " +self.t_dev)