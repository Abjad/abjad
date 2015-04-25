# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):
    r'''A statal server.
    '''

    ### INITIALIZER ###

    def __init__(self, cyclic_tree=None):
        from abjad.tools import datastructuretools
        self._cyclic_tree = datastructuretools.CyclicPayloadTree(cyclic_tree)

    ### SPECIAL METHODS ###

    def __call__(self, position=None, reverse=False):
        r'''Calls statal server.

        Returns statal server cursor.
        '''
        from abjad.tools import datastructuretools
        if isinstance(position, int):
            position = (position,)
        cursor = datastructuretools.StatalServerCursor(
            statal_server=self,
            position=position,
            reverse=reverse,
            )
        return cursor

    def __eq__(self, expr):
        r'''Is true when `expr` is a statal server with cyclic tree equal to
        that of this statal server. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.cyclic_tree == expr.cyclic_tree:
                return True
        return False

    def __hash__(self):
        r'''Hashes statal server.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(StatalServer, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic_tree(self):
        r'''Statal server cyclic tree.
        '''
        return self._cyclic_tree

    @property
    def last_node(self):
        r'''Statal server last node.
        '''
        return self.last_nodes[-1]