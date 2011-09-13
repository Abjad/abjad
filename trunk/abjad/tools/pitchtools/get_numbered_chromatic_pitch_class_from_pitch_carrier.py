from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier


def get_numbered_chromatic_pitch_class_from_pitch_carrier(pitch_carrier):
    '''.. versionadded:: 2.0

    Get numbered chromatic pitch-class from `pitch_carrier`::

        abjad> note = Note("cs'4")
        abjad> pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(note)
        NumberedChromaticPitchClass(1)

    Raise missing pitch error on empty chords.

    Raise extra pitch error on many-note chords.

    Return numbered chromatic pitch-class.

    .. versionchanged:: 2.0
        renamed ``pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier()`` to
        ``pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier()``.
    '''

    pitch = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier)
    pitch_class = NumberedChromaticPitchClass(pitch)
    return pitch_class
