import crawl_class
import classes


#narrows bar list to keep only the best bars in the list
def narrowBars(head: classes.Node, nodes: list[classes.Node], nodesAtTime: int=2) -> list[classes.Node]:

    newList = [head]
    crawl = crawl_class.Crawl([])

    for i in range(crawl.start+1, crawl.end + 1):
        bestNodes = bestNodesAtTime(nodes=nodes, time=i, numNodes=nodesAtTime)

        for node in bestNodes:
            if node not in newList:
                newList.append(node)
    
    return newList

#returns the best node at any time t
def bestNodesAtTime(nodes: list[classes.Node], time: int, numNodes: int=1) -> classes.Node:
    
    bestNodes = []
    worstBestNode = None
    worstBestPayoff = float('-inf')

    for node in nodes:
        if (len(bestNodes) < numNodes):
            bestNodes.append(node)
            worstBestNode = findWorstNode(nodes=bestNodes, time=time)
            worstBestPayoff = worstBestNode.calc_payoff_step(time=time)

        elif (node.calc_payoff_step(time=time) > worstBestPayoff):
            bestNodes.append(node)
            bestNodes.remove(worstBestNode)
            worstBestNode = findWorstNode(nodes=bestNodes, time=time)
            worstBestPayoff = worstBestNode.calc_payoff_step(time=time)

    return bestNodes

#finds the worst node in a list at any time t
def findWorstNode(nodes: list[classes.Node], time: int) -> classes.Node:
    
    worstNode = None
    worstPayoff = float('inf')

    for node in nodes:
        if (node.calc_payoff_step(time=time) < worstPayoff):
            worstPayoff = node.calc_payoff_step(time=time)
            worstNode = node

    return worstNode