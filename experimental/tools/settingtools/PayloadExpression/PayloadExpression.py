from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools
from experimental.tools.settingtools.Expression import Expression


class PayloadExpression(Expression):
    r'''Payload expression.

    ::

        >>> expression = settingtools.PayloadExpression([(4, 16), (2, 16)])

    ::

        >>> expression
        PayloadExpression(((4, 16), (2, 16)))

    ::

        >>> z(expression)
        settingtools.PayloadExpression(
            ((4, 16), (2, 16))
            )

    Payload expressions are assumed to evaluate to a list or other iterable.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload):
        from experimental.tools import settingtools
        assert not isinstance(payload, str), repr(payload)
        assert not isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        assert isinstance(payload, (str, tuple, list, 
            settingtools.DivisionList, containertools.Container)), repr(payload)
        Expression.__init__(self)
        if isinstance(payload, list):
            payload = tuple(payload)
        self._payload = payload

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Logical AND of payload expression and `timespan`.

        Return newly constructed payload expression.
        '''
        from experimental.tools import settingtools
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        division_payload_expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=payload, start_offset=0, voice_name='dummy voice name')
        result = division_payload_expression & timespan
        assert len(result) in (0, 1)
        if result:
            divisions = result[0].payload.divisions
            expression = self.new(payload=divisions)
            result[0] = expression
        return result

    def __getitem__(self, expr):
        payload = self.payload.__getitem__(expr)
        result = self.new(payload=payload)
        return result

    ### READ-ONLY PRIVATE PROPERTIES ##

    @property
    def elements(self):
        return self.payload[:]

    ### PRIVATE METHODS ###

    def _duration_helper(self, expression):
        if hasattr(expression, 'duration'):
            return expression.duration
        elif hasattr(expression, 'prolated_duration'):
            return expression.prolated_duration
        else:
            duration = durationtools.Duration(expression)
            return duration

    def _evaluate(self):
        return self

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Payload expression payload:

        ::

            >>> expression.payload
            ((4, 16), (2, 16))

        Return tuple or string.
        '''
        return self._payload

    @property
    def storage_format(self):
        '''Payload expression storage format:

        ::

            >>> z(expression)
            settingtools.PayloadExpression(
                ((4, 16), (2, 16))
                )

        Return string.
        '''
        return Expression.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition by ratio.

        Return newly constructed payload expression.
        '''
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(self.payload, ratio)
        result = []
        for part in parts:
            part = self.new(payload=part)
            result.append(part)
        return result

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition by ratio of durations.

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
        '''Reflect.

        Return newly constructed payload expression.
        '''
        # TODO: eventually allow only tuple or list
        #assert isinstance(self.payload, (tuple, list)), repr(self.payload)
        if isinstance(self.payload, (tuple, list)):
            payload = type(self.payload)(reversed(self.payload))
            result = self.new(payload=payload)
            return result
        # TODO: This is probably the source of the "can't look up parseable string rhythm setting" bug.
        #       Means that parseable strings shouldn't be passed around as PayloadExpression objects.
        elif isinstance(self.payload, str):
            return self
        else:
            raise TypeError(self.payload)

    def repeat_to_duration(self, duration):
        '''Repeat to duration.

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
        '''Repeat to length.

        Return newly constructed payload expression.
        '''
        payload = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = self.new(payload=payload)
        return result

    def rotate(self, n):
        '''Rotate.

        Return newly constructed payload expression.
        '''
        payload = sequencetools.rotate_sequence(self.payload, n)
        result = self.new(payload=payload)
        return result
