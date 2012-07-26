from abjad.tools import abctools
from abjad.tools import sequencetools
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent
from experimental.quantizationtools.SilentQEvent import SilentQEvent
from experimental.quantizationtools.TerminalQEvent import TerminalQEvent


class QEventSequence(tuple, abctools.ImmutableAbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __new__(klass, *args):
        assert 1 < len(args)
        assert all([isinstance(x, (PitchedQEvent, SilentQEvent)) for x in args[:-1]])
        assert isinstance(args[-1], TerminalQEvent)
        assert sequencetools.is_monotonically_increasing_sequence([x.offset for x in args])
        assert 0 <= args[0].offset
        return tuple.__new__(klass, args)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return durationtools.Duration(self[-1].offset)

    ### PUBLIC METHODS ###

    @classmethod
    def from_tempo_scaled_leaves(klass, leaves, tempo=None):
        pass

    @classmethod
    def from_tempo_scaled_rationals(klass, rationals, tempo=None):
        pass
    
    @classmethod
    def from_millisecond_pitch_pairs(klass, pairs):
        pass

    @classmethod
    def from_millisecond_offsets(klass, offsets):
        pass

    @classmethod
    def from_millisecond_durations(klass, durations):
        pass
