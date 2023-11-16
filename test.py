import main
import genetic
import classes

head, nodes = main.create()
crawl = genetic.create_crawl_genetic(head, nodes)

print(crawl)
print(crawl.evaluate_crawl())

pass