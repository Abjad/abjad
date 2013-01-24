import math
from abjad.tools import beamtools
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.StartPositionedPayloadExpression import StartPositionedPayloadExpression


class StartPositionedRhythmPayloadExpression(StartPositionedPayloadExpression):
    r'''Rhythm region product:

    ::

        >>> payload = [Container("c'8 d'8 e'8 f'8")]
        >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(10))

    ::

        >>> z(product)
        settingtools.StartPositionedRhythmPayloadExpression(
            payload=containertools.Container(
                music=({c'8, d'8, e'8, f'8},)
                ),
            start_offset=durationtools.Offset(10, 1)
            )

    Contiguous block of one voice's counttime components.

    Rhythm interpretation generates many rhythm region products.

    Rhythm interpretation completes when contiguous rhythm region
    products exist to account for the duration of every voice.

    Rhythm region products may be constructed out of chronological order.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        payload = containertools.Container(music=payload)
        StartPositionedPayloadExpression.__init__(self, 
            payload=payload, start_offset=start_offset, voice_name=voice_name)

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Intersection of `timespan` and rhythm region product.

        Example 1. Intersection on the left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(Offset(-1, 8), Offset(3, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8},)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Example 2. Intersection on the right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(5, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({d'8, e'8, f'8},)
                        ),
                    start_offset=durationtools.Offset(1, 8)
                    )
                ])

        Example 3. Trisection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(Offset(1, 8), Offset(3, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({d'8, e'8},)
                        ),
                    start_offset=durationtools.Offset(1, 8)
                    )
                ])

        Example 4. No intersection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product & timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__and__(self, timespan)

    def __copy__(self, *args):
        new = type(self)(voice_name=self.voice_name, start_offset=self.start_offset)
        # TODO: use copy.deepcopy() instead (once Component.__deepcopy__ is unaliased)
        new._payload = componenttools.copy_components_and_covered_spanners([self.payload])[0]
        return new

    __deepcopy__ = __copy__

    def __getitem__(self, expr):
        assert isinstance(expr, slice), repr(expr)
        leaves = self.payload.leaves.__getitem__(expr)
        start_offset = leaves[0].start_offset
        stop_offset = leaves[-1].stop_offset
        timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = timespan.translate(self.start_offset)
        result = self & timespan
        assert len(result) == 1, repr(result)
        result = result[0]
        return result

    def __len__(self): 
        '''Defined equal to number of leaves in payload.
    
        Return nonnegative integer.
        '''
        return len(self.payload.leaves)

    def __or__(self, expr):
        '''Logical OR of two rhythm region products:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product_1 = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> payload = [Container("g'8 a'8 b'8 c''8")]
            >>> product_2 = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(4, 8))

        ::

            >>> product_1.timespan.stops_when_timespan_starts(product_2)
            True

        ::

            >>> result = product_1 | product_2

        ::
        
            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8, f'8, g'8, a'8, b'8, c''8},)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Leave rhythm region product unchanged:

        ::

            >>> z(product_1)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8},)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Leave `expr` unchanged:

        ::

            >>> z(product_2)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({g'8, a'8, b'8, c''8},)
                    ),
                start_offset=durationtools.Offset(1, 2)
                )

        Return region command inventory.
        '''
        return StartPositionedPayloadExpression.__or__(self, expr)

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(0, Offset(1, 8))

        ::

                >>> z(result)
                timespantools.TimespanInventory([
                    settingtools.StartPositionedRhythmPayloadExpression(
                        payload=containertools.Container(
                            music=({d'8, e'8, f'8},)
                            ),
                        start_offset=durationtools.Offset(1, 8)
                        )
                    ])

        Example 2. Subtract from right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(Offset(3, 8), 100)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8},)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Example 3. Subtract from middle:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(Offset(1, 8), Offset(3, 8))

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8},)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    ),
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({f'8},)
                        ),
                    start_offset=durationtools.Offset(3, 8)
                    )
                ])

        Example 4. Subtract nothing:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = product - timespantools.Timespan(100, 200)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8, d'8, e'8, f'8},)
                        ),
                    start_offset=durationtools.Offset(0, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        return StartPositionedPayloadExpression.__sub__(self, timespan)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        return self.payload.prolated_duration

    @property
    def _payload_elements(self):
        return self.payload.leaves

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
        return StartPositionedPayloadExpression.payload.fget(self)

    @property
    def start_offset(self):
        '''Rhythm region product start offset:

        ::

            >>> product.start_offset
            Offset(0, 1)

        Return offset.
        '''
        return StartPositionedPayloadExpression.start_offset.fget(self)

    @property
    def stop_offset(self):
        '''Rhythm region product stop offset:

        ::

            >>> product.stop_offset
            Offset(1, 2)

        Return offset.
        '''
        return StartPositionedPayloadExpression.stop_offset.fget(self)

    @property
    def storage_format(self):
        '''Rhythm region product storage format:

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8},)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Return string.
        '''
        return StartPositionedPayloadExpression.storage_format.fget(self)

    @property
    def timespan(self):
        '''Rhythm region product timespan:

        ::

            >>> product.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 2))

        Return timespan.
        '''
        return StartPositionedPayloadExpression.timespan.fget(self)

    @property
    def voice_name(self):
        '''Rhythm region product voice name:

        ::

            >>> product.voice_name is None
            True

        Return string.
        '''
        return StartPositionedPayloadExpression.voice_name.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition leaves by `ratio`:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(10))

        ::

            >>> result = product.partition_by_ratio((1, 2, 1))

        ::

            >>> z(result)
            settingtools.RegionExpressionInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'8},)
                        ),
                    start_offset=durationtools.Offset(10, 1)
                    ),
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({d'8, e'8},)
                        ),
                    start_offset=durationtools.Offset(81, 8)
                    ),
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({f'8},)
                        ),
                    start_offset=durationtools.Offset(83, 8)
                    )
                ])

        Operate in place and return newly constructed region command inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio(self, ratio)

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition leaves by `ratio` of durations:

        ::

            >>> payload = [Container("c'2 d'8 e'8 f'4")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(10))

        ::

            >>> result = product.partition_by_ratio_of_durations((1, 1))

        ::

            >>> z(result)
            settingtools.RegionExpressionInventory([
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({c'2},)
                        ),
                    start_offset=durationtools.Offset(10, 1)
                    ),
                settingtools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=({d'8, e'8, f'4},)
                        ),
                    start_offset=durationtools.Offset(21, 2)
                    )
                ])

        Operate in place and return newly constructed region command inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio_of_durations(self, ratio)

    def reflect(self):
        '''Reflect rhythm about axis:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.reflect()    

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({f'8, e'8, d'8, c'8},)
                    ),
                start_offset=durationtools.Offset(0, 1)
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

        Example 1. Repeat to duration less than rhythm region product:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.repeat_to_duration(Duration(5, 16))

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'16},)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Example 2. Repeat to duration greater than rhythm region product:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.repeat_to_duration(Duration(13, 16))

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8}, {c'8, d'8, e'16})
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

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
        '''Repeat to leaf `length`.

        Example 1. Repeat to `length` less than rhythm region product:
    
        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.repeat_to_length(3)

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8},)
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Example 2. Repeat to `length` greater than rhythm region product:
    
        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.repeat_to_length(7)

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8}, {c'8, d'8, e'8})
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

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
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.repeat_to_stop_offset(Offset(17, 16))    

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8}, {c'8, d'8, e'8, f'8}, {c'16})
                    ),
                start_offset=durationtools.Offset(0, 1)
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
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.rotate(-1)

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({d'8, e'8, f'8}, {c'8})
                    ),
                start_offset=durationtools.Offset(0, 1)
                )

        Example 2. Rotate by duration:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.rotate(-Duration(3, 16))

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({d'16, e'8, f'8}, {c'8, d'16})
                    ),
                start_offset=durationtools.Offset(0, 1)
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

    def translate(self, translation):
        '''Translate rhythm region product by `translation`:
        
        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.StartPositionedRhythmPayloadExpression(payload, Offset(0))

        ::

            >>> result = product.translate(10)

        ::

            >>> z(product)
            settingtools.StartPositionedRhythmPayloadExpression(
                payload=containertools.Container(
                    music=({c'8, d'8, e'8, f'8},)
                    ),
                start_offset=durationtools.Offset(10, 1)
                )

        Operate in place and return rhythm region product.
        '''
        return StartPositionedPayloadExpression.translate(self, translation)
