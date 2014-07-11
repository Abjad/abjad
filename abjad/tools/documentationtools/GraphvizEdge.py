# -*- encoding: utf-8 -*-
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizEdge(GraphvizObject):
    r'''A Graphviz edge.
    '''

    ### INITIALIZER ###

    def __init__(self, attributes=None, is_directed=True):
        GraphvizObject.__init__(self, attributes=attributes)
        self._head = None
        self._tail = None
        self._is_directed = bool(is_directed)
        self._head_port_position = None
        self._tail_port_position = None

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        r'''Calls Graphviz edge.

        Returns Graphviz edge.
        '''
        from abjad.tools import documentationtools
        if args:
            assert len(args) == 2
            prototype = (
                documentationtools.GraphvizSubgraph,
                documentationtools.GraphvizNode,
                documentationtools.GraphvizField,
                )
            assert all(isinstance(x, prototype) for x in args)
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

    ### PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        connection = '->'
        if not self.is_directed:
            connection = '--'
        tail_name = self.tail.canonical_name
        if self._tail_port_position is not None:
            tail_name = '{}:{}'.format(tail_name, self._tail_port_position)
        head_name = self.head.canonical_name
        if self._head_port_position is not None:
            head_name = '{}:{}'.format(head_name, self._head_port_position)
        edge_def = '{} {} {}'.format(
            self._format_value(tail_name),
            connection,
            self._format_value(head_name),
            )
        if len(self.attributes):
            result = self._format_attribute_list(self.attributes)
            result[0] = '{} {}'.format(edge_def, result[0])
            return result
        return [edge_def + ';']

    ### PUBLIC PROPERTIES ###

    @property
    def head(self):
        r'''Head of Graphviz edge.
        '''
        return self._head

    @property
    def head_port_position(self):
        r'''Head port position.
        '''
        return self._head_port_position

    @head_port_position.setter
    def head_port_position(self, expr):
        self._head_port_position = expr

    @property
    def is_directed(self):
        r'''Is true when Graphviz edge is directed. Otherwise false.

        Returns boolean.
        '''
        return self._is_directed

    @is_directed.setter
    def is_directed(self, arg):
        self._is_directed = bool(arg)

    @property
    def tail(self):
        r'''Tail of Graphviz edge.
        '''
        return self._tail

    @property
    def tail_port_position(self):
        r'''Tail port position.
        '''
        return self._tail_port_position

    @tail_port_position.setter
    def tail_port_position(self, expr):
        self._tail_port_position = expr

