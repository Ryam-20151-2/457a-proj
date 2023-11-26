import main
import genetic

head, nodes = main.create()
crawl = genetic.create_crawl_genetic(head, nodes)

print(crawl)
print(crawl.evaluate_crawl())

pass