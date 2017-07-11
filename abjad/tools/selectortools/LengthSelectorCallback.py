# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class LengthSelectorCallback(AbjadValueObject):
    r'''Length selector callback.

    ::

        >>> import abjad

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

    def __call__(self, argument, rotation=None):
        r'''Iterates iterable `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import selectortools
        assert isinstance(argument, collections.Iterable), repr(argument)
        inequality = self.length
        if not isinstance(inequality, selectortools.LengthInequality):
            inequality = selectortools.LengthInequality(
                length=inequality,
                operator_string='==',
                )
        result = []
        for subexpr in argument:
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
