from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):
    '''Statal server.
    '''

    ### INITIALIZER ###

    def __init__(self, cyclic_tree):
        self._cyclic_tree = sequencetools.CyclicTree(cyclic_tree)

    ### SPECIAL METHODS ###

    def __call__(self, position=None, read_direction=None):
        '''Return statal server cursor.
        '''
        cursor = expressiontools.StatalServerCursor(
            self, position=position, read_direction=read_direction)
        return cursor

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
