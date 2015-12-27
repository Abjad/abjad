# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class CallbackStack(TypedList):
    r'''A callback stack.

    ..  container:: example

        **Example 1.** Partitions sequence into thirds and gets last third:

        ::

            >>> ratio = mathtools.Ratio((1, 1, 1))
            >>> index = -1
            >>> callbacks = datastructuretools.CallbackStack(
            ...    items=[
            ...         sequencetools.PartitionByRatioOfLengthsCallback(ratio),
            ...         sequencetools.GetItemCallback(index),
            ...        ],
            ...    )

        ::

            >>> callbacks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            [7, 8, 9]

        ::

            >>> callbacks('text comprises characters.')
            'aracters.'

        ::

            >>> print(format(callbacks))
            datastructuretools.CallbackStack(
                [
                    sequencetools.PartitionByRatioOfLengthsCallback(
                        ratio=mathtools.Ratio((1, 1, 1)),
                        ),
                    sequencetools.GetItemCallback(
                        index=-1,
                        ),
                    ]
                )

    ..  container:: example

        **Example 2.** Partitions sequence into halves and gets first half:

        ::

            >>> ratio = mathtools.Ratio((1, 1))
            >>> index = 0
            >>> callbacks = datastructuretools.CallbackStack(
            ...    items=[
            ...         sequencetools.PartitionByRatioOfLengthsCallback(ratio),
            ...         sequencetools.GetItemCallback(index),
            ...        ],
            ...    )

        ::

            >>> callbacks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            [0, 1, 2, 3, 4]

        ::

            >>> callbacks('text comprises characters.')
            'text comprise'

        ::

            >>> print(format(callbacks))
            datastructuretools.CallbackStack(
                [
                    sequencetools.PartitionByRatioOfLengthsCallback(
                        ratio=mathtools.Ratio((1, 1)),
                        ),
                    sequencetools.GetItemCallback(
                        index=0,
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls callback stack on `expr`.

        Returns arbitrary value.
        '''
        for callback in self:
            expr = callback(expr)
        return expr