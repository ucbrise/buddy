import datetime
from subprocess import check_call

class MyDigraph:

    def __init__(self, name):
        self._name = name
        self._type = 'digraph'
        self._nodes = {}
        self._edges = {}

        self._diamonds = {}
        self._dummy_ids = 0

    def node(self, name):
        assert name not in self._nodes
        d = {
            'shape': 'circle',
        }
        self._nodes[name] = d

    def edge(self, source, sink, color=None):
        self._edges[(source, sink)] = self._stringify_edge(source, sink, color)

    def channel(self, source, sink, color=None):
        self._edges[(source, sink)] = self._stringify_channel(source, sink, color)

    def temporal_edge(self, source, sink, color=None):
        sink = self._stringify_temporal(sink)
        viz = self._stringify_edge(source, sink, color)
        self._edges[(source, sink)] = viz

    def temporal_channel(self, source, sink, color=None):
        sink = self._stringify_temporal(sink)
        viz = self._stringify_channel(source, sink, color)
        self._edges[(source, sink)] = viz

    def write(self):
        for name in self._nodes:
            self._nodes[name] = self._stringify_node(name)
        for src, snk in self._edges:
            if snk in self._diamonds:
                assert snk not in self._nodes, f'{snk} is a Channel but it was registered as a node'
                self._edges[(src, snk)] = self._edges[(src, snk)].replace(snk, self._diamonds[snk]['dummy'])
        file_path = f'{self._name}_{datetime.datetime.now().isoformat().split(".")[0]}'
        with open(f'{file_path}.gv', 'w') as f:
            f.write(f'{self._type} {self._name} {{\n')
            f.write('size="8,5"\n')
            for node_viz in self._nodes.values():
                f.write(node_viz)
            for diamond in self._diamonds.values():
                f.write(diamond['viz'])
            for edge_viz in self._edges.values():
                f.write(edge_viz)
            f.write('}\n')
        check_call(['dot','-Tpng', f'{file_path}.gv', '-o', f'{file_path}.png'])


    def _promote_node(self, name):
        # Elevate node from circle to doublecircle
        assert name in self._nodes
        self._nodes[name]['shape'] = 'doublecircle'
        promoted_name = f'"{name}+"'
        d = {
            'shape': 'doublecircle'
        }
        self._nodes[promoted_name] = d
        return promoted_name

    def _gen_dummy(self):
        dummy_node = f'dummy{self._dummy_ids}'
        self._dummy_ids += 1
        return dummy_node

    def _stringify_node(self, name):
        return f'{name} [shape={self._nodes[name]["shape"]}];\n'

    def _stringify_dummy(self, alias):
        dummy = self._gen_dummy()
        assert dummy not in self._diamonds
        self._diamonds[alias] = {
                'dummy': dummy,
                'viz': f'{dummy} [shape=diamond,style=filled,label="",height=.1,width=.1];\n'
        }
        return dummy

    def _stringify_edge(self, source, sink, color=None):
        if color is None:
            return f'{source} -> {sink};\n'
        else:
            return f'{source} -> {sink} [color={color}];\n'

    def _stringify_channel(self, source, sink, color=None):
        dummy_node = self._stringify_dummy(source)
        if color is None:
            return f'{dummy_node} -> {sink} [style=dotted,label={source}];\n'
        else:
            return f'{dummy_node} -> {sink} [color={color},style=dotted,label={source}];\n'

    def _stringify_temporal(self, sink):
        sink = self._promote_node(sink)
        return sink
