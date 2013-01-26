import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.settingtools.StartPositionedPayloadExpression import StartPositionedPayloadExpression


class StartPositionedDivisionPayloadExpression(StartPositionedPayloadExpression):
    r'''Division region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

    ::

        >>> z(product)
        settingtools.StartPositionedDivisionPayloadExpression(
            payload=settingtools.DivisionList(
                [Division('[6, 8]', start_offset=Offset(0, 1)), 
                Division('[6, 8]', start_offset=Offset(3, 4)), 
                Division('[3, 4]', start_offset=Offset(3, 2))],
                start_offset=durationtools.Offset(0, 1)
                ),
            start_offset=durationtools.Offset(0, 1)
            )

    Contiguous block of one voice's divisions.

    Division interpretation generates many division region products.
    
    Division interpretation completes when contiguous division region
    products exist to account for the duration of every voice.

    Division region products may be constructed out of chronological order.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        from experimental.tools import settingtools
        payload = settingtools.DivisionList(payload, start_offset=start_offset, voice_name=voice_name)
        StartPositionedPayloadExpression.__init__(self, 
            payload=payload, start_offset=start_offset, voice_name=voice_name) 

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Keep intersection of `timespan` and rhythm region product.

        Example 1. Intersection on the left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(0, 1))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Example 2. Intersection on the right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(17, 8))],
                        start_offset=durationtools.Offset(17, 8)
                        ),
                    start_offset=durationtools.Offset(17, 8)
                    )
                ])

        Example 3. Trisection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__and__(self, timespan)

    def __getitem__(self, expr):
        assert isinstance(expr, slice), repr(expr)
        divisions = self.payload.__getitem__(expr)
        if divisions:
            start_offset = divisions[0].start_offset
        else:
            start_offset = durationtools.Offset(0)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=start_offset)
        return result

    def __or__(self, expr):
        '''Logical OR of two division region products:

        ::

            >>> product_1 = settingtools.StartPositionedDivisionPayloadExpression(2 * [(3, 16)], Offset(0))
            >>> timespan = timespantools.Timespan(Offset(6, 16))
            >>> product_2 = settingtools.StartPositionedDivisionPayloadExpression(2 * [(2, 16)], Offset(6, 16))

        ::

            >>> product_1.timespan.stops_when_timespan_starts(product_2)
            True

        ::

            >>> result = product_1 | product_2

        ::
        
            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
        '''Subtract `timespan` from division region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(0, 1))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]', start_offset=Offset(17, 8))],
                        start_offset=durationtools.Offset(17, 8)
                        ),
                    start_offset=durationtools.Offset(17, 8)
                    )
                ])


        Example 4. Subtract from nothing:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def elements(self):
        return self.payload.divisions

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        from experimental.tools import settingtools
        divisions = copy.deepcopy(self.payload.divisions)
        self._payload = settingtools.DivisionList([], voice_name=self.voice_name, start_offset=self.start_offset)
        shards = sequencetools.split_sequence_by_weights(
            divisions, offsets, cyclic=False, overhang=True)
        result, total_duration = [], durationtools.Duration(0)
        for shard in shards:
            shard = settingtools.DivisionList(shard, voice_name=self.voice_name, start_offset=total_duration)
            result.append(shard)
            total_duration += shard.duration
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Division region product payload:

        ::

            >>> product.payload
            DivisionList('[6, 8], [6, 8], [3, 4]')

        Return division list.
        '''
        return StartPositionedPayloadExpression.payload.fget(self)

    @property
    def start_offset(self):
        '''Division region product start offset:

        ::

            >>> product.start_offset
            Offset(0, 1)

        Return offset.
        '''
        return StartPositionedPayloadExpression.start_offset.fget(self)

    @property
    def stop_offset(self):
        '''Division region product stop offset:

        ::

            >>> product.stop_offset
            Offset(9, 4)

        Return offset.
        '''
        return StartPositionedPayloadExpression.stop_offset.fget(self)

    @property
    def storage_format(self):
        '''Division region product storage format:

        ::

            >>> z(product)
            settingtools.StartPositionedDivisionPayloadExpression(
                payload=settingtools.DivisionList(
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
        '''Division region product timespan:

        ::

            >>> product.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Return timespan.
        '''
        return StartPositionedPayloadExpression.timespan.fget(self)

    @property
    def voice_name(self):
        '''Division region product voice name:

        ::

            >>> product.voice_name is None
            True

        Return string.
        '''
        return StartPositionedPayloadExpression.voice_name.fget(self)
        
    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition divisions by `ratio`:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.partition_by_ratio((1, 1))

        ::

            >>> z(result)
            settingtools.TimespanScopedSingleContextSettingInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[6, 8]', start_offset=Offset(3, 2))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
        '''Partition divisions by `ratio` of durations:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.partition_by_ratio_of_durations((1, 1))

        ::

            >>> z(result)
            settingtools.TimespanScopedSingleContextSettingInventory([
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]', start_offset=Offset(0, 1)), 
                        Division('[6, 8]', start_offset=Offset(3, 4)), 
                        Division('[6, 8]', start_offset=Offset(3, 2)), 
                        Division('[6, 8]', start_offset=Offset(9, 4))],
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                settingtools.StartPositionedDivisionPayloadExpression(
                    payload=settingtools.DivisionList(
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
        '''Reflect divisions about axis:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.reflect()    

        ::

            >>> z(product)
            settingtools.StartPositionedDivisionPayloadExpression(
                payload=settingtools.DivisionList(
                    [Division('[3, 4]', start_offset=Offset(0, 1)), 
                    Division('[6, 8]', start_offset=Offset(3, 4)), 
                    Division('[6, 8]', start_offset=Offset(3, 2))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Operate in place and return division region product.
        '''
        return StartPositionedPayloadExpression.reflect(self)

    # TODO: add example
    def repeat_to_duration(self, duration):
        divisions = sequencetools.repeat_sequence_to_weight_exactly(self.payload, duration)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    # TODO: add example
    def repeat_to_length(self, length):
        divisions = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    def rotate(self, rotation):
        '''Rotate divisions by `rotation`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.rotate(-1)    

        ::

            >>> z(product)
            settingtools.StartPositionedDivisionPayloadExpression(
                payload=settingtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(0, 1)), 
                    Division('[3, 4]', start_offset=Offset(3, 4)), 
                    Division('[6, 8]', start_offset=Offset(3, 2))],
                    start_offset=durationtools.Offset(0, 1)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )
        
        Operate in place and return division region product.
        '''
        return StartPositionedPayloadExpression.rotate(self, rotation)

    def translate(self, translation):
        '''Translate division region product by `translation`:
        
        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.StartPositionedDivisionPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.translate(10)

        ::

            >>> z(result)
            settingtools.StartPositionedDivisionPayloadExpression(
                payload=settingtools.DivisionList(
                    [Division('[6, 8]', start_offset=Offset(10, 1)), 
                    Division('[6, 8]', start_offset=Offset(43, 4)), 
                    Division('[3, 4]', start_offset=Offset(23, 2))],
                    start_offset=durationtools.Offset(10, 1)
                    ),
                start_offset=durationtools.Offset(10, 1)
                )

        Operate in place and return division region product.
        '''
        new_start_offset = self.start_offset + translation
        result = type(self)(self.payload.divisions, voice_name=self.voice_name, start_offset=new_start_offset)
        return result
