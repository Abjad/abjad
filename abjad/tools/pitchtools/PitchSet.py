# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class PitchSet(Set):
    r'''A pitch segment.

    ::

        >>> numbered_pitch_set = pitchtools.PitchSet(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitch,
        ...     )
        >>> numbered_pitch_set
        PitchSet([-2, -1.5, 6, 7])

    ::

        >>> named_pitch_set = pitchtools.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=NamedPitch,
        ...     )
        >>> named_pitch_set
        PitchSet(['bf,', 'aqs', 'bqf', "fs'", "g'"])

    Returns pitch segment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _sort_self(self):
        from abjad.tools import pitchtools
        return sorted(pitchtools.PitchSegment(tuple(self)))

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Pitch

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None, custom_identifier=None):
        r'''Initialize pitch set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.PitchSet.from_selection(selection)
            PitchSet(['c', 'g', 'b', "c'", "d'", "fs'", "a'"])
        
        Returns pitch set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            tokens=pitch_segment,
            item_class=item_class,
            custom_identifier=custom_identifier,
            )

    def invert(self, axis):
        r'''Invert pitch set around `axis`.

        Emit new pitch set.
        '''
        tokens = (pitch.invert(axis) for pitch in self)
        return self.new(tokens=tokens)

    def is_equivalent_under_transposition(self, expr):
        r'''True if equivalent under transposition to `expr`, otherwise False.
        
        Returns boolean.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = self.new(tokens=new_pitch)
        return expr == new_pitches

    def transpose(self, expr):
        r'''Transpose all pitches in self by `expr`.
        '''
        from abjad.tools import pitchtools
        #interval = pitchtools.NumberedInterval(n)
        tokens = (pitch.transpose(expr) for pitch in self)
        return self.new(tokens=tokens)

    ### PUBLIC PROPERTIES ###

    @property
    def duplicate_pitch_classes(self):
        from abjad.tools import pitchtools
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = pitchtools.NumberedPitchClass(pitch)
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return pitchtools.PitchClassSet(
            duplicate_pitch_classes,
            item_class=pitchtools.NumberedPitchClass,
            )

    @property
    def is_pitch_class_unique(self):
        from abjad.tools import pitchtools
        numbered_pitch_class_set = pitchtools.PitchClassSet(
            self, item_class=pitchtools.NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)
