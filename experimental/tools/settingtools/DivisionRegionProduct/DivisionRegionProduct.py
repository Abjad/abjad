import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools import divisiontools
from experimental.tools.settingtools.RegionProduct import RegionProduct


class DivisionRegionProduct(RegionProduct):
    r'''Division region expression.

    Interpreter byproduct.
    '''

    ### INITIALIZER ###

    def __init__(self, payload, voice_name=None, timespan=None):
        RegionProduct.__init__(self, voice_name, timespan=timespan)
        if not isinstance(payload, divisiontools.DivisionList):
            payload = divisiontools.DivisionList(payload)
        self._payload = payload

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.payload)

    ### READ-ONLY PRIVATE PROPERTIES ##

    @property
    def _duration(self):
        return self.payload.duration

    ### PRIVATE METHODS ###

    def _set_start_offset(self, start_offset):
        '''Set start offset.

        ::

            >>> expr = settingtools.DivisionRegionProduct(4 * [(3, 16)], 'Voice 1')

        ::

            >>> z(expr)
            settingtools.DivisionRegionProduct(
                divisiontools.DivisionList(
                    [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(3, 4)
                    )
                )

        ::

            >>> expr.set_offsets(start_offset=(1, 16))

        ::

            >>> z(expr)
            settingtools.DivisionRegionProduct(
                divisiontools.DivisionList(
                    [Division('[2, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(1, 16),
                    stop_offset=durationtools.Offset(3, 4)
                    )
                )

        ::

            >>> expr.timespan.duration
            Duration(11, 16)

        Set start offset.
        
        Operate in place and return none.
        '''
        start_offset = durationtools.Offset(start_offset)
        assert self.timespan.start_offset <= start_offset
        duration_to_trim = start_offset - self.timespan.start_offset
        divisions = copy.deepcopy(self.payload.divisions)
        shards = sequencetools.split_sequence_by_weights(
            divisions, [duration_to_trim], cyclic=False, overhang=True)
        trimmed_divisions = shards[-1]
        division_list = divisiontools.DivisionList(trimmed_divisions)
        self._payload = division_list
        self._start_offset = start_offset

    def _set_stop_offset(self, stop_offset):
        '''Set stop offset.

        ::

            >>> expr = settingtools.DivisionRegionProduct(4 * [(3, 16)], 'Voice 1')

        ::

            >>> z(expr)
            settingtools.DivisionRegionProduct(
                divisiontools.DivisionList(
                    [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(3, 4)
                    )
                )

        ::

            >>> expr.set_offsets(stop_offset=(11, 16))

        ::

            >>> z(expr)
            settingtools.DivisionRegionProduct(
                divisiontools.DivisionList(
                    [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[2, 16]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(11, 16)
                    )
                )

        ::

            >>> expr.timespan.duration
            Duration(11, 16)

        Set stop offset.
        
        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.timespan.stop_offset
        duration_to_trim = self.timespan.stop_offset - stop_offset
        duration_to_keep = self.payload.duration - duration_to_trim
        divisions = copy.deepcopy(self.payload.divisions)
        shards = sequencetools.split_sequence_by_weights(
            divisions, [duration_to_keep], cyclic=False, overhang=True)
        trimmed_divisions = shards[0]
        division_list = divisiontools.DivisionList(trimmed_divisions)
        self._payload = division_list

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

    def fuse(self, expr):
        '''Fuse if expression stops when `expr` starts::

            >>> expr_1 = settingtools.DivisionRegionProduct(2 * [(3, 16)], 'Voice 1')
            >>> timespan = timespantools.Timespan(Offset(6, 16))
            >>> expr_2 = settingtools.DivisionRegionProduct(
            ...     2 * [(2, 16)], 'Voice 1', timespan=timespan)

        ::

            >>> expr_1.timespan.stops_when_timespan_starts(expr_2)
            True

        ::

            >>> new_expr = expr_1.fuse(expr_2)

        ::
        
            >>> z(new_expr)
            settingtools.DivisionRegionProduct(
                divisiontools.DivisionList(
                    [Division('[3, 16]'), Division('[3, 16]'), Division('[2, 16]'), Division('[2, 16]')]
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 8)
                    )
                )

        Return newly constructed expression.
        '''
        assert self.can_fuse(expr)
        division_list = self.payload + expr.payload
        result = type(self)(division_list, voice_name=self.voice_name, timespan=self.timespan)
        return result

    def reverse(self):
        self.payload.reverse()

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
