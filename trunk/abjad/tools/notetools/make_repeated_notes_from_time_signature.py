def make_repeated_notes_from_time_signature(time_signature, pitch="c'"):
    '''.. versionadded:: 2.0

    Make repeated notes from `time_signature`::

        >>> notetools.make_repeated_notes_from_time_signature((5, 32))
        [Note("c'32"), Note("c'32"), Note("c'32"), Note("c'32"), Note("c'32")]

    Make repeated notes with `pitch` from `time_signature`::

        >>> notetools.make_repeated_notes_from_time_signature((5, 32), pitch="d''")
        [Note("d''32"), Note("d''32"), Note("d''32"), Note("d''32"), Note("d''32")]

    Return list of notes.
    '''
    from abjad.tools import contexttools
    from abjad.tools import notetools

    # afford basic input polymorphism
    time_signature = contexttools.TimeSignatureMark(time_signature)

    # check input
    if time_signature.is_nonbinary:
        raise NotImplementedError('TODO: extend this function for nonbinary time signatures.')

    # make and return repeated notes
    return time_signature.numerator * notetools.Note(pitch, (1, time_signature.denominator))
