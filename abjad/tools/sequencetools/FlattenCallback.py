# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class FlattenCallback(AbjadValueObject):
    r'''A flatten callback.

    ..  container:: example

        **Example 1.** Flattens sequence completely:

        ::

            >>> callback = sequencetools.flatten_sequence(None)
            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> callback(sequence)
            [1, 2, 3, 4, 5, 6, 7, 8]

    ..  container:: example

        **Example 2.** Flattens `sequence` to depth ``1``:

        ::

            >>> callback = sequencetools.flatten_sequence(None, depth=1)
            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> callback(sequence)
            [1, 2, 3, [4], 5, 6, 7, [8]]

    ..  container:: example

        **Example 3.** Flattens `sequence` to depth ``2``:

        ::

            >>> callback = sequencetools.flatten_sequence(None, depth=2)
            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> callback(sequence)
            [1, 2, 3, 4, 5, 6, 7, 8]

    ..  container:: example

        **Example 4.** Flattens `sequence` at `indices`:

        ::

            >>> callback = sequencetools.flatten_sequence(None, indices=[3])
            >>> sequence = [0, 1, [2, 3, 4], [5, 6, 7]]
            >>> callback(sequence)
            [0, 1, [2, 3, 4], 5, 6, 7]

    ..  container:: example

        **Example 5.** Flattens `sequence` at negative `indices`:

        ::

            >>> callback = sequencetools.flatten_sequence(None, indices=[-1])
            >>> sequence = [0, 1, [2, 3, 4], [5, 6, 7]]
            >>> callback(sequence)
            [0, 1, [2, 3, 4], 5, 6, 7]

    ..  container:: example

        **Example 6.** Flattens only lists in `sequence`:

        ::

            >>> callback = sequencetools.flatten_sequence(None, classes=(list,))
            >>> sequence = ['ab', 'cd', ['ef', 'gh'], ['ij', 'kl']]
            >>> callback(sequence)
            ['ab', 'cd', 'ef', 'gh', 'ij', 'kl']

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '__callback',
        '_classes',
        '_depth',
        '_indices',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        classes=None,
        depth=-1,
        indices=None,
        ):
        from abjad.tools import sequencetools
        self.__callback = sequencetools.flatten_sequence
        self._classes = classes
        self._depth = depth
        self._indices = indices

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls callback on `expr`.
        '''
        result = self.__callback(
            expr, 
            classes=self.classes,
            depth=self.depth,
            indices=self.indices
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def classes(self):
        r'''Gets classes of callback.

        Returns tuple or none.
        '''
        return self._classes

    @property
    def depth(self):
        r'''Gets depth of callback.

        Returns integer.
        '''
        return self._depth

    @property
    def indices(self):
        r'''Gets indices of callback.

        Returns integers or none.
        '''
        return self._indices