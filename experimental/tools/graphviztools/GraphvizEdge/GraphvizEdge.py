from abjad.tools.abctools import AbjadObject


class GraphvizEdge(AbjadObject):
    '''A Graphviz edge.'''

    ### INITIALIZER ###

    def __init__(self):
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

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _graphviz_format_pieces(self):
        return '{} -> {};'.format(
            self.tail.name,
            self.head.name,
            )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

