# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import iterate


def transpose_from_written_pitch_to_sounding_pitch(argument):
    r'''Transpose notes and chords in `argument` from sounding pitch
    to written pitch:

    ::

        >>> staff = Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> clarinet = instrumenttools.ClarinetInBFlat()
        >>> attach(clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
            \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
            <c' e' g'>4
            d'4
            r4
            e'4
        }

    ::

        >>> instrumenttools.transpose_from_written_pitch_to_sounding_pitch(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
            \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
            <bf d' f'>4
            c'4
            r4
            d'4
        }

    Returns none.
    '''
    from abjad.tools import instrumenttools
    prototype = (scoretools.Note, scoretools.Chord)
    for note_or_chord in iterate(argument).by_class(prototype):
        instrument = note_or_chord._get_effective(
            instrumenttools.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.sounding_pitch_of_written_middle_c
        interval = pitchtools.NamedPitch('C4') - sounding_pitch
        if isinstance(note_or_chord, scoretools.Note):
            written_pitch = note_or_chord.written_pitch
            written_pitch = interval.transpose(written_pitch)
            note_or_chord.written_pitch = written_pitch
        elif isinstance(note_or_chord, scoretools.Chord):
            pitches = [
                interval.transpose(pitch)
                for pitch in note_or_chord.written_pitches
                ]
            note_or_chord.written_pitches = pitches
