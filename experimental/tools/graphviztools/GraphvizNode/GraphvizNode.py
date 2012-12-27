from abjad.tools.datastructuretools import TreeNode


class GraphvizNode(TreeNode):

    ### INITIALIZER ###

    def __init__(self, attributes=None, name=None):
        TreeNode.__init__(self, name=name)
        assert isinstance(attributes, (dict, type(None)))
        if attributes is None:
            self._attributes = {}
        else:
            self._attributes = copy.copy(attributes)
        self._edges = set([])

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edges(self):
        return tuple(self._edges) 

