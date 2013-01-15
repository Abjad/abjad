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
    r'''Rhythm region product:

    ::

        >>> payload = [Container("c'8 d'8 e'8 f'8")]
        >>> timespan = timespantools.Timespan(Offset(10), None)
        >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)

    ::

        >>> z(product)
        settingtools.RhythmRegionProduct(
            payload=containertools.Container(
                music=({c'8, d'8, e'8, f'8},)
                ),
            voice_name='Voice 1',
            timespan=timespantools.Timespan(
                start_offset=durationtools.Offset(10, 1),
                stop_offset=durationtools.Offset(21, 2)
                )
            )

    Contiguous block of counttime components specified by voice.

    The interpretive process of building up the rhythm for a complete
    voice involves the generation of many different rhythm region products.
    Voice rhythm interpretation completes when contiguous rhythm region 
    products exist to account for the duration of the voice.

    The rhythm region products that together constitute the rhythm 
    of a voice may not be constructed in chronological order 
    during interpretation.

    Interpreter byproduct.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, timespan=None):
        payload = containertools.Container(music=payload)
        RegionProduct.__init__(self, payload=payload, voice_name=voice_name, timespan=timespan)

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Intersection of `timespan` and rhythm region product.

        Example 1. Intersection on the left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
            >>> result = product & timespantools.Timespan(Offset(-1, 8), Offset(3, 8))

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

        Example 2. Intersection on the right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(5, 8))

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

        Example 3. Trisection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(3, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.RhythmRegionProduct(
                    payload=containertools.Container(
                        music=({d'8, e'8},)
                        ),
                    voice_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(1, 8),
                        stop_offset=durationtools.Offset(3, 8)
                        )
                    )
                ])

        Example 4. No intersection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
            >>> result = product & timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
        '''
        return RegionProduct.__and__(self, timespan)

    def __copy__(self, *args):
        new = type(self)(voice_name=self.voice_name, timespan=self.timespan)
        # TODO: use copy.deepcopy() instead (once Component.__deepcopy__ is unaliased)
        new._payload = componenttools.copy_components_and_covered_spanners([self.payload])[0]
        return new

    __deepcopy__ = __copy__

    def _getitem(self, expr):
        assert isinstance(expr, slice), repr(expr)
        leaves = self.payload.leaves.__getitem__(expr)
        start_offset = leaves[0].start_offset
        stop_offset = leaves[-1].stop_offset
        timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = timespan.translate(self.start_offset)
        result = self & timespan
        assert len(result) == 1, repr(result)
        result = result[0]
        result = result.translate(-start_offset)
        return result

    def __len__(self): 
        '''Defined equal to number of leaves in payload.
    
        Return nonnegative integer.
        '''
        return len(self.payload.leaves)

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
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
                >>> timespan = timespantools.Timespan(0, None)
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
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
                >>> timespan = timespantools.Timespan(0, None)
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
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
                >>> timespan = timespantools.Timespan(0, None)
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)
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
        return RegionProduct.__sub__(self, timespan)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        return self.payload.prolated_duration

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        assert isinstance(self.payload, containertools.Container)
        music = self.payload
        self._payload = containertools.Container()
        shards = componenttools.split_components_at_offsets(
            [music], offsets, cyclic=False, fracture_spanners=True)
        shards = [shard[0] for shard in shards]
        for shard in shards:
            if not wellformednesstools.is_well_formed_component(shard):
                wellformednesstools.tabulate_well_formedness_violations_in_expr(shard)
        return shards

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Rhythm region product payload:

        ::

            >>> product.payload
            {{c'8, d'8, e'8, f'8}}

        Return container.
        '''
        return self._payload

    ### PUBLIC METHODS ###

    def reflect(self):
        '''Reflect rhythm about rhythm region product axis:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.reflect()    

        ::

            >>> z(product)
            settingtools.RhythmRegionProduct(
                payload=containertools.Container(
                    music=({f'8, e'8, d'8, c'8},)
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(1, 2)
                    )
                )

        Operate in place and return rhythm region product.
        '''
        for container in iterationtools.iterate_containers_in_expr(self.payload):
            container._music.reverse()
        for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.payload):
            spanner._reverse_components()
        return self

    def repeat_to_duration(self, duration):
        '''Repeat to `duration`.

        .. note:: add example.
        
        Operate in place and return rhythm region product.
        '''
        if self.timespan.duration < duration:
            stop_offset = self.start_offset + duration
            return self.repeat_to_stop_offset(stop_offset)
        elif duration < self.timespan.duration:
            stop_offset = self.start_offset + duration
            timespan = timespantools.Timespan(self.start_offset, stop_offset)
            result = self & timespan
            assert len(result) == 1, repr(result)
            result = result[0]
            return result
        elif self.timespan.duration == duration:
            return self

    def repeat_to_length(self, length):
        '''Repeat to `length` of leaves.

        .. note:: add example.
        
        Operate in place and return rhythm region product.
        '''
        leaves = sequencetools.CyclicTuple(self.payload.leaves)
        leaves = leaves[:length]
        duration = sum([leaf.prolated_duration for leaf in leaves])
        return self.repeat_to_duration(duration)

    def repeat_to_stop_offset(self, stop_offset):
        '''Repeat rhythm region product to `stop_offset`:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.repeat_to_stop_offset(Offset(17, 16))    

        ::

            >>> z(product)
            settingtools.RhythmRegionProduct(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8}, {c'8, d'8, e'8, f'8}, {c'16})
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(17, 16)
                    )
                )

        Operate in place and return rhythm region product.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset, repr((self.stop_offset, stop_offset))
        additional_duration = stop_offset - self.stop_offset
        needed_copies = int(math.ceil(additional_duration / self.payload.prolated_duration))
        copies = []
        for i in range(needed_copies):
            copies.append(componenttools.copy_components_and_covered_spanners([self.payload])[0])
        for element in copies:
            self.payload.extend(element)
        assert stop_offset <= self.stop_offset
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        assert self.start_offset < stop_offset
        duration_to_trim = self.stop_offset - stop_offset
        duration_to_keep = self.payload.prolated_duration - duration_to_trim
        shards = self._split_payload_at_offsets([duration_to_keep])
        assert len(shards) in (1, 2), repr(shards)
        self._payload = shards[0]
        return self

    def rotate(self, n, fracture_spanners=True):
        '''Rotate rhythm region product payload.

        Example 1. Rotate by count:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.rotate(-1)

        ::

            >>> z(product)
            settingtools.RhythmRegionProduct(
                payload=containertools.Container(
                    music=({d'8, e'8, f'8}, {c'8})
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(1, 2)
                    )
                )

        Example 2. Rotate by duration:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> timespan = timespantools.Timespan(0, None)
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespan)

        ::

            >>> result = product.rotate(-Duration(3, 16))

        ::

            >>> z(product)
            settingtools.RhythmRegionProduct(
                payload=containertools.Container(
                    music=({d'16, e'8, f'8}, {c'8, d'16})
                    ),
                voice_name='Voice 1',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(1, 2)
                    )
                )

        Operate in place and return rhythm region product.
        '''
        from experimental.tools import settingtools
        if isinstance(n, int):
            leaves = sequencetools.CyclicTuple(self.payload.leaves)
            if 0 < n:
                split_offset = leaves[-n].start_offset
            elif n == 0:
                return self
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
                    return self
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
            return self
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
        return self
