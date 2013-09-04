# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):
    r'''Statal server.
    '''

    ### INITIALIZER ###

    def __init__(self, cyclic_tree=None):
        assert cyclic_tree is not None, repr(cyclic_tree)
        self._cyclic_tree = datastructuretools.CyclicPayloadTree(cyclic_tree)

    ### SPECIAL METHODS ###

    def __call__(self, position=None, reverse=False):
        r'''Return statal server cursor.
        '''
        from experimental.tools import musicexpressiontools
        cursor = musicexpressiontools.StatalServerCursor(
            statal_server=self,
            position=position,
            reverse=reverse,
            )
        return cursor

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.cyclic_tree == expr.cyclic_tree:
                return True
        return False

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
