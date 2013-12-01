# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TreeNode
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizNode(TreeNode, GraphvizObject):
    r'''A Graphviz node.
    '''

    ### INITIALIZER ###

    def __init__(self, attributes=None, name=None):
        TreeNode.__init__(self, name=name)
        GraphvizObject.__init__(self, attributes=attributes)
        self._edges = set([])

    ### PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        node_def = self._format_value(self.canonical_name)
        if len(self.attributes):
            result = []
            result.extend(self._format_attribute_list(self.attributes))
            result[0] = '{} {}'.format(node_def, result[0])
            return result
        return [node_def + ';']

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        r'''Canonical name of Graphviz node.

        Returns string.
        '''
        if self.name is not None:
            return self.name
        return 'node_' + '_'.join(str(x) for x in self.graph_order)

    @property
    def edges(self):
        r'''Edges of Graphviz node.

        Returns tuple.
        '''
        return tuple(self._edges)
