# -*- coding: utf-8 -*-
import copy
import numbers


def transpose_pitch_carrier_by_interval(pitch_carrier, interval):
    '''Transposes `pitch_carrier` by named `interval`.

    ::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_interval(
        ...     chord, '+m2')
        Chord("<df' f' af'>4")

    Transpose `pitch_carrier` by numbered `interval`:

    ::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_interval(chord, 1)
        Chord("<cs' f' af'>4")

    Returns non-pitch-carrying input unchaged:

    ::

        >>> rest = Rest('r4')

    ::

        >>> pitchtools.transpose_pitch_carrier_by_interval(rest, 1)
        Rest('r4')

    Return `pitch_carrier`.
    '''
    from abjad.tools import pitchtools
    from abjad.tools import scoretools

    def _transpose_pitch_by_named_interval(pitch, mdi):
        pitch_number = pitch.pitch_number + mdi.semitones
        diatonic_pitch_class_number = \
            (pitch.diatonic_pitch_class_number + mdi.staff_spaces) % 7
        diatonic_pitch_class_name = \
            pitchtools.PitchClass._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
                diatonic_pitch_class_number]
        named_pitch = pitchtools.NamedPitch(
            pitch_number, diatonic_pitch_class_name)
        return type(pitch)(named_pitch)

    def _transpose_pitch_carrier_by_named_interval(
        pitch_carrier, named_interval):
        mdi = pitchtools.NamedInterval(named_interval)
        if isinstance(pitch_carrier, pitchtools.Pitch):
            return _transpose_pitch_by_named_interval(
                pitch_carrier, mdi)
        elif isinstance(pitch_carrier, scoretools.Note):
            new_note = copy.copy(pitch_carrier)
            new_pitch = _transpose_pitch_by_named_interval(
                pitch_carrier.written_pitch, mdi)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, scoretools.Chord):
            new_chord = copy.copy(pitch_carrier)
            for new_nh, old_nh in \
                zip(new_chord.note_heads, pitch_carrier.note_heads):
                new_pitch = _transpose_pitch_by_named_interval(
                    old_nh.written_pitch, mdi)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier

    def _transpose_pitch_carrier_by_numbered_interval(
        pitch_carrier, numbered_interval):
        mci = pitchtools.NumberedInterval(numbered_interval)
        if isinstance(pitch_carrier, pitchtools.Pitch):
            number = pitch_carrier.pitch_number + mci.semitones
            return type(pitch_carrier)(number)
        elif isinstance(pitch_carrier, numbers.Number):
            pitch_carrier = pitchtools.NumberedPitch(pitch_carrier)
            result = _transpose_pitch_carrier_by_numbered_interval(
                pitch_carrier, mci)
            return result.pitch_number
        elif isinstance(pitch_carrier, scoretools.Note):
            new_note = copy.copy(pitch_carrier)
            number = pitchtools.NumberedPitch(
                pitch_carrier.written_pitch).pitch_number
            number += mci.number
            new_pitch = pitchtools.NamedPitch(number)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, scoretools.Chord):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                number = \
                    pitchtools.NumberedPitch(old_nh.written_pitch).pitch_number
                number += mci.number
                new_pitch = pitchtools.NamedPitch(number)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier


    diatonic_types = (pitchtools.NamedInterval, str)
    if isinstance(interval, diatonic_types):
        interval = \
            pitchtools.NamedInterval(interval)
        return _transpose_pitch_carrier_by_named_interval(
            pitch_carrier, interval)
    else:
        interval = \
            pitchtools.NumberedInterval(interval)
        return _transpose_pitch_carrier_by_numbered_interval(
            pitch_carrier, interval)