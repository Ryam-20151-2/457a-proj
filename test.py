import main
import ant_colony

head, nodes = main.create()
crawl = ant_colony.ant_colony(head, nodes)
crawl.concatenate()
print(crawl)
print(crawl.evaluate_crawl())

pass