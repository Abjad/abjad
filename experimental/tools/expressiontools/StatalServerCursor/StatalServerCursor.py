from abjad.tools.abctools import AbjadObject


class StatalServerCursor(AbjadObject):
    '''Statal server cursor.
    '''

    ### INITIALIZER ###

    def __init__(self, statal_server=None, position=None, read_direction=None):
        from experimental.tools import expressiontools
        assert isinstance(statal_server, expressiontools.StatalServer), repr(statal_server)
        assert isinstance(position, (tuple, type(None))), repr(position)
        assert read_direction in (None, Left, Right), repr(read_direction)    
        position = position or (0, )
        read_direction = read_direction or Right
        self._statal_server = statal_server
        self._position = position
        self._read_direction = read_direction

    ### SPECIAL METHODS ###

    def __call__(self, n=1, level=-1):
        '''Aliased to ``self.get_next_n_nodes_at_level()``.

        Return list.
        '''
        return self.get_next_n_nodes_at_level(n, level=level)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def position(self):
        '''Statal server cursor position.
        
        Return tuple.
        '''
        return self._position

    @property
    def read_direction(self):
        '''Statal server cursor read direction.

        Return direction constant.
        '''
        return self._read_direction

    @property   
    def statal_server(self):
        '''Statal server cursor statal server.

        Return statal server.
        '''
        return self._statal_server

    ### PUBLC METHODS ###

    def get_next_n_nodes_at_level(self, n=1, level=-1):
        '''Get next `n` nodes at `level`.

        Return list.
        '''
        nodes = self.statal_server.get_next_n_nodes_at_level(self.position, n, level)
        position = nodes[-1].position
        self._position = position
        return nodes
