from abjad.tools import durationtools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class CompoundInequality(ObjectInventory):
    '''.. versionadded:: 2.12

    Compound inequality:

    ::

        >>> compound_inequality = timerelationtools.CompoundInequality([
        ...    timerelationtools.CompoundInequality([
        ...        'timespan_1.start_offset <= timespan_2.start_offset',
        ...        'timespan_2.start_offset < timespan_1.stop_offset'],
        ...         logical_operator='and'),
        ...     timerelationtools.CompoundInequality([
        ...        'timespan_2.start_offset <= timespan_1.start_offset',
        ...        'timespan_1.start_offset < timespan_2.stop_offset'],
        ...        logical_operator='and')],
        ...    logical_operator='or')

    ::

        >>> z(compound_inequality)
        timerelationtools.CompoundInequality([
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan_1.start_offset <= timespan_2.start_offset'),
                timerelationtools.SimpleInequality('timespan_2.start_offset < timespan_1.stop_offset')
                ],
                logical_operator='and'
                ),
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan_2.start_offset <= timespan_1.start_offset'),
                timerelationtools.SimpleInequality('timespan_1.start_offset < timespan_2.stop_offset')
                ],
                logical_operator='and'
                )
            ],
            logical_operator='or'
            )

    Return compound inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_logical_operator', '_name',
        )

    logical_operator_dictionary = {
        'and': '&',
        'or': '|',
        'xor': '^',
        }

    ### INITIALIZER ###

    def __init__(self, tokens=None, logical_operator='and', name=None):
        ObjectInventory.__init__(self, tokens=tokens, name=name)
        self._logical_operator = logical_operator

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import timerelationtools
        def to_inequality(expr):
            if isinstance(expr, str):
                return timerelationtools.SimpleInequality(expr)
            elif isinstance(expr, timerelationtools.SimpleInequality):
                return expr
            elif isinstance(expr, timerelationtools.CompoundInequality):
                return expr
            else:
                raise TypeError(expr)
        return to_inequality

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def logical_operator(self):
        '''Compound inequality logical operator.
        '''
        return self._logical_operator

    ### PUBLIC METHODS ###

    def evaluate(self, timespan_1_start_offset, timespan_1_stop_offset, 
        timespan_2_start_offset, timespan_2_stop_offset):
        from abjad.tools import timerelationtools
        truth_values = []
        for inequality in self:
            # TODO: compress the following two branches
            if isinstance(inequality, timerelationtools.SimpleInequality):
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
            raise ValueError(self.logical_operator)
        return truth_value

    def evaluate_offset_inequality(self, timespan_start, timespan_stop, offset):
        from abjad.tools import timerelationtools
        truth_values = []
        for inequality in self:
            if isinstance(inequality, timerelationtools.SimpleInequality):
                truth_value = inequality.evaluate_offset_inequality(timespan_start, timespan_stop, offset)
                truth_values.append(truth_value)
            elif isinstance(inequality, type(self)):
                truth_value = inequality.evaluate_offset_inequality(
                    timespan_start, timespan_stop, offset)
                truth_values.append(truth_value)
            else:
                raise TypeError(inequality)
        assert truth_values, repr(truth_values)
        if self.logical_operator == 'and':
            truth_value = all(truth_values)
        elif self.logical_operator == 'or':
            truth_value = any(truth_values)
        elif self.logical_operator == 'xor':
            truth_value = bool(len([x for x in truth_values if x]) == 1)
        else:
            raise ValueError(self.logical_operator)
        return truth_value
        
    def get_offset_indices(self, timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets):
        from experimental.tools import timerelationtools
        from experimental.tools import timespantools
        timespans = timespantools.TimespanInventory()
        for element in self:
            # TODO: compress the following two branches
            if isinstance(element, type(self)):
                result = element.get_offset_indices(
                    timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
                timespans.extend(result)
            elif isinstance(element, timerelationtools.SimpleInequality):
                offset_indices = element.get_offset_indices(
                    timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
                timespan = timespantools.Timespan(*offset_indices)
                timespans.append(timespan)
            else:
                raise TypeError(element)
        if self.logical_operator == 'and':
            result = timespans.compute_logical_and()
        elif self.logical_operator == 'or':
            timespans.sort()
            result = timespans.compute_logical_or()
        elif self.logical_operator == 'xor':
            result = timespans.compute_logical_xor()
        else:
            raise ValueError(self.logical_operator)         
        return result
