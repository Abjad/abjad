import math
from abjad.tools import beamtools
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.RegionProduct import RegionProduct


class RhythmRegionProduct(RegionProduct):
    r'''Rhythm region product.

    Contiguous block of counttime components specified by voice.

    The interpretive process of building up the rhythm for a complete
    voice of payload involves the generation of many 
    different rhythm region products.
    The rhythmic interpretation of a voice completes when enough    
    contiguous rhythm region products exist to account for the entire
    duration of the voice.

    The many different rhythm region products that together constitute the
    rhythm of a voice may not necessarily be constructed in
    chronological order during interpretation.

    Interpreter byproduct.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, timespan=None):
        payload = containertools.Container(music=payload)
        RegionProduct.__init__(self, payload=payload, voice_name=voice_name, timespan=timespan)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = type(self)(voice_name=self.voice_name, timespan=self.timespan)
        # TODO: use copy.deepcopy() instead
        new._payload = componenttools.copy_components_and_covered_spanners([self.payload])[0]
        return new

    __deepcopy__ = __copy__

    def __getitem__(self, expr):
        # it's possible that payload deepcopy will be required.
        # try returning references first and see if it causes problems.
        return self.payload.__getitem__(expr)

    def __len__(self): 
        '''Defined equal to number of leaves in ``self.payload``.
    
        Return nonnegative integer.
        '''
        return len(self.payload.leaves)

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({d'8, e'8, f'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(1, 8),
                        stop_offset=durationtools.Offset(1, 2)
                        )
                    )
                ])

        Example 2. Subtract from right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(Offset(3, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 8)
                        )
                    )
                ])

        Example 3. Subtract from middle:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(Offset(1, 8), Offset(3, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({c'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(1, 8)
                        )
                    ),
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({f'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 8),
                        stop_offset=durationtools.Offset(1, 2)
                        )
                    )
                ])

        Example 4. Subtract nothing:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8, f'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(1, 2)
                        )
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        if timespan.delays_timespan(self):
            split_offset = durationtools.Offset(timespan.stop_offset)
            duration_to_trim = split_offset - self.start_offset
            result = componenttools.split_components_at_offsets(
                [self.payload], [duration_to_trim], cyclic=False, fracture_spanners=True)
            trimmed_payload = result[-1][0]
            self._payload = trimmed_payload
            self._start_offset = split_offset
            result = timespantools.TimespanInventory([self])
        elif timespan.curtails_timespan(self):
            split_offset = durationtools.Offset(timespan.start_offset)
            duration_to_trim = self.stop_offset - split_offset
            duration_to_keep = self.payload.prolated_duration - duration_to_trim
            result = componenttools.split_components_at_offsets(
                [self.payload], [duration_to_keep], cyclic=False, fracture_spanners=True)
            trimmed_payload = result[0][0]
            if not wellformednesstools.is_well_formed_component(trimmed_payload):
                self._debug(trimmed_payload, 'trimmed payload')
                wellformednesstools.tabulate_well_formedness_violations_in_expr(trimmed_payload)
            self._payload = trimmed_payload
            result = timespantools.TimespanInventory([self])
        elif timespan.trisects_timespan(self):
            split_offsets = []
            split_offsets.append(timespan.start_offset - self.start_offset)
            split_offsets.append(timespan.duration)
            assert isinstance(self.payload, containertools.Container)
            assert len(self.payload) == 1
            music = self.payload[0]
            self.payload[:] = []
            result = componenttools.split_components_at_offsets(
                [music], split_offsets, cyclic=False, fracture_spanners=True)
            left_payload = result[0][0]
            right_payload = result[-1][0]
            if not wellformednesstools.is_well_formed_component(left_payload):
                wellformednesstools.tabulate_well_formedness_violations_in_expr(left_payload)
            if not wellformednesstools.is_well_formed_component(right_payload):
                wellformednesstools.tabulate_well_formedness_violations_in_expr(right_payload)
            left_timespan = timespantools.Timespan(self.start_offset)
            left_product = type(self)(
                payload=[left_payload], voice_name=self.voice_name, timespan=left_timespan)
            right_timespan = timespantools.Timespan(timespan.stop_offset)
            right_product = type(self)(
                payload=[right_payload], voice_name=self.voice_name, timespan=right_timespan)
            products = [left_product, right_product]
            result = timespantools.TimespanInventory(products)
        else:
            result = timespantools.TimespanInventory([self])
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        return self.payload.prolated_duration

    ### PRIVATE METHODS ###

    def _set_start_offset(self, start_offset):
        '''Set start offset.

        .. note:: add example.
        
        Operate in place and return none.
        '''
        start_offset = durationtools.Offset(start_offset)
        assert self.start_offset <= start_offset
        assert start_offset < self.stop_offset
        duration_to_trim = start_offset - self.start_offset
        result = componenttools.split_components_at_offsets(
            [self.payload], [duration_to_trim], cyclic=False, fracture_spanners=True)
        trimmed_payload = result[-1][0]
        assert wellformednesstools.is_well_formed_component(trimmed_payload)
        self._payload = trimmed_payload
        self._start_offset = start_offset

    def _set_stop_offset(self, stop_offset):
        '''Set stop offset.

        .. note:: add example.

        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        assert self.start_offset < stop_offset
        duration_to_trim = self.stop_offset - stop_offset
        duration_to_keep = self.payload.prolated_duration - duration_to_trim
        result = componenttools.split_components_at_offsets(
            [self.payload], [duration_to_keep], cyclic=False, fracture_spanners=True)
        trimmed_payload = result[0][0]
        if not wellformednesstools.is_well_formed_component(trimmed_payload):
            self._debug(trimmed_payload, 'trimmed payload')
            wellformednesstools.tabulate_well_formedness_violations_in_expr(trimmed_payload)
        assert wellformednesstools.is_well_formed_component(trimmed_payload)
        self._payload = trimmed_payload

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Rhythm region product payload.

        Return container.
        '''
        return self._payload

    ### PUBLIC METHODS ###

    def repeat_to_stop_offset(self, stop_offset):
        '''Repeat rhythm to `stop_offset`.

        .. note:: add example.

        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        additional_duration = stop_offset - self.stop_offset
        needed_copies = int(math.ceil(additional_duration / self.payload.prolated_duration))
        copies = []
        for i in range(needed_copies):
            copies.append(componenttools.copy_components_and_covered_spanners([self.payload])[0])
        for element in copies:
            self.payload.extend(element)
        assert stop_offset <= self.stop_offset
        self._set_stop_offset(stop_offset)

    def reflect(self):
        '''Reverse rhythm.

        .. note:: add example.

        Operate in place and return none.
        '''
        for container in iterationtools.iterate_containers_in_expr(self.payload):
            container._music.reverse()
        for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.payload):
            spanner._reverse_components()

    def rotate(self, n, fracture_spanners=True):
        '''Rotate rhythm.

        .. note:: add example.

        .. note:: extend method in several ways; check todo file.

        Operate in place and return none.
        '''
        from experimental.tools import settingtools
        if isinstance(n, int):
            leaves = sequencetools.CyclicTuple(self.payload.leaves)
            if 0 < n:
                split_offset = leaves[-n].start_offset
            elif n == 0:
                return
            else:
                split_offset = leaves[-(n+1)].stop_offset
        elif isinstance(n, settingtools.RotationIndicator):
            rotation_indicator = n
            if rotation_indicator.level is None:
                components_at_level = self.payload.leaves
            else:
                components_at_level = []
                for component in iterationtools.iterate_components_in_expr(self.payload):
                    score_index = component.parentage.score_index
                    if len(score_index) == rotation_indicator.level:
                        components_at_level.append(component)
            components_at_level = sequencetools.CyclicTuple(components_at_level)
            if isinstance(rotation_indicator.index, int):
                if 0 < rotation_indicator.index:
                    split_offset = components_at_level[-rotation_indicator.index].start_offset
                elif n == 0:
                    return
                else:
                    split_offset = components_at_level[-(rotation_indicator.index+1)].stop_offset
            else:
                index = durationtools.Duration(rotation_indicator.index)
                if 0 <= index:
                    split_offset = self.payload.prolated_duration - index
                else:
                    split_offset = abs(index)
            if rotation_indicator.fracture_spanners is not None:
                fracture_spanners = rotation_indicator.fracture_spanners
        else:
            n = durationtools.Duration(n)
            if 0 <= n:
                split_offset = self.payload.prolated_duration - n
            else:
                split_offset = abs(n)
        #self._debug(split_offset, 'split offset')
        if split_offset == self.payload.prolated_duration:
            return
        if fracture_spanners:
            result = componenttools.split_components_at_offsets(
                [self.payload], [split_offset], cyclic=False, fracture_spanners=True, tie_split_notes=False)
            left_half, right_half = result[0][0], result[-1][0]
            payload = containertools.Container()
            payload.extend(right_half)
            payload.extend(left_half)
            assert wellformednesstools.is_well_formed_component(payload)
            self._payload = payload
        else:
            result = componenttools.split_components_at_offsets(
                self.payload[:], [split_offset], cyclic=False, fracture_spanners=False, tie_split_notes=False)
            left_half, right_half = result[0], result[-1]
            for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(
                self.payload, klass=beamtools.DuratedComplexBeamSpanner):
                if left_half[-1] in spanner and right_half[0] in spanner:
                    leaf_right_of_split = right_half[0]
                    split_offset_in_beam = spanner._duration_offset_in_me(leaf_right_of_split)
                    left_durations, right_durations = sequencetools.split_sequence_by_weights(
                        spanner.durations, [split_offset_in_beam], cyclic=False, overhang=True)
                    new_durations = right_durations + left_durations
                    spanner._durations = new_durations
            new_payload = right_half + left_half
            self.payload._music = new_payload
            for component in new_payload:
                component._mark_entire_score_tree_for_later_update('prolated')
            for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.payload):
                spanner._components.sort(lambda x, y: cmp(x.parentage.score_index, y.parentage.score_index))
            assert wellformednesstools.is_well_formed_component(self.payload)
