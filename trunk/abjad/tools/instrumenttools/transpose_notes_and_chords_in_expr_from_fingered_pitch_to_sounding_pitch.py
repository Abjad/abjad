from abjad.tools import pitchtools
from abjad.tools.contexttools.get_effective_instrument import get_effective_instrument


def transpose_notes_and_chords_in_expr_from_fingered_pitch_to_sounding_pitch(expr):
    r'''.. versionadded:: 2.0

    Transpose notes and chords in `expr` from sounding pitch to fingered pitch::

        abjad> staff = Staff("<c' e' g'>4 d'4 r4 e'4")
        abjad> instrumenttools.BFlatClarinet()(staff)
        BFlatClarinet()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            <c' e' g'>4
            d'4
            r4
            e'4
        }

    ::

        abjad> for leaf in staff.leaves:
        ...   leaf.written_pitch_indication_is_at_sounding_pitch = False

        abjad> instrumenttools.transpose_notes_and_chords_in_expr_from_fingered_pitch_to_sounding_pitch(staff)

    ::

        abjad> f(staff)
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
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools import leaftools

    for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        if note_or_chord.written_pitch_indication_is_at_sounding_pitch:
            continue
        instrument = get_effective_instrument(note_or_chord)
        if not instrument:
            continue
        t_n = instrument.interval_of_transposition
        if isinstance(note_or_chord, Note):
            note_or_chord.written_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(
                note_or_chord.written_pitch, t_n)
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = True
        elif isinstance(note_or_chord, Chord):
            pitches = [pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
                for pitch in note_or_chord.written_pitches]
            note_or_chord.written_pitches = pitches
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = True
