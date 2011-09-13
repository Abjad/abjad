_diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
    0: 'c', 1: 'd', 2: 'e', 3: 'f', 4: 'g', 5: 'a', 6: 'b' }


def diatonic_pitch_class_number_to_diatonic_pitch_class_name(diatonic_pitch_class_number):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_class_number` to diatonic pitch-class name::

        abjad> pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(0)
        'c'

    Return string.
    '''

    error_message = '\n\tNot diatonic pitch-class number: "%s".' % diatonic_pitch_class_number
    if not isinstance(diatonic_pitch_class_number, (int, long)):
        raise TypeError(error_message)

    try:
        return _diatonic_pitch_class_number_to_diatonic_pitch_class_name[diatonic_pitch_class_number]
    except KeyError:
        raise ValueError(error_message)
