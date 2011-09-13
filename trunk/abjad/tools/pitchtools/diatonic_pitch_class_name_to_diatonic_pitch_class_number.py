_diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
    'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6 }


def diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_class_name` to diatonic pitch-class number::

        abjad> pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('c')
        0

    Return integer.
    '''

    error_message = '\n\tNot diatonic pitch-class name: "%s".' % diatonic_pitch_class_name
    if not isinstance(diatonic_pitch_class_name, str):
        raise TypeError(error_message)

    try:
        return _diatonic_pitch_class_name_to_diatonic_pitch_class_number[diatonic_pitch_class_name]
    except KeyError:
        raise ValueError(error_message)
