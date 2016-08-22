# -*- coding: utf-8 -*-
import itertools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class LogicalMeasureSelectorCallback(AbjadValueObject):
    r'''A logical measure selector callback.

    ..  container:: example

        Score for examples 1 - 3:

        ::

            >>> staff = Staff("c'8 d' e' f' g' a' b' c''")
            >>> attach(TimeSignature((2, 8)), staff[0])
            >>> attach(TimeSignature((3, 8)), staff[4])
            >>> attach(TimeSignature((1, 8)), staff[7])
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 1.** Selects the leaves of every logical measure:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> for x in selector(staff):
            ...     x
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8")])
            Selection([Note("c''8")])

    ..  container:: example

        **Example 2.** Selects the first leaf of every logical measure:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> selector = selector[0]
            >>> selector(staff)
            Selection([Note("c'8"), Note("e'8"), Note("g'8"), Note("c''8")])

    ..  container:: example

        **Example 3.** Selects the last leaf of every logical measure:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> selector = selector[-1]
            >>> selector(staff)
            Selection([Note("d'8"), Note("f'8"), Note("b'8"), Note("c''8")])

    ..  container:: example

        **Example 4.** Works with implicit time signatures:

        ::

            >>> staff = Staff("c'4 d' e' f' g' a' b' c''")
            >>> score = Score([staff])
            >>> scheme = schemetools.SchemeMoment((1, 16))
            >>> set_(score).proportional_notation_duration = scheme
            >>> show(score) # doctest: +SKIP

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> for x in selector(score):
            ...     x
            ...
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
            Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

    Groups components by the logical measure of component start offset.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(expr)
        selections = []
        for subexpr in expr:
            selections_ = self._group(subexpr)
            selections.extend(selections_)
        return tuple(selections)

    ### PRIVATE METHODS ###


    def _get_first_component(self, expr):
        from abjad.tools import scoretools
        if isinstance(expr, scoretools.Component):
            return expr
        else:
            component = expr[0]
            assert isinstance(component, scoretools.Component)
            return component

    def _get_logical_measure_number(self, expr):
        first_component = self._get_first_component(expr)
        assert first_component._logical_measure_number is not None
        return first_component._logical_measure_number

    def _group(self, expr):
        selections = []
        first_component = self._get_first_component(expr)
        first_component._update_logical_measure_numbers()
        pairs = itertools.groupby(
            expr,
            lambda _: self._get_logical_measure_number(_),
            )
        for value, group in pairs:
            selection = selectiontools.Selection(list(group))
            selections.append(selection)
        return tuple(selections)
