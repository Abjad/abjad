# -*- coding: utf-8 -*-
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

    def __eq__(self, expr):
        r'''True `expr` is a statal server cursor and keyword
        argument values are equal. Otherwise false.

        Returns true or false.
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
        if not self.statal_server.source._is_valid_level(level):
            message = 'invalid level: {!r}.'.format(level)
            raise Exception(message)
        current_node = self.statal_server.source.get_node_at_position(
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
        r'''Gets position.

        Returns tuple.
        '''
        return self._position

    @property
    def reverse(self):
        r'''Is true when cursor reads from left to right.
        Is false when cursor reads from right to left.

        Returns true or false.
        '''
        return self._reverse

    @property
    def statal_server(self):
        r'''Gets statal server.

        Returns statal server.
        '''
        return self._statal_server

    ### PUBLIC METHODS ###

    def next(self, n=1, level=-1):
        r'''Gets next `n` nodes at `level`.

        ..  container:: example

            **Example 1.** Gets nodes at level -1:

            ::

                >>> sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server.make_cursor()

            ::

                >>> cursor.next()
                [0]
                >>> cursor.next()
                [1]
                >>> cursor.next()
                [2]
                >>> cursor.next()
                [3]
                >>> cursor.next()
                [4]
                >>> cursor.next()
                [5]
                >>> cursor.next()
                [6]
                >>> cursor.next()
                [7]
                >>> cursor.next()
                [0]
                >>> cursor.next()
                [1]

        ..  container:: example

            **Example 2.** Gets nodes at level -2:

            ::

                >>> sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server.make_cursor()

            ::

                >>> cursor.next(level=-2)
                [0, 1]
                >>> cursor.next(level=-2)
                [2, 3]
                >>> cursor.next(level=-2)
                [4, 5]
                >>> cursor.next(level=-2)
                [6, 7]
                >>> cursor.next(level=-2)
                [0, 1]

        ..  container:: example

            **Example 3.** Gets nodes at level -1:

            ::

                >>> sequence = [0]
                >>> server = datastructuretools.StatalServer(sequence)
                >>> cursor = server.make_cursor()

            ::

                >>> cursor.next()
                [0]
                >>> cursor.next()
                [0]
                >>> cursor.next()
                [0]
                >>> cursor.next()
                [0]
                >>> cursor.next()
                [0]

        Returns list.
        '''
        return self._get_manifest_payload_of_next_n_nodes_at_level(
            n,
            level=level,
            )