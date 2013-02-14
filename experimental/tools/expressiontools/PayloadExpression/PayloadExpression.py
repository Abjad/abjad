from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools
from experimental.tools.expressiontools.Expression import Expression


class PayloadExpression(Expression):
    r'''Payload expression.

    ::

        >>> payload_expression = expressiontools.PayloadExpression([(4, 16), (2, 16)])

    ::

        >>> payload_expression
        PayloadExpression(((4, 16), (2, 16)))

    ::

        >>> z(payload_expression)
        expressiontools.PayloadExpression(
            ((4, 16), (2, 16))
            )

    Payload expressions are assumed to evaluate to a list or other iterable.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload):
        from experimental.tools import expressiontools
        assert not isinstance(payload, str), repr(payload)
        assert not isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        assert isinstance(payload, (str, tuple, list, 
            expressiontools.DivisionList, containertools.Container)), repr(payload)
        Expression.__init__(self)
        if isinstance(payload, list):
            payload = tuple(payload)
        self._payload = payload

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Logical AND of payload expression and `timespan`.

        ::

            >>> timespan = timespantools.Timespan((1, 16), (5, 16))
            >>> result = payload_expression & timespan

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                expressiontools.PayloadExpression(
                    (Division('[3, 16]', start_offset=Offset(1, 16)), 
                    Division('[1, 16]', start_offset=Offset(1, 4)))
                    )
                ])

        Return newly constructed payload expression.
        '''
        from experimental.tools import expressiontools
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        division_payload_expression = expressiontools.StartPositionedDivisionPayloadExpression(
            payload=payload, start_offset=0, voice_name='dummy voice name')
        result = division_payload_expression & timespan
        assert len(result) in (0, 1)
        if result:
            divisions = result[0].payload.divisions
            expression = self.new(payload=divisions)
            result[0] = expression
        return result

    def __getitem__(self, expr):
        '''Payload expression get item.

        ::

            >>> result = payload_expression[:1]

        ::

            >>> z(result)
            expressiontools.PayloadExpression(
                ((4, 16),)
                )

        Return newly constructed payload expression
        with referenced payload.
        '''
        payload = self.payload.__getitem__(expr)
        result = self.new(payload=payload)
        return result

    ### READ-ONLY PRIVATE PROPERTIES ##

    @property
    def elements(self):
        '''Payload expression elements.

        ::

            >>> payload_expression.elements
            ((4, 16), (2, 16))

        Return tuple.
        '''
        return self.payload[:]

    ### PRIVATE METHODS ###

    def _duration_helper(self, expression):
        if hasattr(expression, 'duration'):
            return expression.duration
        elif hasattr(expression, 'duration'):
            return expression.duration
        else:
            duration = durationtools.Duration(expression)
            return duration

    def evaluate(self):
        '''Evaluate payload expression.

            >>> payload_expression.evaluate()
            PayloadExpression(((4, 16), (2, 16)))

        Return payload expression.
        '''
        return self

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Payload expression payload:

        ::

            >>> payload_expression.payload
            ((4, 16), (2, 16))

        Return tuple or string.
        '''
        return self._payload

    @property
    def storage_format(self):
        '''Payload expression storage format:

        ::

            >>> z(payload_expression)
            expressiontools.PayloadExpression(
                ((4, 16), (2, 16))
                )

        Return string.
        '''
        return Expression.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition payload expression by ratio.

        ::

            >>> result = payload_expression.partition_by_ratio((1, 1))

        ::

            >>> for element in result:
            ...     z(element)
            expressiontools.PayloadExpression(
                ((4, 16),)
                )
            expressiontools.PayloadExpression(
                ((2, 16),)
                )

        Return list of newly constructed payload expressions.
        '''
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(self.payload, ratio)
        result = []
        for part in parts:
            part = self.new(payload=part)
            result.append(part)
        return result

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition payload expression by ratio of durations.

        ::

            >>> result = payload_expression.partition_by_ratio_of_durations((1, 1))

        ::

            >>> for element in result:
            ...     z(element)
            expressiontools.PayloadExpression(
                ((4, 16),)
                )
            expressiontools.PayloadExpression(
                ((2, 16),)
                )

        Return newly constructed payload expression.
        '''
        element_durations = [self._duration_helper(x) for x in self.payload]
        element_tokens = durationtools.durations_to_integers(element_durations)
        token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
        part_lengths = [len(x) for x in token_parts]
        duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
        element_parts = sequencetools.partition_sequence_by_counts(self.payload, part_lengths)
        result = []
        for part in element_parts:
            part = self.new(payload=part)
            result.append(part)
        return result

    def reflect(self):
        '''Reflect payload expression.

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> z(result)
            expressiontools.PayloadExpression(
                ((2, 16), (4, 16))
                )

        Return newly constructed payload expression.
        '''
        assert isinstance(self.payload, tuple), repr(self.payload)
        payload = type(self.payload)(reversed(self.payload))
        result = self.new(payload=payload)
        return result

    def repeat_to_duration(self, duration):
        '''Repeat payload expression to duration.

        ::

            >>> result = payload_expression.repeat_to_duration(Duration(13, 16))

        ::

            >>> z(result)
            expressiontools.PayloadExpression(
                (NonreducedFraction(4, 16), 
                NonreducedFraction(2, 16), 
                NonreducedFraction(4, 16), 
                NonreducedFraction(2, 16), 
                NonreducedFraction(1, 16))
                )

        Return newly constructed payload expression.
        '''
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        payload = sequencetools.repeat_sequence_to_weight_exactly(payload, duration)
        result = self.new(payload=payload)
        return result

    def repeat_to_length(self, length):
        '''Repeat payload expression to length.

        ::

            >>> result = payload_expression.repeat_to_length(4)

        ::

            >>> z(result)
            expressiontools.PayloadExpression(
                ((4, 16), (2, 16), (4, 16), (2, 16))
                )

        Return newly constructed payload expression.
        '''
        payload = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = self.new(payload=payload)
        return result

    def rotate(self, n):
        '''Rotate payload expression.

        ::

            >>> result = payload_expression.rotate(-1)

        ::

            >>> z(result)
            expressiontools.PayloadExpression(
                ((2, 16), (4, 16))
                )

        Return newly constructed payload expression.
        '''
        payload = sequencetools.rotate_sequence(self.payload, n)
        result = self.new(payload=payload)
        return result
