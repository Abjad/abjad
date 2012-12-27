from abjad.tools.abctools import AbjadObject


class GraphvizEdge(AbjadObject):
    '''A Graphviz edge.'''

    ### INITIALIZER ###

    def __init__(self, attributes=None):
        assert isinstance(attributes, (dict, type(None)))
        if attributes is None:
            self._attributes = {}
        else:
            self._attributes = copy.copy(attributes)
        self._head = None
        self._tail = None

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        from experimental.tools import graphviztools
        if args:
            assert len(args) == 2
            assert all(isinstance(x,
                (graphviztools.GraphvizCluster, graphviztools.GraphvizNode))
                for x in args)
            tail, head = args
            self._disconnect()
            self._connect(tail, head)
        else:
            self._disconnect()
        return self

    ### PRIVATE METHODS ###

    def _connect(self, tail, head):
        tail._edges.add(self)
        head._edges.add(self)
        self._tail = tail
        self._head = head

    def _disconnect(self):
        if self.tail is not None:
            self.tail._edges.remove(self)
        if self.head is not None:
            self.head._edges.remove(self)
        self._tail = None
        self._head = None

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
            return '{} -> {} {};'.format(
                self.tail.name, self.head.name, 
                self._format_attribute_list(self.attributes))
        return '{} -> {};'.format(self.tail.name, self.head.name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

