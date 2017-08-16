import abjad


class TestCase(abjad.TestCase):

    def test_01(self):
        graph_one = abjad.graphtools.GraphvizGraph()
        node_one = abjad.graphtools.GraphvizNode()
        node_two = abjad.graphtools.GraphvizNode()
        node_one.attach(node_two)
        graph_one.extend([node_one, node_two])
        assert str(graph_one) == self.normalize('''
            digraph G {
                node_0;
                node_1;
                node_0 -> node_1;
            }
            ''')
        graph_two = abjad.graphtools.GraphvizGraph()
        assert str(graph_two) == self.normalize('''
            digraph G {
            }
            ''')
        graph_two.extend(graph_one)
        assert str(graph_one) == self.normalize('''
            digraph G {
            }
            ''')
        assert str(graph_two) == self.normalize('''
            digraph G {
                node_0;
                node_1;
                node_0 -> node_1;
            }
            ''')
