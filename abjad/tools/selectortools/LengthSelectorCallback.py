# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class LengthSelectorCallback(AbjadValueObject):
    r'''A length selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        length=1,
        ):
        from abjad.tools import selectortools
        prototype = (
            int,
            selectortools.LengthInequality,
            )
        assert isinstance(length, prototype)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import selectortools
        assert isinstance(expr, tuple), repr(expr)
        inequality = self.length
        if not isinstance(inequality, selectortools.LengthInequality):
            inequality = selectortools.LengthInequality(
                length=inequality,
                operator_string='==',
                )
        result = []
        for subexpr in expr:
            if inequality(subexpr):
                result.append(subexpr)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets length selector callback length.

        Returns length.
        '''
        return self._length
