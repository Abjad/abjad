from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizEdge(GraphvizObject):
    '''A Graphviz edge.'''

    ### INITIALIZER ###

    def __init__(self, attributes=None, is_directed=True):
        GraphvizObject.__init__(self, attributes=attributes)
        self._head = None
        self._tail = None
        self._is_directed = bool(is_directed)

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        from abjad.tools import documentationtools
        if args:
            assert len(args) == 2
            assert all(isinstance(x,
                (documentationtools.GraphvizSubgraph, documentationtools.GraphvizNode))
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        connection = '->'
        if not self.is_directed:
            connection = '--'
        edge_def = '{} {} {}'.format(
            self._format_value(self.tail.canonical_name),
            connection,
            self._format_value(self.head.canonical_name))
        if len(self.attributes):
            result = self._format_attribute_list(self.attributes)
            result[0] = '{} {}'.format(edge_def, result[0])
            return result
        return [edge_def + ';']

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_directed():
        def fget(self):
            return self._is_directed
        def fset(self, arg):
            self._is_directed = bool(arg)
        return property(**locals())

