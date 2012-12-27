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

    ### PRIVATE METHODS ###

    def _format_attribute(self, name, value):
        if isinstance(value, str) and ' ' in value:
            return '{}="{}"'.format(name, value)
        return '{}={}'.format(name, value)

    def _format_attribute_list(self, attributes):
        result = []
        for k, v in sorted(attributes.items()):
            result.append(self._format_attribute(k, v))
        return '[{}]'.format(', '.join(result))

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        if len(self.attributes):
            return '{} {};'.format(self.name,
                self._format_attribute_list(self.attributes))
        return '{};'.format(self.name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edges(self):
        return tuple(self._edges) 

