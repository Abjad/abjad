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

    def __call__(self, position=None, read_direction=None):
        '''Return statal server cursor.
        '''
        from experimental.tools import expressiontools
        cursor = expressiontools.StatalServerCursor(
            statal_server=self, position=position, read_direction=read_direction)
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

    ### PUBLIC METHODS ###

    def get_next_n_nodes_at_level(self, position, n, level=-1):
        '''Get next `n` nodes at `level` from node at `position`.
        '''
        current_node = self.cyclic_tree.get_node_at_position(position)
        return current_node.get_next_n_nodes_at_level(n, level)
