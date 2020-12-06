from buddy.study.viz import MyDigraph

graph = MyDigraph('kmerMonotone')

graph.node('kmers')
graph.node('result')

graph.channel('worker', 'kmer_stream')
graph.channel('kmer_stream', 'kmers')
graph.edge('kmers', 'result', color='red')

graph.write()