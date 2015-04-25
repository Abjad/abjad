# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StatalServerCursor(AbjadObject):
    r'''A statal server cursor.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        statal_server=None,
        position=None,
        reverse=False,
        ):
        from abjad.tools import datastructuretools
        assert isinstance(position, (tuple, type(None))), repr(position)
        assert isinstance(reverse, type(True)), repr(reverse)
        position = position or ()
        self._statal_server = statal_server
        self._position = position
        self._reverse = reverse

    ### SPECIAL METHODS ###

    def __call__(self, n=1, level=-1):
        r'''Gets manifest payload of next `n` nodes at `level`.

        ..  container:: example

            Gets manifest payload of nodes at level -1:

            ::

                >>> sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server()

            ::

                >>> cursor()
                [0]
                >>> cursor()
                [1]
                >>> cursor()
                [2]
                >>> cursor()
                [3]
                >>> cursor()
                [4]
                >>> cursor()
                [5]
                >>> cursor()
                [6]
                >>> cursor()
                [7]
                >>> cursor()
                [0]
                >>> cursor()
                [1]

        ..  container:: example

            Gets manifest payload of nodes at level -2:

            ::

                >>> sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server()

            ::

                >>> cursor(level=-2)
                [0, 1]
                >>> cursor(level=-2)
                [2, 3]
                >>> cursor(level=-2)
                [4, 5]
                >>> cursor(level=-2)
                [6, 7]
                >>> cursor(level=-2)
                [0, 1]

        ..  container:: example

            Gets manifest payload of nodes at level -1 for statal server of
            length 1:

            ::

                >>> sequence = [0]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server()

            ::

                >>> cursor()
                [0]
                >>> cursor()
                [0]
                >>> cursor()
                [0]
                >>> cursor()
                [0]
                >>> cursor()
                [0]

        Returns list of arbitrary values.
        '''
        return self._get_manifest_payload_of_next_n_nodes_at_level(
            n, level=level)

    def __eq__(self, expr):
        r'''True `expr` is a statal server cursor and keyword
        argument values are equal. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes statal server cursor.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(StatalServerCursor, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_manifest_payload_of_next_n_nodes_at_level(self, n=1, level=-1):
        result = []
        #print
        #print repr(self.position), '(position)'
        if not self.statal_server.cyclic_tree._is_valid_level(level):
            message = 'invalid level: {!r}.'.format(level)
            raise Exception(message)
        current_node = self.statal_server.cyclic_tree.get_node_at_position(
            self.position)
        if self.reverse:
            n *= -1
        nodes = current_node.get_next_n_nodes_at_level(n, level)
        position = nodes[-1].position
        self._position = position
        for node in nodes:
            result.extend(node.manifest_payload)
        #print repr(result), '(result)'
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def position(self):
        r'''Statal server cursor position.

        Returns tuple.
        '''
        return self._position

    @property
    def reverse(self):
        r'''Statal server cursor reverse.

        False when cursor reads from left to right.
        Is true when cursor reads from right to left.

        Returns boolean.
        '''
        return self._reverse

    @property
    def statal_server(self):
        r'''Statal server cursor statal server.

        Returns statal server.
        '''
        return self._statal_server