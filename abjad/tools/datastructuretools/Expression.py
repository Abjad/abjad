# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class Expression(TypedTuple):
    r'''An expression.

    ..  container:: example

        **Example.**

        ::

            >>> expression = datastructuretools.Expression(
            ...    items=[
            ...        rhythmmakertools.select_every(indices=[0], period=2),
            ...        rhythmmakertools.select_last(3, invert=True),
            ...        ],
            ...    operator='and',
            ...    )

        ::

            >>> print(format(expression))
            datastructuretools.Expression(
                (
                    rhythmmakertools.Pattern(
                        indices=(0,),
                        period=2,
                        ),
                    rhythmmakertools.Pattern(
                        indices=(-3, -2, -1),
                        invert=True,
                        ),
                    ),
                operator='and',
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_operator',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, operator=None):
        TypedTuple.__init__(
            self,
            items=items,
            )
        self._operator = operator

    ### PUBLIC PROPERTIES ###

    @property
    def operator(self):
        r'''Gets operator of expression.

        Set to string.

        Returns string.
        '''
        return self._operator