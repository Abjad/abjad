from abjad.tools import durationtools


def make_notes_with_multiplied_durations(pitch, written_duration, multiplied_durations):
    '''.. versionadded:: 2.0

    Make `written_duration` notes with `pitch` and `multiplied_durations`::

        >>> args = [0, Duration(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)]]
        >>> notetools.make_notes_with_multiplied_durations(*args)
        [Note("c'4 * 2"), Note("c'4 * 4/3"), Note("c'4 * 1"), Note("c'4 * 4/5")]

    Useful for making spatially positioned notes.

    Return list of notes.
    '''
    from abjad.tools import notetools

    # initialize input
    written_duration = durationtools.Duration(written_duration)

    # make notes
    notes = []
    for multiplied_duration in multiplied_durations:
        multiplied_duration = durationtools.Duration(multiplied_duration)
        note = notetools.Note(pitch, written_duration)
        multiplier = multiplied_duration / written_duration
        note.duration_multiplier = multiplier
        notes.append(note)

    # return notes
    return notes
