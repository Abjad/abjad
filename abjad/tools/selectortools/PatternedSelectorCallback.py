# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class PatternedSelectorCallback(AbjadValueObject):
    r'''A patterned selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_apply_to_each',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        apply_to_each=None,
        ):
        if pattern is not None:
            assert isinstance(pattern, patterntools.Pattern)
        self._pattern = pattern
        if apply_to_each is not None:
            apply_to_each = bool(apply_to_each)
        self._apply_to_each = apply_to_each

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        if not self.pattern:
            return expr
        result = []
        if self.apply_to_each:
            for subexpr in expr:
                subresult = []
                length = len(subexpr)
                for index, item in enumerate(subexpr):
                    if self.pattern.matches_index(
                        index,
                        length,
                        rotation=rotation,
                        ):
                        subresult.append(item)
                if subresult:
                    subresult = selectiontools.Selection(subresult)
                    result.append(subresult)
        else:
            length = len(expr)
            for index, item in enumerate(expr):
                if self.pattern.matches_index(
                    index,
                    length,
                    rotation=rotation,
                    ):
                    result.append(item)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def apply_to_each(self):
        r'''Is true if patterned selector callback is applied against each
        subexpression. Otherwise false.

        Returns true or false.
        '''
        return self._apply_to_each

    @property
    def pattern(self):
        r'''Gets pattern of patterned selector callback.

        Returns pattern.
        '''
        return self._pattern
