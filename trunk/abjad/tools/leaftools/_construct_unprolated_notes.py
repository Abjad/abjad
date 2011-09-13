from abjad.tools.leaftools._construct_tied_note import _construct_tied_note


def _construct_unprolated_notes(pitches, durations, direction='big-endian'):
    '''Private helper returns a list of unprolated notes.
    '''

    assert len(pitches) == len(durations)
    result = []
    for pitch, dur in zip(pitches, durations):
        result.extend(_construct_tied_note(pitch, dur, direction))
    return result
