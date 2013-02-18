from abjad.tools.abctools import AbjadObject


class StatalServerCursor(AbjadObject):
    '''Statal server cursor.
    '''

    ### INITIALIZER ###

    def __init__(self, statal_server=None, position=None, read_direction=None):
        assert isinstance(statal_server, expressiontools.StatalServer), repr(statal_server)
        assert isinstance(position, (tuple, type(None))), repr(position)
        assert read_direction in (None, Left, Right), repr(read_direction)    
        position = position or (0, )
        read_direction = read_direction or Right
        self._statal_server = statal_server
        self._position = position
        self._read_direction = read_direction

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
