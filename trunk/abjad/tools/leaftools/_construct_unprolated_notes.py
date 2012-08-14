def _construct_unprolated_notes(pitches, durations, direction='big-endian'):
    '''Private helper returns a list of unprolated notes.
    '''
    from abjad.tools import notetools

    assert len(pitches) == len(durations)
    result = []
    for pitch, dur in zip(pitches, durations):
        result.extend(notetools.make_tied_note(pitch, dur, direction))
    return result
