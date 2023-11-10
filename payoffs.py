import math
import classes 

def calc_distance(stop: classes.stop, prev_stop: classes.stop):

    R = 6371                    #earths rad in km

    #variable priming
    lat1 = stop.node.lat * math.pi/180                 
    lat2 = prev_stop.node.lat * math.pi/180
    
    delta_lat = (stop.node.lat-prev_stop.node.lat) * math.pi/180
    delta_long = (stop.node.long-prev_stop.node.long) * math.pi/180

    a = (math.sin(delta_lat/2) ** 2) + (math.cos(lat1) * math.cos(lat2) * (math.cos(delta_long/2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c             #distance in km

def calc_distance_penatly(stop: classes.stop, prev_stop: classes.stop):

    distance = calc_distance(stop=stop, prev_stop=prev_stop)

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
