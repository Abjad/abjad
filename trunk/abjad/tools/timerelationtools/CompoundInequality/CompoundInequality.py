from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class CompoundInequality(ObjectInventory):
    '''.. versionadded:: 2.12

    Compound inequality:

    ::

        >>> compound_inequality = timerelationtools.CompoundInequality([
        ...    timerelationtools.CompoundInequality([
        ...        'timespan_1.start <= timespan_2.start',
        ...        'timespan_2.start < timespan_1.stop'],
        ...         logical_operator='and'),
        ...     timerelationtools.CompoundInequality([
        ...        'timespan_2.start <= timespan_1.start',
        ...        'timespan_1.start < timespan_2.stop'],
        ...        logical_operator='and')],
        ...    logical_operator='or')

    ::

        >>> z(compound_inequality)
        timerelationtools.CompoundInequality([
            timerelationtools.CompoundInequality([
                'timespan_1.start <= timespan_2.start',
                'timespan_2.start < timespan_1.stop'
                ]),
            timerelationtools.CompoundInequality([
                'timespan_2.start <= timespan_1.start',
                'timespan_1.start < timespan_2.stop'
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
