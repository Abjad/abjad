import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.RegionProduct import RegionProduct


class DivisionRegionProduct(RegionProduct):
    r'''Division region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> timespan = timespantools.Timespan(0, Infinity)
        >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

    ::

        >>> z(product)
        settingtools.DivisionRegionProduct(
            payload=settingtools.DivisionList(
                [Division('[6, 8]'), Division('[6, 8]'), Division('[3, 4]')]
                ),
            voice_name='Voice 1',
            timespan=timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(9, 4)
                )
            )

    Contiguous block of one voice's divisions.

    Division interpretation generates many division region products.
    
    Division interpretation completes when contiguous division region
    products exist to account for the duration of every voice.

    Division region products may be constructed out of chronological order.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, timespan=None):
        from experimental.tools import settingtools
        payload = settingtools.DivisionList(payload)
        RegionProduct.__init__(self, payload=payload, voice_name=voice_name, timespan=timespan)

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Keep intersection of `timespan` and rhythm region product.

        Example 1. Intersection on the left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product & timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(1, 8)
                        )
                    )
                ])

        Example 2. Intersection on the right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product & timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(17, 8),
                        stop_offset=durationtools.Offset(9, 4)
                        )
                    )
                ])

        Example 3. Trisection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[5, 8]'), Division('[6, 8]'), Division('[5, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(1, 8),
                        stop_offset=durationtools.Offset(17, 8)
                        )
                    )
                ])

        Example 4. No intersection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product & timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
        '''
        return RegionProduct.__and__(self, timespan)

    def __or__(self, expr):
        '''Logical OR of two division region products:

        ::

            >>> region_product_1 = settingtools.DivisionRegionProduct(2 * [(3, 16)], 'Voice 1')
            >>> timespan = timespantools.Timespan(Offset(6, 16))
            >>> region_product_2 = settingtools.DivisionRegionProduct(
            ...     2 * [(2, 16)], 'Voice 1', timespan=timespan)

        ::

            >>> region_product_1.timespan.stops_when_timespan_starts(region_product_2)
            True

        ::

            >>> result = region_product_1 | region_product_2

        ::
        
            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[3, 16]'), Division('[3, 16]'), Division('[2, 16]'), Division('[2, 16]')]
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 8)
                        )
                    )
                ])

        Return timespan inventory.
        '''
        return RegionProduct.__or__(self, expr)

    def __sub__(self, timespan):
        '''Subtract `timespan` from division region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[5, 8]'), Division('[6, 8]'), Division('[3, 4]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(1, 8),
                        stop_offset=durationtools.Offset(9, 4)
                        )
                    )
                ])

        Example 2. Subtract from right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]'), Division('[6, 8]'), Division('[5, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(17, 8)
                        )
                    )
                ])

        Example 3. Subtract from middle:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(1, 8)
                        )
                    ),
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[1, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(17, 8),
                        stop_offset=durationtools.Offset(9, 4)
                        )
                    )
                ])


        Example 4. Subtract from nothing:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]'), Division('[6, 8]'), Division('[3, 4]')]
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(9, 4)
                        )
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        return RegionProduct.__sub__(self, timespan)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _payload_elements(self):
        return self.payload.divisions

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        from experimental.tools import settingtools
        divisions = copy.deepcopy(self.payload.divisions)
        self._payload = settingtools.DivisionList([], voice_name=self.voice_name)
        shards = sequencetools.split_sequence_by_weights(
            divisions, offsets, cyclic=False, overhang=True)
        shards = [settingtools.DivisionList(shard, voice_name=self.voice_name) for shard in shards]
        return shards

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Division region product payload:

        ::

            >>> product.payload
            DivisionList('[6, 8], [6, 8], [3, 4]')

        Return division list.
        '''
        return RegionProduct.payload.fget(self)

    @property
    def start_offset(self):
        '''Division region product start offset:

        ::

            >>> product.start_offset
            Offset(0, 1)

        Return offset.
        '''
        return RegionProduct.start_offset.fget(self)

    @property
    def stop_offset(self):
        '''Division region product stop offset:

        ::

            >>> product.stop_offset
            Offset(9, 4)

        Return offset.
        '''
        return RegionProduct.stop_offset.fget(self)

    @property
    def storage_format(self):
        '''Division region product storage format:

        ::

            >>> z(product)
            settingtools.DivisionRegionProduct(
                payload=settingtools.DivisionList(
                    [Division('[6, 8]'), Division('[6, 8]'), Division('[3, 4]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    )
                )

        Return string.
        '''
        return RegionProduct.storage_format.fget(self)

    @property
    def timespan(self):
        '''Division region product timespan:

        ::

            >>> product.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Return timespan.
        '''
        return RegionProduct.timespan.fget(self)

    @property
    def voice_name(self):
        '''Division region product voice name:

        ::

            >>> product.voice_name
            'Voice 1'

        Return string.
        '''
        return RegionProduct.voice_name.fget(self)
        
    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition divisions by `ratio`:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> timespan = timespantools.Timespan(0, Infinity)
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.partition_by_ratio((1, 1))

        ::

            >>> z(result)
            settingtools.RegionCommandInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]'), Division('[6, 8]'), Division('[6, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(9, 4)
                        )
                    ),
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]'), Division('[6, 4]'), Division('[6, 4]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(9, 4),
                        stop_offset=durationtools.Offset(6, 1)
                        )
                    )
                ])

        Operate in place and return newly constructed inventory.
        '''
        return RegionProduct.partition_by_ratio(self, ratio)

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition divisions by `ratio` of durations:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> timespan = timespantools.Timespan(0, Infinity)
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.partition_by_ratio_of_durations((1, 1))

        ::

            >>> z(result)
            settingtools.RegionCommandInventory([
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 8]'), Division('[6, 8]'), Division('[6, 8]'), Division('[6, 8]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1)
                        )
                    ),
                settingtools.DivisionRegionProduct(
                    payload=settingtools.DivisionList(
                        [Division('[6, 4]'), Division('[6, 4]')],
                        voice_name='Voice 1'
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1)
                        )
                    )
                ])

        Operate in place and return newly constructed inventory.
        '''
        return RegionProduct.partition_by_ratio_of_durations(self, ratio)

    def reflect(self):
        '''Reflect divisions about axis:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> timespan = timespantools.Timespan(0, Infinity)
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.reflect()    

        ::

            >>> z(product)
            settingtools.DivisionRegionProduct(
                payload=settingtools.DivisionList(
                    [Division('[3, 4]'), Division('[6, 8]'), Division('[6, 8]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    )
                )

        Operate in place and return division region product.
        '''
        return RegionProduct.reflect(self)

    def rotate(self, rotation):
        '''Rotate divisions by `rotation`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> timespan = timespantools.Timespan(0, Infinity)
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.rotate(-1)    

        ::

            >>> z(product)
            settingtools.DivisionRegionProduct(
                payload=settingtools.DivisionList(
                    [Division('[6, 8]'), Division('[3, 4]'), Division('[6, 8]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    )
                )
        
        .. note:: implement duration rotation.

        Operate in place and return division region product.
        '''
        return RegionProduct.rotate(self, rotation)

    def translate(self, translation):
        '''Translate division region product by `translation`:
        
        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> timespan = timespantools.Timespan(0, Infinity)
            >>> product = settingtools.DivisionRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.translate(10)

        ::

            >>> z(product)
            settingtools.DivisionRegionProduct(
                payload=settingtools.DivisionList(
                    [Division('[6, 8]'), Division('[6, 8]'), Division('[3, 4]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(49, 4)
                    )
                )

        Operate in place and return division region product.
        '''
        return RegionProduct.translate(self, translation)
