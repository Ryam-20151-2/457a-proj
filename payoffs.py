import math

def calc_distance_penatly(stop, prev_stop):

    x_delta_sq = (stop.x_loc - prev_stop.x_loc) ** 2
    y_delta_sq = (stop.y_loc - prev_stop.y_loc) ** 2
    distance = (x_delta_sq + y_delta_sq) ** 0.5

    return 20 * (distance ** 1.2)

def calc_payoff(stop):

    payoff = 0      #initializes payoff

    #loops through for each time step you are at the bar
    for i in range(stop.s_time, stop.e_time):           
        payoff += calc_payoff_step(i, stop.node)
    
    #punishes payoff slightly for being too long/small of a stop
    den = 1 + 0.005*abs(120 - (stop.e_time - stop.s_time))
    payoff = payoff / den
    
def calc_payoff_step(time, node):

    #is a normal distribution with 
    #       peak value p_fun
    #       peak arrival time p_time
    #       standard deviation t_dev

    arg = (time - node.p_time) / node.t_dev     #(t - mu / stdev)
    arg = -0.5 * (arg ** 2)                     #argument to exponential
    return (node.p_fun * math.exp(arg))         
