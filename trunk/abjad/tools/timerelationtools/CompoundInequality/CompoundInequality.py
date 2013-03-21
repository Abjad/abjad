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
                'timespan_1.start_offset <= timespan_2.start_offset',
                'timespan_2.start_offset < timespan_1.stop_offset'
                ]),
            timerelationtools.CompoundInequality([
                'timespan_2.start_offset <= timespan_1.start_offset',
                'timespan_1.start_offset < timespan_2.stop_offset'
                ])
            ])

    Return compound inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_inequalities', '_logical_operator', '_name',
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def logical_operator(self):
        '''Compound inequality logical operator.
        '''
        return self._logical_operator

    ### PUBLIC METHODS ###

    def get_offset_indices(self, timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets):
        from experimental.tools import timerelationtools
        from experimental.tools import timespantools
        timespans = timespantools.TimespanInventory()
        for element in self:
            if isinstance(element, type(self)):
                result = element.get_offset_indices(
                    timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
                timespans.extend(result)
            elif isinstance(element, str):
                offset_indices = timerelationtools.simple_inequality_to_offset_indices(
                    element, timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
                timespan = timespantools.Timespan(*offset_indices)
                timespans.append(timespan)
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
