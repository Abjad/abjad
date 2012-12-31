import math
from abjad.tools import beamtools
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.RegionExpression import RegionExpression


class RhythmRegionExpression(RegionExpression):
    r'''Offset-positioned rhythm expression.

    One voice of counttime components. 
    Counttime components are tuplets, notes, rests and chords.

    The interpretive process of building up the rhythm for a complete
    voice of music involves the generation of many different rhythm expressions.
    The rhythmic interpretation of a voice completes when enough    
    contiguous rhythm expressions exist to account for the entire
    duration of the voice.

    The many different rhythm expressions that together constitute the
    rhythm of a voice may not necessarily be constructed in
    chronological order during interpretation.

    Initializing ``start_offset=None`` will set `start_offset` to
    ``Offset(0)``.
    
    Composers do not create rhythm expression objects because 
    rhythm expressions arise as a byproduct of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None, voice_name=None, start_offset=None, stop_offset=None):
        RegionExpression.__init__(
            self, voice_name, start_offset=start_offset, stop_offset=stop_offset)
        music = containertools.Container(music=music)
        self._music = music

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = type(self)(voice_name=self.voice_name, start_offset=self.start_offset)
        new._music = componenttools.copy_components_and_covered_spanners([self.music])[0]
        return new

    __deepcopy__ = __copy__

    def __getitem__(self, expr):
        # it's possible that music deepcopy will be required.
        # try returning references first and see if it causes problems.
        return self.music.__getitem__(expr)

    def __len__(self): 
        '''Defined equal to number of leaves in ``self.music``.
    
        Return nonnegative integer.
        '''
        return len(self.music.leaves)

    ### PRIVATE METHODS ###

    def _set_start_offset(self, start_offset):
        '''Trim to start offset.

        .. note:: add example.
        
        Adjust start offset.
        
        Operate in place and return none.
        '''
        start_offset = durationtools.Offset(start_offset)
        assert self.start_offset <= start_offset
        duration_to_trim = start_offset - self.start_offset
        result = componenttools.split_components_at_offsets(
            [self.music], [duration_to_trim], cyclic=False, fracture_spanners=True)
        trimmed_music = result[-1][0]
        assert wellformednesstools.is_well_formed_component(trimmed_music)
        self._music = trimmed_music
        self._start_offset = start_offset

    def _set_stop_offset(self, stop_offset):
        '''Trim to stop offset.

        .. note:: add example.

        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        duration_to_trim = self.stop_offset - stop_offset
        duration_to_keep = self.music.prolated_duration - duration_to_trim
        result = componenttools.split_components_at_offsets(
            [self.music], [duration_to_keep], cyclic=False, fracture_spanners=True)
        trimmed_music = result[0][0]
        if not wellformednesstools.is_well_formed_component(trimmed_music):
            self._debug(trimmed_music, 'trimmed music')
            wellformednesstools.tabulate_well_formedness_violations_in_expr(trimmed_music)
        assert wellformednesstools.is_well_formed_component(trimmed_music)
        self._music = trimmed_music

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Duration of rhythm expression.

        Return duration.
        '''
        return self.music.prolated_duration

    @property
    def music(self):
        '''Offset-positioned rhythm expression music.

        Return container.
        '''
        return self._music

    ### PUBLIC METHODS ###

    def repeat_to_stop_offset(self, stop_offset):
        '''Repeat rhythm to `stop_offset`.

        .. note:: add example.

        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        additional_duration = stop_offset - self.stop_offset
        needed_copies = int(math.ceil(additional_duration / self.music.prolated_duration))
        copies = []
        for i in range(needed_copies):
            copies.append(componenttools.copy_components_and_covered_spanners([self.music])[0])
        for element in copies:
            self.music.extend(element)
        assert stop_offset <= self.stop_offset
        self._set_stop_offset(stop_offset)

    def reverse(self):
        '''Reverse rhythm.

        .. note:: add example.

        Operate in place and return none.
        '''
        for container in iterationtools.iterate_containers_in_expr(self.music):
            container._music.reverse()
        for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.music):
            spanner._reverse_components()

    def rotate(self, n, fracture_spanners=True):
        '''Rotate rhythm.

        .. note:: add example.

        .. note:: extend method in several ways; check todo file.

        Operate in place and return none.
        '''
        from experimental.tools import settingtools
        if isinstance(n, int):
            leaves = sequencetools.CyclicTuple(self.music.leaves)
            if 0 < n:
                split_offset = leaves[-n].start_offset
            elif n == 0:
                return
            else:
                split_offset = leaves[-(n+1)].stop_offset
        elif isinstance(n, settingtools.RotationIndicator):
            rotation_indicator = n
            if rotation_indicator.level is None:
                components_at_level = self.music.leaves
            else:
                components_at_level = []
                for component in iterationtools.iterate_components_in_expr(self.music):
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
                    split_offset = self.music.prolated_duration - index
                else:
                    split_offset = abs(index)
            if rotation_indicator.fracture_spanners is not None:
                fracture_spanners = rotation_indicator.fracture_spanners
        else:
            n = durationtools.Duration(n)
            if 0 <= n:
                split_offset = self.music.prolated_duration - n
            else:
                split_offset = abs(n)
        #self._debug(split_offset, 'split offset')
        if split_offset == self.music.prolated_duration:
            return
        if fracture_spanners:
            result = componenttools.split_components_at_offsets(
                [self.music], [split_offset], cyclic=False, fracture_spanners=True, tie_split_notes=False)
            left_half, right_half = result[0][0], result[-1][0]
            music = containertools.Container()
            music.extend(right_half)
            music.extend(left_half)
            assert wellformednesstools.is_well_formed_component(music)
            self._music = music
        else:
            result = componenttools.split_components_at_offsets(
                self.music[:], [split_offset], cyclic=False, fracture_spanners=False, tie_split_notes=False)
            left_half, right_half = result[0], result[-1]
            for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(
                self.music, klass=beamtools.DuratedComplexBeamSpanner):
                if left_half[-1] in spanner and right_half[0] in spanner:
                    leaf_right_of_split = right_half[0]
                    split_offset_in_beam = spanner._duration_offset_in_me(leaf_right_of_split)
                    left_durations, right_durations = sequencetools.split_sequence_by_weights(
                        spanner.durations, [split_offset_in_beam], cyclic=False, overhang=True)
                    new_durations = right_durations + left_durations
                    spanner._durations = new_durations
            new_music = right_half + left_half
            self.music._music = new_music
            for component in new_music:
                component._mark_entire_score_tree_for_later_update('prolated')
            for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.music):
                spanner._components.sort(lambda x, y: cmp(x.parentage.score_index, y.parentage.score_index))
            assert wellformednesstools.is_well_formed_component(self.music)
