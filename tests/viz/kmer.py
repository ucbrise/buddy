from buddy.study.viz import MyDigraph

graph = MyDigraph('kmer')

graph.node('addresses')
graph.node('kmers')
graph.node('result')

graph.edge('addresses', 'worker', color='red')
graph.channel('worker', 'chunk')
graph.channel('chunk', 'kmers')
graph.edge('kmers', 'result', color='red')

graph.write()