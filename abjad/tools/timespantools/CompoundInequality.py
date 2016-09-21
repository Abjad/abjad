# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.datastructuretools.TypedList import TypedList


class CompoundInequality(TypedList):
    '''A compound time-relation inequality.

    ::

        >>> compound_inequality = timespantools.CompoundInequality([
        ...    timespantools.CompoundInequality([
        ...        'timespan_1.start_offset <= timespan_2.start_offset',
        ...        'timespan_2.start_offset < timespan_1.stop_offset'],
        ...         logical_operator='and'),
        ...     timespantools.CompoundInequality([
        ...        'timespan_2.start_offset <= timespan_1.start_offset',
        ...        'timespan_1.start_offset < timespan_2.stop_offset'],
        ...        logical_operator='and')],
        ...    logical_operator='or',
        ...     )

    ::

        >>> print(format(compound_inequality))
        timespantools.CompoundInequality(
            [
                timespantools.CompoundInequality(
                    [
                        timespantools.Inequality('timespan_1.start_offset <= timespan_2.start_offset'),
                        timespantools.Inequality('timespan_2.start_offset < timespan_1.stop_offset'),
                        ],
                    logical_operator='and',
                    ),
                timespantools.CompoundInequality(
                    [
                        timespantools.Inequality('timespan_2.start_offset <= timespan_1.start_offset'),
                        timespantools.Inequality('timespan_1.start_offset < timespan_2.stop_offset'),
                        ],
                    logical_operator='and',
                    ),
                ],
            logical_operator='or',
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_logical_operator',
        '_name',
        )

    logical_operator_dictionary = {
        'and': '&',
        'or': '|',
        'xor': '^',
        }

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        logical_operator='and',
        ):
        TypedList.__init__(self,
            items=items,
            )
        self._logical_operator = logical_operator

    ### PUBLIC METHODS ###

    def evaluate(
        self,
        timespan_1_start_offset,
        timespan_1_stop_offset,
        timespan_2_start_offset,
        timespan_2_stop_offset,
        ):
        r'''Evalutes compound inequality.

        Returns true or false.
        '''
        from abjad.tools import timespantools
        truth_values = []
        for inequality in self:
            # TODO: compress the following two branches
            if isinstance(inequality, timespantools.Inequality):
                truth_value = inequality.evaluate(
                    timespan_1_start_offset, timespan_1_stop_offset,
                    timespan_2_start_offset, timespan_2_stop_offset)
                truth_values.append(truth_value)
            elif isinstance(inequality, type(self)):
                truth_value = inequality.evaluate(
                    timespan_1_start_offset, timespan_1_stop_offset,
                    timespan_2_start_offset, timespan_2_stop_offset)
                truth_values.append(truth_value)
        if self.logical_operator == 'and':
            truth_value = all(truth_values)
        elif self.logical_operator == 'or':
            truth_value = any(truth_values)
        elif self.logical_operator == 'xor':
            truth_value = bool(len([x for x in truth_values if x]) == 1)
        else:
            message = 'unknown logical operator: {!r}.'
            message = message.format(self.logical_operator)
            raise ValueError(message)
        return truth_value

    def evaluate_offset_inequality(
        self,
        timespan_start,
        timespan_stop,
        offset,
        ):
        r'''Evalutes offset inequality.

        Returns true or false.
        '''
        from abjad.tools import timespantools
        truth_values = []
        for inequality in self:
            if isinstance(inequality, timespantools.Inequality):
                truth_value = inequality.evaluate_offset_inequality(
                    timespan_start, timespan_stop, offset)
                truth_values.append(truth_value)
            elif isinstance(inequality, type(self)):
                truth_value = inequality.evaluate_offset_inequality(
                    timespan_start, timespan_stop, offset)
                truth_values.append(truth_value)
            else:
                message = 'unknown inequality: {!r}.'
                message = message.format(inequality)
                raise TypeError(message)
        assert truth_values, repr(truth_values)
        if self.logical_operator == 'and':
            truth_value = all(truth_values)
        elif self.logical_operator == 'or':
            truth_value = any(truth_values)
        elif self.logical_operator == 'xor':
            truth_value = bool(len([x for x in truth_values if x]) == 1)
        else:
            message = 'unknown logical operator: {!r}.'
            message = message.format(self.logical_operator)
            raise ValueError(message)
        return truth_value

    def get_offset_indices(
        self,
        timespan_1,
        timespan_2_start_offsets,
        timespan_2_stop_offsets,
        ):
        r'''Gets offset indices of compound inequality.
        '''
        from abjad.tools import timespantools
        from abjad.tools import timespantools
        timespans = timespantools.TimespanInventory()
        for element in self:
            # TODO: compress the following two branches
            if isinstance(element, type(self)):
                result = element.get_offset_indices(
                    timespan_1,
                    timespan_2_start_offsets,
                    timespan_2_stop_offsets)
                timespans.extend(result)
            elif isinstance(element, timespantools.Inequality):
                offset_indices = element.get_offset_indices(
                    timespan_1,
                    timespan_2_start_offsets,
                    timespan_2_stop_offsets)
                timespan = timespantools.Timespan(*offset_indices)
                timespans.append(timespan)
            else:
                message = 'unknown inequality: {!r}.'
                message = message(element)
                raise TypeError(message)
        if self.logical_operator == 'and':
            result = timespans.compute_logical_and()
        elif self.logical_operator == 'or':
            timespans.sort()
            result = timespans.compute_logical_or()
        elif self.logical_operator == 'xor':
            result = timespans.compute_logical_xor()
        else:
            message = 'unknown logical operator: {!r}.'
            message = mesage.format(self.logical_operator)
            raise ValueError(message)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import timespantools
        def coerce_(expr):
            if isinstance(expr, str):
                return timespantools.Inequality(expr)
            elif isinstance(expr, timespantools.Inequality):
                return expr
            elif isinstance(expr, timespantools.CompoundInequality):
                return expr
            else:
                raise TypeError(expr)
        return coerce_

    ### PUBLIC PROPERTIES ###

    @property
    def logical_operator(self):
        r'''Compound inequality logical operator.
        '''
        return self._logical_operator
