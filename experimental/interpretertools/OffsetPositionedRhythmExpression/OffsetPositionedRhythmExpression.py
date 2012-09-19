from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import spannertools
from abjad.tools.abctools.AbjadObject import AbjadObject


class OffsetPositionedRhythmExpression(AbjadObject):
    r'''.. versionadded:: 1.0

    Rhythm expression.

    One voice of counttime components: tuplets, notes, rests and chords.

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

    def __init__(self, music=None, start_offset=None, stop_offset=None):
        music = containertools.Container(music=music)
        self._music = music
        if start_offset is None:
            start_offset = durationtools.Offset(0)
        else:
            start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = type(self)(start_offset=self.start_offset)
        new._music = componenttools.copy_components_and_covered_spanners([self.music])[0]
        return new

    __deepcopy__ = __copy__

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def music(self):
        '''Offset-positioned rhythm expression music.

        Return container.
        '''
        return self._music

    @property
    def start_offset(self):
        '''Rhythm expression start offset.

        Assigned at initialization during rhythm interpretation.

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Rhythm expression stop offset.
        
        Defined equal to start offset plus 
        prolated duration of rhythm expression

        Return offset.
        '''
        return self.start_offset + self.music.prolated_duration

    ### PUBLIC METHODS ###

    def adjust_to_offsets(self, start_offset=None, stop_offset=None):
        '''Adjust to offsets.

        .. note:: add example.

        Operate in place and return none.
        '''
        if stop_offset < self.stop_offset:
            self.trim_to_stop_offset(stop_offset)
        if self.start_offset < start_offset:
            self.trim_to_start_offset(start_offset)

    def reverse(self):
        '''Reverse rhythm.

        .. note:: add example.

        Operate in place and return none.
        '''
        for container in containertools.iterate_containers_in_expr(self.music):
            container._music.reverse()
        for spanner in spannertools.get_spanners_attached_to_any_improper_child_of_component(self.music):
            spanner._reverse_components()

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
        assert componenttools.is_well_formed_component(trimmed_music)
        self._music = trimmed_music
