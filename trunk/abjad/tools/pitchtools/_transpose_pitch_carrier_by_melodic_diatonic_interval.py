from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools._Pitch import _Pitch
from abjad.tools.pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name import diatonic_pitch_class_number_to_diatonic_pitch_class_name


def _transpose_pitch_carrier_by_melodic_diatonic_interval(pitch_carrier, melodic_diatonic_interval):
    '''.. versionadded:: 2.0

    Transpose `pitch_carrier` by `melodic_diatonic_interval`::

        abjad> from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_diatonic_interval import _transpose_pitch_carrier_by_melodic_diatonic_interval

        abjad> pitch_carrier = pitchtools.NamedChromaticPitch("c''")
        abjad> mdi = pitchtools.MelodicDiatonicInterval('minor', -3)
        abjad> _transpose_pitch_carrier_by_melodic_diatonic_interval(pitch_carrier, mdi)
        NamedChromaticPitch("a'")

    Return named chromatic pitch.
    '''
    from abjad.tools import componenttools
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note

    try:
        mdi = MelodicDiatonicInterval(melodic_diatonic_interval)
    except (TypeError, ValueError):
        raise TypeError('must be melodic diatonic interval.')

    if isinstance(pitch_carrier, _Pitch):
        return _transpose_pitch_by_melodic_diatonic_interval(pitch_carrier, mdi)
    elif isinstance(pitch_carrier, Note):
        new_note = componenttools.copy_components_and_remove_all_spanners([pitch_carrier])[0]
        new_pitch = _transpose_pitch_by_melodic_diatonic_interval(pitch_carrier.written_pitch, mdi)
        new_note.written_pitch = new_pitch
        return new_note
    elif isinstance(pitch_carrier, Chord):
        new_chord = componenttools.copy_components_and_remove_all_spanners([pitch_carrier])[0]
        for new_nh, old_nh in zip(new_chord.note_heads, pitch_carrier.note_heads):
            new_pitch = _transpose_pitch_by_melodic_diatonic_interval(old_nh.written_pitch, mdi)
            new_nh.written_pitch = new_pitch
        return new_chord
    else:
        #raise TypeError('must be pitch, note or chord: %s' % str(pitch_carrier))
        return pitch_carrier


def _transpose_pitch_by_melodic_diatonic_interval(pitch, mdi):
    chromatic_pitch_number = pitch.chromatic_pitch_number + mdi.semitones
    diatonic_pitch_class_number = (pitch.diatonic_pitch_class_number + mdi.staff_spaces) % 7
    diatonic_pitch_class_name = diatonic_pitch_class_number_to_diatonic_pitch_class_name(
        diatonic_pitch_class_number)
    named_chromatic_pitch = NamedChromaticPitch(chromatic_pitch_number, diatonic_pitch_class_name)
    return type(pitch)(named_chromatic_pitch)
