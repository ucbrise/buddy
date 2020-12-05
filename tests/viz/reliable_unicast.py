from buddy.study.viz import MyDigraph

graph = MyDigraph('reliableUnicast')

graph.node('pipe_in')
graph.node('pipe_sent')

graph.edge('pipe_in', 'data_chan')
graph.edge('pipe_sent', 'data_chan', 'red')
graph.temporal_edge('pipe_in', 'pipe_sent')
graph.channel('data_chan', 'ack_chan')
graph.temporal_channel('ack_chan', 'pipe_sent')

graph.write()