# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class PatternedSelectorCallback(AbjadValueObject):
    r'''Patterned selector callback.

    ::

        >>> import abjad

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
            assert isinstance(pattern, datastructuretools.Pattern)
        self._pattern = pattern
        if apply_to_each is not None:
            apply_to_each = bool(apply_to_each)
        self._apply_to_each = apply_to_each

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        if not self.pattern:
            return argument
        result = []
        if self.apply_to_each:
            for subexpr in argument:
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
            length = len(argument)
            for index, item in enumerate(argument):
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
