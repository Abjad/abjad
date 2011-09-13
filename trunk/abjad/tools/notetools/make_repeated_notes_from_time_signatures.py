from abjad.tools.notetools.make_repeated_notes_from_time_signature import make_repeated_notes_from_time_signature


def make_repeated_notes_from_time_signatures(time_signatures, pitch = "c'"):
    '''.. versionadded 1.1.2

    Make repated notes from `time_signatures`::

        notetools.make_repeated_notes_from_time_signatures([(2, 8), (3, 32)])
        [[Note("c'8"), Note("c'8")], [Note("c'32"), Note("c'32"), Note("c'32")]]

    Make repeated notes with `pitch` from `time_signatures`::

        abjad> notetools.make_repeated_notes_from_time_signatures([(2, 8), (3, 32)], pitch = "d''")
        [[Note("d''8"), Note("d''8")], [Note("d''32"), Note("d''32"), Note("d''32")]]

    Return two-dimensional list of note lists.

    Use ``sequencetools.flatten_sequence()`` to flatten output if required.
    '''

    # init result
    result = []

    # iterate time signatures and make notes
    for time_signature in time_signatures:
        notes = make_repeated_notes_from_time_signature(time_signature, pitch = pitch)
        result.append(notes)

    # return result
    return result
