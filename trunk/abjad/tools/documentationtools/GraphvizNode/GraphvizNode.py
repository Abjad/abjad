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
        if len(self.attributes):
            result = []
            result.extend(self._format_attribute_list(self.attributes))
            result[0] = '"{}" {}'.format(self.name, result[0])
            return result
        return ['"{}";'.format(self.name)]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def edges(self):
        return tuple(self._edges) 

