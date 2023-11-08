import math
import classes 

def calc_distance_penatly(stop: classes.stop, prev_stop: classes.stop):

    x_delta_sq = (float(stop.node.x_loc) - float(prev_stop.node.x_loc)) ** 2
    y_delta_sq = (float(stop.node.y_loc) - float(prev_stop.node.y_loc)) ** 2
    distance = (x_delta_sq + y_delta_sq) ** 0.5

    return 20 * (distance ** 1.2)

def calc_payoff(stop: classes.stop):

    payoff = 0      #initializes payoff

    #loops through for each time step you are at the bar
    for i in range(stop.s_time, stop.e_time):           
        payoff += calc_payoff_step(i, stop.node)
    
    #punishes payoff slightly for being too long/small of a stop
    den = 1 + 0.005*abs(120 - (stop.e_time - stop.s_time))
    payoff = payoff / den
    return payoff
    
def calc_payoff_step(time, node: classes.Node):

    #is a normal distribution with 
    #       peak value p_fun
    #       peak arrival time p_time
    #       standard deviation t_dev

    arg = (time - float(node.p_time)) / float(node.t_dev)     #(t - mu / stdev)
    arg = -0.5 * (arg ** 2)                     #argument to exponential
    return (float(node.p_fun) * math.exp(arg))         
