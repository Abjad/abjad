# -*- encoding: utf-8 -*-
import copy
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment


class NamedPitchClassSegment(PitchClassSegment):
    '''Abjad model of named chromatic pitch-class segment:

    ::

        >>> pitchtools.NamedPitchClassSegment(
        ...     ['gs', 'a', 'as', 'c', 'cs'])
        NamedPitchClassSegment(['gs', 'a', 'as', 'c', 'cs'])

    Named chromatic pitch-class segments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __init__(self, tokens, **kwargs):
        from abjad.tools import pitchtools
        PitchClassSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedPitchClass,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_diatonic_interval_class_segment(self):
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        dics = mathtools.difference_series(self)
        return pitchtools.NamedInversionEquivalentIntervalClassSegment(dics)

    @property
    def named_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClassSet(self)

    @property
    def named_chromatic_pitch_classes(self):
        return tuple(self[:])

    @property
    def numbered_chromatic_pitch_class_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSegment(self)

    @property
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSet(self)

    @property
    def numbered_chromatic_pitch_classes(self):
        return self.pitch_class_segment.pitch_classes

    ### PUBLIC METHODS ###

    def is_equivalent_under_transposition(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            return False
        if not len(self) == len(arg):
            return False
        difference = -(pitchtools.NamedPitch(arg[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_npcs = [x + difference for x in self]
        new_npc_seg = type(self)(new_npcs)
        return arg == new_npc_seg

    def retrograde(self):
        return type(self)(reversed(self))

    def rotate(self, n):
        from abjad.tools import sequencetools
        named_chromatic_pitch_classes = sequencetools.rotate_sequence(
            self.named_chromatic_pitch_classes, n)
        return type(self)(named_chromatic_pitch_classes)

    def transpose(self, melodic_diatonic_interval):
        return type(self)([npc + melodic_diatonic_interval  for npc in self])
