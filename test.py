import main
import classes
import crawl_class
import smartsearch

head, nodes = main.create()

crawl = main.create_crawl(head, nodes)
stop = crawl[-1]

pass

crawl = smartsearch.smartSearch(head, nodes)


print(crawl)
print(crawl.evaluate_crawl())

pass