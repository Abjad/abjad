from abjad.tools import chordtools
from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import notetools
from abjad.tools import pitchtools


def transpose_from_fingered_pitch_to_sounding_pitch(expr):
    r'''.. versionadded:: 2.0

    Transpose notes and chords in `expr` from sounding pitch to fingered pitch::

        >>> staff = Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> instrumenttools.BFlatClarinet()(staff)
        BFlatClarinet()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            <c' e' g'>4
            d'4
            r4
            e'4
        }

    ::

        >>> for leaf in staff.leaves:
        ...   leaf.written_pitch_indication_is_at_sounding_pitch = False

        >>> instrumenttools.transpose_from_fingered_pitch_to_sounding_pitch(staff)

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            <bf d' f'>4
            c'4
            r4
            d'4
        }

    Return none.
    '''

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        if note_or_chord.written_pitch_indication_is_at_sounding_pitch:
            continue
        instrument = contexttools.get_effective_instrument(note_or_chord)
        if not instrument:
            continue
        t_n = instrument.interval_of_transposition
        if isinstance(note_or_chord, notetools.Note):
            note_or_chord.written_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(
                note_or_chord.written_pitch, t_n)
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = True
        elif isinstance(note_or_chord, chordtools.Chord):
            pitches = [pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
                for pitch in note_or_chord.written_pitches]
            note_or_chord.written_pitches = pitches
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = True
