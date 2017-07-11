# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class ExtraLeafSelectorCallback(AbjadValueObject):
    r'''Extra leaf selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_with_next_leaf',
        '_with_previous_leaf',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        with_next_leaf=False,
        with_previous_leaf=False,
        ):
        self._with_next_leaf = bool(with_next_leaf)
        self._with_previous_leaf = bool(with_previous_leaf)

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools.topleveltools import select
        assert isinstance(argument, collections.Iterable), repr(argument)
        result = []
        for subexpr in argument:
            if isinstance(subexpr, scoretools.Leaf):
                subexpr = selectiontools.Selection([subexpr])
            subresult = []
            if self.with_previous_leaf:
                if isinstance(subexpr[0], selectiontools.LogicalTie):
                    first_leaf = subexpr[0].head
                else:
                    first_leaf = subexpr[0]
                previous_leaf = first_leaf._get_leaf(-1)
                if previous_leaf is not None:
                    subresult.append(previous_leaf)
            if isinstance(subexpr, selectiontools.Selection):
                subresult.extend(subexpr)
            else:
                subresult.append(subexpr)
            if self.with_next_leaf:
                if isinstance(subexpr[-1], selectiontools.LogicalTie):
                    last_leaf = subexpr[-1].tail
                else:
                    last_leaf = subexpr[-1]
                next_leaf = last_leaf._get_leaf(1)
                if next_leaf is not None:
                    subresult.append(next_leaf)
            subresult = select(subresult)
            result.append(subresult)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def with_next_leaf(self):
        r'''Gets next leaf inclusion.

        Returns true or false.
        '''
        return self._with_next_leaf

    @property
    def with_previous_leaf(self):
        r'''Gets previous leaf inclusion.

        Returns true or false.
        '''
        return self._with_previous_leaf
