# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.PayloadExpression \
    import PayloadExpression


class IterablePayloadExpression(PayloadExpression):
    r'''Payload expression.

    ::

        >>> payload_expression = \
        ...     musicexpressiontools.IterablePayloadExpression(
        ...     [(4, 16), (2, 16)])

    ::

        >>> payload_expression
        IterablePayloadExpression(payload=((4, 16), (2, 16)))

    ::

        >>> z(payload_expression)
        musicexpressiontools.IterablePayloadExpression(
            payload=((4, 16), (2, 16))
            )

    Payload expressions are assumed to evaluate to a list or other iterable.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        from experimental.tools import musicexpressiontools
        assert not isinstance(payload, rhythmmakertools.RhythmMaker)
        assert not isinstance(payload, musicexpressiontools.StatalServerCursor)
        assert isinstance(payload, (
            str, tuple, list, 
            containertools.Container,
            datastructuretools.TypedList,
            musicexpressiontools.DivisionList,
            selectiontools.SliceSelection,
            ))
        if isinstance(payload, list):
            payload = tuple(payload)
        PayloadExpression.__init__(self, payload)

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Logical AND of payload expression and `timespan`.

        ::

            >>> timespan = timespantools.Timespan((1, 16), (5, 16))
            >>> result = payload_expression & timespan

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                musicexpressiontools.IterablePayloadExpression(
                    payload=(Division('[3, 16]', start_offset=Offset(1, 16)),
                    Division('[1, 16]', start_offset=Offset(1, 4)))
                    )
                ])

        Returns newly constructed payload expression.
        '''
        from experimental.tools import musicexpressiontools
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        division_payload_expression = \
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=payload, start_offset=0, voice_name='dummy voice name')
        result = division_payload_expression & timespan
        assert len(result) in (0, 1)
        if result:
            divisions = result[0].payload.divisions
            expression = self.new(payload=divisions)
            result[0] = expression
        return result

    def __getitem__(self, expr):
        r'''Payload expression get item.

        ::

            >>> result = payload_expression[:1]

        ::

            >>> z(result)
            musicexpressiontools.IterablePayloadExpression(
                payload=((4, 16),)
                )

        Returns newly constructed payload expression
        with referenced payload.
        '''
        payload = self.payload.__getitem__(expr)
        result = self.new(payload=payload)
        return result

    ### PRIVATE METHODS ###

    def _duration_helper(self, expression):
        if hasattr(expression, 'duration'):
            return expression.duration
        elif hasattr(expression, 'duration'):
            return expression.duration
        else:
            duration = durationtools.Duration(expression)
            return duration

    @staticmethod
    def _durations_to_integers(durations):
        r'''Change `durations` to integers:

        ::

            >>> durations = [Duration(2, 4), 3, (5, 16)]
            >>> for integer in payload_expression._durations_to_integers(
            ...     durations):
            ...     integer
            ...
            8
            48
            5

        Returns new object of `durations` type.
        '''
        from abjad.tools import durationtools
        # change to nonreduced fractions
        nonreduced_fractions = \
            durationtools.Duration.durations_to_nonreduced_fractions_with_common_denominator(
            durations)
        # find common denominator
        common_denominator = nonreduced_fractions[0].denominator
        # change to integers
        nonreduced_fractions = [
            common_denominator * nonreduced_fraction 
            for nonreduced_fraction in nonreduced_fractions
            ]
        fractions = [
            nonreduced_fraction.reduce() 
            for nonreduced_fraction in nonreduced_fractions
            ]
        assert all(fraction.denominator == 1 for fraction in fractions)
        integers = [fraction.numerator for fraction in fractions]
        # return integers
        return integers

    ### PUBLIC PROPERTIES ###

    @property
    def elements(self):
        r'''Payload expression elements.

        ::

            >>> payload_expression.elements
            ((4, 16), (2, 16))

        Returns tuple.
        '''
        return self.payload[:]

    @property
    def payload(self):
        r'''Payload expression payload:

        ::

            >>> payload_expression.payload
            ((4, 16), (2, 16))

        Returns tuple or string.
        '''
        return self._payload

    @property
    def storage_format(self):
        r'''Payload expression storage format:

        ::

            >>> z(payload_expression)
            musicexpressiontools.IterablePayloadExpression(
                payload=((4, 16), (2, 16))
                )

        Returns string.
        '''
        return PayloadExpression.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate payload expression.

            >>> payload_expression.evaluate()
            IterablePayloadExpression(payload=((4, 16), (2, 16)))

        Returns payload expression.
        '''
        return PayloadExpression.evaluate(self)

    def partition_by_ratio(self, ratio):
        r'''Partition payload expression by ratio.

        ::

            >>> result = payload_expression.partition_by_ratio((1, 1))

        ::

            >>> for element in result:
            ...     z(element)
            musicexpressiontools.IterablePayloadExpression(
                payload=((4, 16),)
                )
            musicexpressiontools.IterablePayloadExpression(
                payload=((2, 16),)
                )

        Returns list of newly constructed payload expressions.
        '''
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            self.payload, ratio)
        result = []
        for part in parts:
            part = self.new(payload=part)
            result.append(part)
        return result

    def partition_by_ratio_of_durations(self, ratio):
        r'''Partition payload expression by ratio of durations.

        ::

            >>> result = \
            ...     payload_expression.partition_by_ratio_of_durations((1, 1))

        ::

            >>> for element in result:
            ...     z(element)
            musicexpressiontools.IterablePayloadExpression(
                payload=((4, 16),)
                )
            musicexpressiontools.IterablePayloadExpression(
                payload=((2, 16),)
                )

        Returns newly constructed payload expression.
        '''
        element_durations = [self._duration_helper(x) for x in self.payload]
        element_tokens = self._durations_to_integers(element_durations)
        token_parts = sequencetools.partition_sequence_by_ratio_of_weights(
                element_tokens, ratio)
        part_lengths = [len(x) for x in token_parts]
        duration_parts = sequencetools.partition_sequence_by_counts(
            element_durations, part_lengths)
        element_parts = sequencetools.partition_sequence_by_counts(
            self.payload, part_lengths)
        result = []
        for part in element_parts:
            part = self.new(payload=part)
            result.append(part)
        return result

    def reflect(self):
        r'''Reflect payload expression.

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> z(result)
            musicexpressiontools.IterablePayloadExpression(
                payload=((2, 16), (4, 16))
                )

        Returns newly constructed payload expression.
        '''
        assert isinstance(self.payload, tuple), repr(self.payload)
        payload = type(self.payload)(reversed(self.payload))
        result = self.new(payload=payload)
        return result

    def repeat_to_duration(self, duration):
        r'''Repeat payload expression to duration.

        ::

            >>> result = \
            ...     payload_expression.repeat_to_duration(Duration(13, 16))

        ::

            >>> z(result)
            musicexpressiontools.IterablePayloadExpression(
                payload=(NonreducedFraction(4, 16),
                NonreducedFraction(2, 16),
                NonreducedFraction(4, 16),
                NonreducedFraction(2, 16),
                NonreducedFraction(1, 16))
                )

        Returns newly constructed payload expression.
        '''
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        payload = sequencetools.repeat_sequence_to_weight_exactly(
            payload, duration)
        result = self.new(payload=payload)
        return result

    def repeat_to_length(self, length):
        r'''Repeat payload expression to length.

        ::

            >>> result = payload_expression.repeat_to_length(4)

        ::

            >>> z(result)
            musicexpressiontools.IterablePayloadExpression(
                payload=((4, 16), (2, 16), (4, 16), (2, 16))
                )

        Returns newly constructed payload expression.
        '''
        payload = sequencetools.repeat_sequence_to_length(
            self.payload, length)
        result = self.new(payload=payload)
        return result

    def rotate(self, n):
        r'''Rotate payload expression.

        ::

            >>> result = payload_expression.rotate(-1)

        ::

            >>> z(result)
            musicexpressiontools.IterablePayloadExpression(
                payload=((2, 16), (4, 16))
                )

        Returns newly constructed payload expression.
        '''
        payload = sequencetools.rotate_sequence(self.payload, n)
        result = self.new(payload=payload)
        return result
