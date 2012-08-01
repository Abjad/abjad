from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent
from experimental.quantizationtools.SilentQEvent import SilentQEvent
from experimental.quantizationtools.TerminalQEvent import TerminalQEvent


class QEventSequence(tuple, abctools.ImmutableAbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __new__(klass, args):
        assert 1 < len(args)
        assert all([isinstance(x, (PitchedQEvent, SilentQEvent)) for x in args[:-1]])
        assert isinstance(args[-1], TerminalQEvent)
        assert sequencetools.is_monotonically_increasing_sequence([x.offset for x in args])
        assert 0 <= args[0].offset
        return tuple.__new__(klass, args)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._class_name, tuple.__repr__(self))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration_in_ms(self):
        return durationtools.Duration(self[-1].offset)

    ### PUBLIC METHODS ###

    @classmethod
    def from_tempo_scaled_leaves(klass, leaves, tempo=None):
        from experimental.quantizationtools import tempo_scaled_leaves_to_q_events
        return klass(tempo_scaled_leaves_to_q_events(leaves, tempo))

    @classmethod
    def from_tempo_scaled_rationals(klass, rationals, tempo=None):
        from experimental.quantizationtools import tempo_scaled_rationals_to_q_events
        return klass(tempo_scaled_rationals_to_q_events(rationals, tempo))
    
    @classmethod
    def from_millisecond_pitch_pairs(klass, pairs):
        from experimental.quantizationtools import millisecond_pitch_pairs_to_q_events
        return klass(millisecond_pitch_pairs_to_q_events(pairs))

    @classmethod
    def from_millisecond_offsets(klass, offsets):
        q_events = [PitchedQEvent(x, [0]) for x in offsets[:-1]]
        q_events.append(TerminalQEvent(offsets[-1]))
        return klass(q_events)

    @classmethod
    def from_millisecond_durations(klass, durations):
        from experimental.quantizationtools import milliseconds_to_q_events
        return klass(milliseconds_to_q_events(durations))
