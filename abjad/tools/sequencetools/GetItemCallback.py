# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class GetItemCallback(AbjadValueObject):
    r'''A get-item callback.

    ..  container:: example

        **Example 1.** Gets item at index ``2``:

        ::

            >>> callback = sequencetools.GetItemCallback(2)
            >>> callback([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
            12

    ..  container:: example

        **Example 2.** Gets item at index ``-2``:

        ::

            >>> callback = sequencetools.GetItemCallback(-2)
            >>> callback([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
            18

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '__callback',
        '_index',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        index=None,
        ):
        self.__callback = self._get_item
        self._index = index

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls callback on `expr`.
        '''
        result = self.__callback(
            expr, 
            index=self.index,
            )
        return result

    ### PRIVATE METHODS ###

    def _get_item(self, expr, index):
        items = list(expr)
        return items[index]

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets index of callback.

        Returns tuple or none.
        '''
        return self._index