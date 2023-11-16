import crawl_class
import classes
import payoffs

def smartSearch(head: classes.Node, nodes: list[classes.Node]) -> crawl_class.Crawl:

    stop = classes.stop(node=head, s_time=0, e_time=0)
    crawl = crawl_class.Crawl([stop])

    for i in range(crawl.start+1, crawl.end + 1):
        bestNode = bestNodeAtTime(time=i, nodes=nodes)
        print(bestNode.name)
        if ((crawl[-1]).node.name == bestNode.name):
            (crawl[-1]).e_time = i
        else:
            stop = classes.stop(node=bestNode, s_time=i, e_time=i)
            crawl.append(stop)
    
    return crawl

def bestNodeAtTime(nodes: list[classes.Node], time: int) -> classes.Node:
    
    bestNode = None
    bestPayoff = -1

    for node in nodes:
        if (payoffs.calc_payoff_step(time=time, node=node) > bestPayoff):
            bestNode = node
            bestPayoff = payoffs.calc_payoff_step(time=time, node=node)

    return bestNode