import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.specificationtools.StartPositionedPayloadExpression import \
    StartPositionedPayloadExpression


class StartPositionedDivisionPayloadExpression(StartPositionedPayloadExpression):
    r'''Start-positioned division payload expression.

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
        ...     payload, Offset(0))

    ::

        >>> z(payload_expression)
        specificationtools.StartPositionedDivisionPayloadExpression(
            payload=specificationtools.DivisionList(
                [Division('[6, 8]', start_offset=Offset(0, 1)), 
                Division('[6, 8]', start_offset=Offset(3, 4)), 
                Division('[3, 4]', start_offset=Offset(3, 2))],
                start_offset=durationtools.Offset(0, 1)
                ),
            start_offset=durationtools.Offset(0, 1)
            )

    Start-positioned division payload expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        from experimental.tools import specificationtools
        payload = specificationtools.DivisionList(payload, start_offset=start_offset, voice_name=voice_name)
        StartPositionedPayloadExpression.__init__(self, 
            payload=payload, start_offset=start_offset, voice_name=voice_name) 

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Keep intersection of start-positioned 
        division payload expression and `timespan`.

        Example 1. Intersection on the left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression & timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(0, 1))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Example 2. Intersection on the right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression & timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(17, 8))],
                        start_offset=durationtools.Offset(17, 8)
                        ),
                    start_offset=durationtools.Offset(17, 8)
                    )
                ])

        Example 3. Trisection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression & timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[5, 8]', start_offset=Offset(1, 8)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[5, 8]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(1, 8)
                        ),
                    start_offset=durationtools.Offset(1, 8)
                    )
                ])

        Example 4. No intersection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression & timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__and__(self, timespan)

    def __getitem__(self, expr):
        '''Get start-positioned division payload expression item.

        ::

            >>> result = payload_expression[:2]

        ::

            >>> z(result)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Return newly constructed start-positioned division payload expression.
        '''
        assert isinstance(expr, slice), repr(expr)
        divisions = self.payload.__getitem__(expr)
        if divisions:
            start_offset = divisions[0].start_offset
        else:
            start_offset = durationtools.Offset(0)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=start_offset)
        return result

    def __or__(self, expr):
        '''Logical OR of two start-positioned division payload expressions:

        ::

            >>> payload_expression_1 = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     2 * [(3, 16)], Offset(0))
            >>> timespan = timespantools.Timespan(Offset(6, 16))
            >>> payload_expression_2 = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     2 * [(2, 16)], Offset(6, 16))

        ::

            >>> payload_expression_1.timespan.stops_when_timespan_starts(payload_expression_2)
            True

        ::

            >>> result = payload_expression_1 | payload_expression_2

        ::
        
            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[3, 16]', start_offset=Offset(0, 1)), 
                        Division('[3, 16]', start_offset=Offset(3, 16)), 
                        Division('[2, 16]', start_offset=Offset(3, 8)), 
                        Division('[2, 16]', start_offset=Offset(1, 2))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__or__(self, expr)

    def __sub__(self, timespan):
        '''Subtract `timespan` from start-positioned division payload expression.

        Example 1. Subtract from left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression - timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[5, 8]', start_offset=Offset(1, 8)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[3, 4]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(1, 8)
                        ),
                    start_offset=durationtools.Offset(1, 8)
                    )
                ])

        Example 2. Subtract from right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression - timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[5, 8]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Example 3. Subtract from middle:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression - timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(0, 1))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(17, 8))],
                        start_offset=durationtools.Offset(17, 8)
                        ),
                    start_offset=durationtools.Offset(17, 8)
                    )
                ])

        Example 4. Subtract from nothing:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = payload_expression - timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[3, 4]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__sub__(self, timespan)

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        from experimental.tools import specificationtools
        divisions = copy.deepcopy(self.payload.divisions)
        self._payload = specificationtools.DivisionList(
            [], voice_name=self.voice_name, start_offset=self.start_offset)
        shards = sequencetools.split_sequence_by_weights(
            divisions, offsets, cyclic=False, overhang=True)
        result, total_duration = [], durationtools.Duration(0)
        for shard in shards:
            shard = specificationtools.DivisionList(
                shard, voice_name=self.voice_name, start_offset=total_duration)
            result.append(shard)
            total_duration += shard.duration
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def elements(self):
        '''Start-positioned division payload expression elements.

        ::

            >>> payload_expression.elements
            [Division('[6, 8]', start_offset=Offset(0, 1)), 
            Division('[6, 8]', start_offset=Offset(3, 4)), 
            Division('[3, 4]', start_offset=Offset(3, 2))]

        Return list.
        '''
        return self.payload.divisions

    @property
    def payload(self):
        '''Start-positioned division payload expression payload.

        ::

            >>> payload_expression.payload
            DivisionList('[6, 8], [6, 8], [3, 4]')

        Return division list.
        '''
        return StartPositionedPayloadExpression.payload.fget(self)

    @property
    def start_offset(self):
        '''Start-positioned division payload expression start offset.

        ::

            >>> payload_expression.start_offset
            Offset(0, 1)

        Return offset.
        '''
        return StartPositionedPayloadExpression.start_offset.fget(self)

    @property
    def stop_offset(self):
        '''Start-positioned division payload expression stop offset.

        ::

            >>> payload_expression.stop_offset
            Offset(9, 4)

        Return offset.
        '''
        return StartPositionedPayloadExpression.stop_offset.fget(self)

    @property
    def storage_format(self):
        '''Start-positioned division payload expression storage format.

        ::

            >>> z(payload_expression)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4)), 
                    Division('[3, 4]', start_offset=Offset(3, 2))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Return string.
        '''
        return StartPositionedPayloadExpression.storage_format.fget(self)

    @property
    def timespan(self):
        '''Start-positioned division payload expression timespan.

        ::

            >>> payload_expression.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Return timespan.
        '''
        return StartPositionedPayloadExpression.timespan.fget(self)

    @property
    def voice_name(self):
        '''Start-positioned division payload expression voice name.

        ::

            >>> payload_expression.voice_name is None
            True

        Return string.
        '''
        return StartPositionedPayloadExpression.voice_name.fget(self)
        
    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition start-positioned division payload expression by `ratio`.

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.partition_by_ratio((1, 1))

        ::

            >>> z(result)
            specificationtools.TimespanScopedSingleContextSetExpressionInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[6, 8]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(9, 4)), 
                        Division('[6, 4]', start_offset=Offset(3, 1)), 
                        Division('[6, 4]', start_offset=Offset(9, 2))],
                        start_offset=durationtools.Offset(9, 4)
                        ),
                    start_offset=durationtools.Offset(9, 4)
                    )
                ])

        Operate in place and return newly constructed inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio(self, ratio)

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition start-positioned division payload expression by `ratio` of durations.

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.partition_by_ratio_of_durations((1, 1))

        ::

            >>> z(result)
            specificationtools.TimespanScopedSingleContextSetExpressionInventory([
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[6, 8]', start_offset=Offset(3, 2)), 
                        Division('[6, 8]', start_offset=Offset(9, 4))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                specificationtools.StartPositionedDivisionPayloadExpression(
                    payload=specificationtools.DivisionList(
                        [Division('[6, 4]', start_offset=Offset(3, 1)), 
                        Division('[6, 4]', start_offset=Offset(9, 2))],
                        start_offset=durationtools.Offset(3, 1)
                        ),
                    start_offset=durationtools.Offset(3, 1)
                    )
                ])

        Operate in place and return newly constructed inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio_of_durations(self, ratio)

    def reflect(self):
        '''Reflect start-positioned division payload expression about axis.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.reflect()    

        ::

            >>> z(payload_expression)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[3, 4]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4)), 
                    Division('[6, 8]', start_offset=Offset(3, 2))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Operate in place and return division payload expression.
        '''
        return StartPositionedPayloadExpression.reflect(self)

    def repeat_to_duration(self, duration):
        '''Repeat start-positioned division payload expression to `duration`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.repeat_to_duration(Duration(13, 4))    

        ::

            >>> z(result)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4)), 
                    Division('[3, 4]', start_offset=Offset(3, 2)), 
                    Division('[6, 8]', start_offset=Offset(9, 4)), 
                    Division('[2, 8]', start_offset=Offset(3, 1))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Return newly constructed start-positioned division payload expression.
        '''
        divisions = sequencetools.repeat_sequence_to_weight_exactly(self.payload, duration)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    def repeat_to_length(self, length):
        '''Repeat start-positioned division payload expression to `length`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.repeat_to_length(5)

        ::

            >>> z(result)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4)), 
                    Division('[3, 4]', start_offset=Offset(3, 2)), 
                    Division('[6, 8]', start_offset=Offset(9, 4)), 
                    Division('[6, 8]', start_offset=Offset(3, 1))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Return newly constructed start-positioned division payload expression.
        '''
        divisions = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    def rotate(self, rotation):
        '''Rotate start-positioned division payload expression by `rotation`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.rotate(-1)    

        ::

            >>> z(payload_expression)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[3, 4]', start_offset=Offset(3, 4)), 
                    Division('[6, 8]', start_offset=Offset(3, 2))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )
        
        Operate in place and return division payload expression.
        '''
        return StartPositionedPayloadExpression.rotate(self, rotation)

    def translate(self, translation):
        '''Translate division payload expression by `translation`.
        
        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> payload_expression = specificationtools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = payload_expression.translate(10)

        ::

            >>> z(result)
            specificationtools.StartPositionedDivisionPayloadExpression(
                payload=specificationtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(10, 1)), 
                    Division('[6, 8]', start_offset=Offset(43, 4)), 
                    Division('[3, 4]', start_offset=Offset(23, 2))],
                    start_offset=durationtools.Offset(10, 1)
                    ),
                start_offset=durationtools.Offset(10, 1)
                )

        Operate in place and return division payload expression.
        '''
        new_start_offset = self.start_offset + translation
        result = type(self)(self.payload.divisions, voice_name=self.voice_name, start_offset=new_start_offset)
        return result
