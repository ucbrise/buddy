

class MyDigraph:

    def __init__(self, name):
        self.name = name
        self.type = 'digraph'
        self.nodes = {}
        self.edges = {}

        self.diamonds = {}
        self.dummy_ids = 0

    def node(self, name):
        assert name not in self.nodes
        d = {
            'shape': 'circle',
        }
        self.nodes[name] = d

    def edge(self, source, sink, color=None):
        self.edges[(source, sink)] = self._stringify_edge(source, sink, color)

    def channel(self, source, sink, color=None):
        self.edges[(source, sink)] = self._stringify_channel(source, sink, color)

    def temporal_edge(self, source, sink, color=None):
        sink, viz = self._stringify_temporal(source, sink, color)
        self.edges[(source, sink)] = viz

    def write(self):
        for name in self.nodes:
            self.nodes[name] = self._stringify_node(name)
        with open('output.gv', 'w') as f:
            f.write(f'{self.type} {self.name} {{\n')
            for node_viz in self.nodes.values():
                f.write(node_viz)
            for diamond_viz in self.diamonds.values():
                f.write(diamond_viz)
            for edge_viz in self.edges.values():
                f.write(edge_viz)
            f.write('}\n')

    def _promote_node(self, name):
        # Elevate node from circle to doublecircle
        assert name in self.nodes
        self.nodes[name]['shape'] = 'doublecircle'
        promoted_name = f"{name}'"
        d = {
            'shape': 'doublecircle'
        }
        self.nodes[promoted_name] = d
        return promoted_name

    def _gen_dummy(self):
        dummy_node = f'dummy{self.dummy_ids}'
        self.dummy_ids += 1
        return dummy_node

    def _stringify_node(self, name):
        return f'{name} [shape={self.nodes[name]["shape"]}];\n'

    def _stringify_dummy(self):
        dummy = self._gen_dummy()
        assert dummy not in self.diamonds
        self.diamonds[dummy] = f'{dummy} [shape=diamond,style=filled,label='',height=.1,width=.1];\n'
        return dummy

    def _stringify_edge(self, source, sink, color=None):
        if color is None:
            return f'{source} -> {sink};\n'
        else:
            return f'{source} -> {sink} [color={color}];\n'

    def _stringify_channel(self, source, sink, color=None):
        dummy_node = self._stringify_dummy()
        if color is None:
            return f'{dummy_node} -> {sink} [style=dotted,label={source}];\n'
        else:
            return f'{dummy_node} -> {sink} [color={color},style=dotted,label={source}];\n'

    def _stringify_temporal(self, source, sink, color=None):
        sink = self._promote_node(sink)
        return sink, self._stringify_edge(source, sink, color)
