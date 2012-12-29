from abjad.tools.datastructuretools import TreeNode
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizNode(TreeNode, GraphvizObject):

    ### INITIALIZER ###

    def __init__(self, attributes=None, name=None):
        TreeNode.__init__(self, name=name)
        GraphvizObject.__init__(self, attributes=attributes)
        self._edges = set([])

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        node_def = '"{}"'.format(self.canonical_name)
        if len(self.attributes):
            result = []
            result.extend(self._format_attribute_list(self.attributes))
            result[0] = '{} {}'.format(node_def, result[0])
            return result
        return [node_def + ';']

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        if self.name is not None:
            return self.name
        return 'node_' + '_'.join(str(x) for x in self.graph_order)

    @property
    def edges(self):
        return tuple(self._edges) 

