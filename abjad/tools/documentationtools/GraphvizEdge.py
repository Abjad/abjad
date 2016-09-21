# -*- coding: utf-8 -*-
from abjad.tools.documentationtools.GraphvizMixin import GraphvizMixin


class GraphvizEdge(GraphvizMixin):
    r'''A Graphviz edge.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_attributes',
        '_head',
        '_head_port_position',
        '_is_directed',
        '_tail',
        '_tail_port_position',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        ):
        GraphvizMixin.__init__(self, attributes=attributes)
        self._head = None
        self._tail = None
        self._is_directed = bool(is_directed)
        self.head_port_position = head_port_position
        self.tail_port_position = tail_port_position

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

    def _get_highest_parent(self):
        from abjad.tools import documentationtools
        highest_parent = None
        if isinstance(self.tail, documentationtools.GraphvizField):
            tail_parentage = list(self.tail.struct.proper_parentage)
        else:
            tail_parentage = list(self.tail.proper_parentage)
        if isinstance(self.head, documentationtools.GraphvizField):
            head_parentage = list(self.head.struct.proper_parentage)
        else:
            head_parentage = list(self.head.proper_parentage)
        while len(tail_parentage) and len(head_parentage) and \
            tail_parentage[-1] is head_parentage[-1]:
            highest_parent = tail_parentage[-1]
            tail_parentage.pop()
            head_parentage.pop()
        if highest_parent is None:
            message = 'highest parent can not be none.'
            raise Exception(message)
        return highest_parent

    ### PUBLIC METHODS ###

    def attach(self, tail, head):
        r'''Attaches edge from `tail` to `head`.
        '''
        from abjad.tools import documentationtools
        prototype = (
            documentationtools.GraphvizSubgraph,
            documentationtools.GraphvizNode,
            documentationtools.GraphvizField,
            )
        assert isinstance(tail, prototype)
        assert isinstance(head, prototype)
        self._disconnect()
        self._connect(tail, head)

    def detach(self):
        r'''Detaches edge.
        '''
        self._disconnect()

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

        Returns true or false.
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
