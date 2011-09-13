_diatonic_pitch_class_number_to_chromatic_pitch_class_number = {
    0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11 }


def diatonic_pitch_class_number_to_chromatic_pitch_class_number(diatonic_pitch_class_number):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_class_number` to chromatic pitch-class number::

        abjad> pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(6)
        11

    Return nonnegative integer.
    '''

    error_message = '\n\tNot a diatonic pitch-class number: "%s".' % diatonic_pitch_class_number
    if not isinstance(diatonic_pitch_class_number, (int, long)):
        raise TypeError(error_message)

    try:
        return _diatonic_pitch_class_number_to_chromatic_pitch_class_number[
            diatonic_pitch_class_number]
    except KeyError:
        raise ValueError(error_message)
