import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.RegionProduct import RegionProduct


class DivisionRegionProduct(RegionProduct):
    r'''Division region expression.

    Interpreter byproduct.
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

    ### READ-ONLY PRIVATE PROPERTIES ##

    @property
    def _duration(self):
        return self.payload.duration

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
        '''Division region product payload.

        Return division list.
        '''
        return self._payload
        
    ### PUBLIC METHODS ###
    
    def fracture(self, slice_index):
        assert isinstance(slice_index, int)
        left_division_list, right_division_list = self.payload.fracture(slice_index)
        left_result = type(self)(left_division_list, voice_name=self.voice_name, timespan=self.timespan)
        right_result = type(self)(right_division_list, voice_name=self.voice_name, timespan=self.timespan)
        return left_result, right_result

    def reflect(self):
        self.payload.reflect()

    # TODO: remove code duplicated from Timespan
    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        new_start_offset = self.timespan.start_offset + start_offset_translation
        new_stop_offset = self.timespan.stop_offset + stop_offset_translation
        divisions = copy.copy(self.payload.divisions)
        timespan = timespantools.Timespan(new_start_offset, new_stop_offset)
        result = type(self)(divisions, voice_name=self.voice_name, timespan=timespan)
        return result
