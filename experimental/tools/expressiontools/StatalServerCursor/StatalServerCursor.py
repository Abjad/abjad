from abjad.tools.abctools import AbjadObject


class StatalServerCursor(AbjadObject):
    '''Statal server cursor.
    '''

    ### INITIALIZER ###

    def __init__(self, statal_server=None, position=None, reverse=False):
        from experimental.tools import expressiontools
        assert isinstance(statal_server, expressiontools.StatalServer), repr(statal_server)
        assert isinstance(position, (tuple, type(None))), repr(position)
        assert isinstance(reverse, type(True)), repr(reverse)
        #position = position or (0, )
        position = position or ()
        self._statal_server = statal_server
        self._position = position
        self._reverse = reverse

    ### SPECIAL METHODS ###

    def __call__(self, n=1, level=-1):
        '''Get manifest payload of next `n` nodes at `level`.

        Return list of arbitrary values.
        '''
        return self._get_manifest_payload_of_next_n_nodes_at_level(n, level=level)

    def __eq__(self, expr):
        '''True `expr` is a statal server cursor and keyword argument values are equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            return self._keyword_argument_values == expr._keyword_argument_values
        return False

    ### PRIVATE METHODS ###

    def _get_manifest_payload_of_next_n_nodes_at_level(self, n=1, level=-1):
        result = []
        current_node = self.statal_server.cyclic_tree.get_node_at_position(self.position)
        if self.reverse:
            n *= -1
        nodes = current_node.get_next_n_nodes_at_level(n, level)
        position = nodes[-1].position
        self._position = position
        for node in nodes:
            result.extend(node.manifest_payload)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def position(self):
        '''Statal server cursor position.
        
        Return tuple.
        '''
        return self._position

    @property
    def reverse(self):
        '''Statal server cursor reverse.

        False when cursor reads from left to right.
        True when cursor reads from right to left.

        Return boolean.
        '''
        return self._reverse

    @property   
    def statal_server(self):
        '''Statal server cursor statal server.

        Return statal server.
        '''
        return self._statal_server
