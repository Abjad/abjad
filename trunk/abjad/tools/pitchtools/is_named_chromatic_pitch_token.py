from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.is_chromatic_pitch_class_name_octave_number_pair import is_chromatic_pitch_class_name_octave_number_pair


# TODO: extend with strings like "c" and "A4"
def is_named_chromatic_pitch_token(pitch_token):
    '''.. versionadded:: 1.1

    True when `pitch_token` has the form of an Abjad pitch token.
    Otherwise false::

        abjad> pitchtools.is_named_chromatic_pitch_token(('c', 4))
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.is_pitch_token()`` to
        ``pitchtools.is_named_chromatic_pitch_token()``.
    '''

    if isinstance(pitch_token, NamedChromaticPitch):
        return True
    elif is_chromatic_pitch_class_name_octave_number_pair(pitch_token):
        return True
    elif isinstance(pitch_token, (int, long)):
        return True
    elif isinstance(pitch_token, float) and pitch_token % 0.5 == 0:
        return True
    else:
        return False
