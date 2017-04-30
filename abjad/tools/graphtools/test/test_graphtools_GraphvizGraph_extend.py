# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools import graphtools


class TestCase(systemtools.TestCase):

    def test_01(self):
        graph_one = graphtools.GraphvizGraph()
        node_one = graphtools.GraphvizNode()
        node_two = graphtools.GraphvizNode()
        node_one.attach(node_two)
        graph_one.extend([node_one, node_two])
        assert str(graph_one) == self.normalize('''
            digraph G {
                node_0;
                node_1;
                node_0 -> node_1;
            }
            ''')
        graph_two = graphtools.GraphvizGraph()
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
