from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):
    '''Statal server.
    '''

    ### INITIALIZER ###

    def __init__(self, cyclic_tree=None):
        assert cyclic_tree is not None, repr(cyclic_tree)
        self._cyclic_tree = sequencetools.CyclicTree(cyclic_tree)

    ### SPECIAL METHODS ###

    def __call__(self, position=None, reverse=False):
        '''Return statal server cursor.
        '''
        from experimental.tools import expressiontools
        cursor = expressiontools.StatalServerCursor(
            statal_server=self, position=position, reverse=reverse)
        return cursor

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.cyclic_tree == expr.cyclic_tree:
                return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def cyclic_tree(self):
        '''Statal server cyclic tree.
        '''
        return self._cyclic_tree

    @property
    def last_node(self):
        '''Statal server last node.
        '''
        return self.last_nodes[-1]
