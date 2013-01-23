from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.tools.settingtools.PayloadExpression import PayloadExpression
from experimental.tools.settingtools.StartPositionedObject import StartPositionedObject


class StartPositionedPayloadExpression(PayloadExpression, StartPositionedObject):
    '''Start-positioned payload expression.

        >>> expression = settingtools.StartPositionedPayloadExpression(
        ...     [(4, 16), (2, 16)], start_offset=Offset(40, 8))

    ::

        >>> expression = expression.repeat_to_length(6)

    ::

        >>> z(expression)
        settingtools.StartPositionedPayloadExpression(
            payload=((4, 16), (2, 16), (4, 16), (2, 16), (4, 16), (2, 16)),
            start_offset=durationtools.Offset(5, 1)
            )

    Start-positioned payload expressions are assumed to evaluate
    to a list or other iterable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None):
        PayloadExpression.__init__(self, payload=payload)
        StartPositionedObject.__init__(self, start_offset=start_offset)

    ### PRIVATE METHODS ###

    def _change_payload_to_numbers(self):
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            payload = self.payload
        return payload

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Start-positioned payload expression start offset:

        ::

            >>> expression.start_offset
            Offset(5, 1)

        Return offset.
        '''
        return StartPositionedObject.start_offset.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition payload by `ratio`:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.partition_by_ratio((1, 1))

        ::
    
            >>> for x in result:
            ...     z(x)
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 8), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(0, 1)
                )
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 8), (6, 4), (6, 4)),
                start_offset=durationtools.Offset(9, 4)
                )

        Return newly constructed start-positioned payload expression.
        '''
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(self.payload, ratio)
        number_payload = self._change_payload_to_numbers()
        number_parts = sequencetools.partition_sequence_by_ratio_of_lengths(number_payload, ratio)
        durations = [sum(number_part) for number_part in number_parts]
        start_offsets = mathtools.cumulative_sums_zero(durations)[:-1]
        result = []
        for part, start_offset in zip(parts, start_offsets):
            expression = type(self)(payload=part, start_offset=start_offset)
            result.append(expression)
        return result

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition payload by `ratio` of durations:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.partition_by_ratio_of_durations((1, 1))

        ::
    
            >>> for x in result:
            ...     z(x)
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 8), (6, 8), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(0, 1)
                )
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 4), (6, 4)),
                start_offset=durationtools.Offset(3, 1)
                )

        Return newly constructed start-positioned payload expression.
        '''
        payload = self._change_payload_to_numbers()
        integers = durationtools.durations_to_integers(payload)
        parts = sequencetools.partition_sequence_by_ratio_of_weights(integers, ratio)
        part_lengths = [len(part) for part in parts]
        number_parts = sequencetools.partition_sequence_by_counts(payload, part_lengths)
        parts = sequencetools.partition_sequence_by_counts(self.payload, part_lengths)
        durations = [sum(number_part) for number_part in number_parts]
        start_offsets = mathtools.cumulative_sums_zero(durations)[:-1]
        result = []
        for part, start_offset in zip(parts, start_offsets):
            expression = type(self)(payload=part, start_offset=start_offset)
            result.append(expression)
        return result

    def reflect(self):
        '''Reflect payload about axis:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.reflect()    

        ::

            >>> z(result)
            settingtools.StartPositionedPayloadExpression(
                payload=((3, 4), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(2, 1)
                )

        Return newly constructed start-positioned payload expression.
        '''
        expression = PayloadExpression.reflect(self)
        payload = expression.payload
        result = type(self)(payload=payload, start_offset=self.start_offset)
        return result

    def repeat_to_duration(self, duration):
        '''Repeat payload to `duration`:

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.repeat_to_duration(Duration(17, 4))

        ::
    
            >>> z(result)
            settingtools.StartPositionedPayloadExpression(
                payload=(NonreducedFraction(6, 8), NonreducedFraction(6, 8), 
                    NonreducedFraction(3, 4), NonreducedFraction(6, 8), 
                    NonreducedFraction(6, 8), NonreducedFraction(4, 8)),
                start_offset=durationtools.Offset(2, 1)
                )
        
        Return newly constructed start-positioned payload expression.
        '''
        payload = self._change_payload_to_numbers()
        payload = sequencetools.repeat_sequence_to_weight_exactly(payload, duration)
        result = type(self)(payload=payload, start_offset=self.start_offset)
        return result

    def repeat_to_length(self, length):
        '''Repeat payload to `length`:

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.repeat_to_length(5)

        ::
    
            >>> z(result)
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 8), (6, 8), (3, 4), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(2, 1)
                )

        Return newly constructed start-positioned payload expression.
        '''
        expression = PayloadExpression.repeat_to_length(self, length)
        result = type(self)(payload=expression.payload, start_offset=self.start_offset)
        return result

    def rotate(self, rotation):
        '''Rotate payload by `rotation`:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.rotate(-1)    

        
        Return newly constructed start-positioned payload expression.
        '''
        expression = PayloadExpression.rotate(self, rotation)
        result = type(self)(payload=expression.payload, start_offset=self.start_offset)
        return result

    def translate(self, translation):
        '''Translate division region product by `translation`:
        
            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedPayloadExpression(payload, Offset(2))

        ::

            >>> result = expression.translate(-1)

        ::
            >>> z(result)
            settingtools.StartPositionedPayloadExpression(
                payload=((6, 8), (6, 8), (3, 4)),
                start_offset=durationtools.Offset(1, 1)
                )

        Return newly constructed start-positioned payload expression.
        '''
        new_start_offset = self.start_offset + translation
        result = type(self)(payload=self.payload, start_offset=new_start_offset)
        return result
