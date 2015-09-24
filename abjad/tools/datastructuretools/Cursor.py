# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Cursor(AbjadObject):
    r'''Cursor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_position',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        position=None,
        ):
        from abjad.tools import datastructuretools
        assert isinstance(position, (int, tuple, type(None))), repr(position)
        position = position or ()
        self._source = source
        self._position = position

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a cursor with keyword
        arguments equal to this cursor. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes cursor.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Cursor, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_manifest_payload_of_next_n_nodes_at_level(self, n=1, level=-1):
        result = []
        if not self.source._is_valid_level(level):
            message = 'invalid level: {!r}.'.format(level)
            raise Exception(message)
        current_node = self.source.get_node_at_position(self.position)
        nodes = current_node.get_next_n_nodes_at_level(n, level)
        position = nodes[-1].position
        self._position = position
        for node in nodes:
            result.extend(node.manifest_payload)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def position(self):
        r'''Gets position.

        Returns tuple.
        '''
        return self._position

    @property
    def source(self):
        r'''Gets source.

        Returns source.
        '''
        return self._source

    ### PUBLIC METHODS ###

    def next(self, n=1, level=-1):
        r'''Gets next `n` nodes at `level`.

        ..  container:: example

            **Example 1.** Gets nodes at level -1:

            ::

                >>> sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
                >>> tree = datastructuretools.CyclicPayloadTree(sequence)
                >>> cursor = datastructuretools.Cursor(source=tree)

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
                >>> tree = datastructuretools.CyclicPayloadTree(sequence)
                >>> cursor = datastructuretools.Cursor(source=tree)

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
                >>> tree = datastructuretools.CyclicPayloadTree(sequence)
                >>> cursor = datastructuretools.Cursor(source=tree)

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