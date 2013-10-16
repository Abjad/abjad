# -*- encoding: utf-8 -*-
from abjad.tools import chordtools
from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import notetools
from abjad.tools import pitchtools


def transpose_from_sounding_pitch_to_written_pitch(expr):
    r'''Transpose notes and chords in `expr` from sounding pitch 
    to written pitch:

    ::

        >>> staff = Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> instrumenttools.BFlatClarinet()(staff)
        BFlatClarinet()(Staff{4})

    ..  doctest::

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

        >>> instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            <d' fs' a'>4
            e'4
            r4
            fs'4
        }

    Return none.
    '''
    from abjad.tools import instrumenttools

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        if not note_or_chord.written_pitch_indication_is_at_sounding_pitch:
            continue
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.sounding_pitch_of_written_middle_c
        t_n = pitchtools.NamedPitch('C4') - sounding_pitch
        t_n *= -1
        if isinstance(note_or_chord, notetools.Note):
            note_or_chord.written_pitch = pitchtools.transpose_pitch_carrier_by_interval(
                note_or_chord.written_pitch, t_n)
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = False
        elif isinstance(note_or_chord, chordtools.Chord):
            pitches = [pitchtools.transpose_pitch_carrier_by_interval(pitch, t_n)
                for pitch in note_or_chord.written_pitches]
            note_or_chord.written_pitches = pitches
            note_or_chord.written_pitch_indication_is_at_sounding_pitch = False
