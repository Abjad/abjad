# -*- encoding: utf-8 -*-
import itertools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class LogicalMeasureSelectorCallback(AbjadValueObject):
    r'''A measure selector callback.

    Groups components by start measure.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, expr):
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