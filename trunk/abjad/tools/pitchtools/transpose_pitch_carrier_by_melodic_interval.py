# -*- encoding: utf-8 -*-
import copy
import numbers


def transpose_pitch_carrier_by_melodic_interval(
    pitch_carrier, melodic_interval):
    '''Transpose `pitch_carrier` by diatonic `melodic_interval`:

    ::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(
        ...     chord, '+m2')
        Chord("<df' f' af'>4")

    Transpose `pitch_carrier` by chromatic `melodic_interval`:

    ::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(chord, 1)
        Chord("<cs' f' af'>4")

    Return non-pitch-carrying input unchaged:

    ::

        >>> rest = Rest('r4')

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(rest, 1)
        Rest('r4')

    Return `pitch_carrier`.
    '''
    from abjad.tools import chordtools
    from abjad.tools import componenttools
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    def _transpose_pitch_by_melodic_diatonic_interval(pitch, mdi):
        chromatic_pitch_number = pitch.chromatic_pitch_number + mdi.semitones
        diatonic_pitch_class_number = \
            (pitch.diatonic_pitch_class_number + mdi.staff_spaces) % 7
        diatonic_pitch_class_name = \
            pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(
            diatonic_pitch_class_number)
        named_chromatic_pitch = pitchtools.NamedPitch(
            chromatic_pitch_number, diatonic_pitch_class_name)
        return type(pitch)(named_chromatic_pitch)

    def _transpose_pitch_carrier_by_melodic_diatonic_interval(
        pitch_carrier, melodic_diatonic_interval):
        mdi = pitchtools.NamedMelodicInterval(melodic_diatonic_interval)
        if isinstance(pitch_carrier, pitchtools.Pitch):
            return _transpose_pitch_by_melodic_diatonic_interval(
                pitch_carrier, mdi)
        elif isinstance(pitch_carrier, notetools.Note):
            new_note = copy.copy(pitch_carrier)
            new_pitch = _transpose_pitch_by_melodic_diatonic_interval(
                pitch_carrier.written_pitch, mdi)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, chordtools.Chord):
            new_chord = copy.copy(pitch_carrier)
            for new_nh, old_nh in \
                zip(new_chord.note_heads, pitch_carrier.note_heads):
                new_pitch = _transpose_pitch_by_melodic_diatonic_interval(
                    old_nh.written_pitch, mdi)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier

    def _transpose_pitch_carrier_by_melodic_chromatic_interval(
        pitch_carrier, melodic_chromatic_interval):
        mci = pitchtools.NumberedMelodicInterval(melodic_chromatic_interval)
        if isinstance(pitch_carrier, pitchtools.Pitch):
            number = pitch_carrier.chromatic_pitch_number + mci.semitones
            return type(pitch_carrier)(number)
        elif isinstance(pitch_carrier, numbers.Number):
            pitch_carrier = pitchtools.NumberedPitch(pitch_carrier)
            result = _transpose_pitch_carrier_by_melodic_chromatic_interval(
                pitch_carrier, mci)
            return result.chromatic_pitch_number
        elif isinstance(pitch_carrier, notetools.Note):
            new_note = copy.copy(pitch_carrier)
            number = abs(pitch_carrier.written_pitch.numbered_chromatic_pitch)
            number += mci.number
            new_pitch = pitchtools.NamedPitch(number)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, chordtools.Chord):
            new_chord = copy.copy(pitch_carrier)
            for new_nh, old_nh in \
                zip(new_chord.note_heads, pitch_carrier.note_heads):
                number = abs(old_nh.written_pitch.numbered_chromatic_pitch)
                number += mci.number
                new_pitch = pitchtools.NamedPitch(number)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier

    diatonic_types = (pitchtools.NamedMelodicInterval, str)
    if isinstance(melodic_interval, diatonic_types):
        melodic_interval = \
            pitchtools.NamedMelodicInterval(melodic_interval)
        return _transpose_pitch_carrier_by_melodic_diatonic_interval(
            pitch_carrier, melodic_interval)
    else:
        melodic_interval = \
            pitchtools.NumberedMelodicInterval(melodic_interval)
        return _transpose_pitch_carrier_by_melodic_chromatic_interval(
            pitch_carrier, melodic_interval)
