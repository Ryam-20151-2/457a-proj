import main
import ant_colony

head, nodes = main.create()
crawl = ant_colony.ant_colony(head, nodes, 1000, 1000)
crawl.concatenate()
print(crawl)
print(crawl.evaluate_crawl())

pass