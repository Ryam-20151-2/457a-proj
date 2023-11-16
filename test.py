import main
import classes

head, nodes = main.create()
crawl = main.create_crawl(head, nodes)

node = crawl.generate_new_node(nodes)
stop = classes.stop(node)

print(crawl)

crawl.insert(0, stop)

print(crawl)
crawl.remove(stop)


print(crawl)

pass