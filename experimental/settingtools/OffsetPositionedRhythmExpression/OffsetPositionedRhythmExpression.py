import math
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import spannertools
from experimental.settingtools.OffsetPositionedExpression import OffsetPositionedExpression


class OffsetPositionedRhythmExpression(OffsetPositionedExpression):
    r'''.. versionadded:: 1.0

    Offset-positioned rhythm expression.

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
        OffsetPositionedExpression.__init__(
            self, voice_name, start_offset=start_offset, stop_offset=stop_offset)
        music = containertools.Container(music=music)
        self._music = music

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = type(self)(voice_name=self.voice_name, start_offset=self.start_offset)
        new._music = componenttools.copy_components_and_covered_spanners([self.music])[0]
        return new

    __deepcopy__ = __copy__

    def __len__(self):
        '''Defined equal to number of leaves in ``self.music``.
    
        Return nonnegative integer.
        '''
        return len(self.music.leaves)

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
        self.trim_to_stop_offset(stop_offset)

    def reverse(self):
        '''Reverse rhythm.

        .. note:: add example.

        Operate in place and return none.
        '''
        for container in iterationtools.iterate_containers_in_expr(self.music):
            container._music.reverse()
        for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.music):
            spanner._reverse_components()

    def rotate(self, n):
        '''Rotate rhythm.

        .. note:: add example.

        Operate in place and return none.
        '''
        if 0 <= n:
            split_offset = self.music.leaves[-n].start_offset
        else:
            split_offset = self.music.leaves[-(n+1)].stop_offset
        result = componenttools.split_components_at_offsets(
            [self.music], [split_offset], cyclic=False, fracture_spanners=True)
        left_half, right_half = result[0][0], result[-1][0]
        music = containertools.Container()
        music.extend(right_half)
        music.extend(left_half)
        assert componenttools.is_well_formed_component(music)
        self._music = music

    def trim_to_start_offset(self, start_offset):
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
        assert componenttools.is_well_formed_component(trimmed_music)
        self._music = trimmed_music
        self._start_offset = start_offset

    def trim_to_stop_offset(self, stop_offset):
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
        if not componenttools.is_well_formed_component(trimmed_music):
            self._debug(trimmed_music, 'trimmed music')
            componenttools.tabulate_well_formedness_violations_in_expr(trimmed_music)
        assert componenttools.is_well_formed_component(trimmed_music)
        self._music = trimmed_music
