from abjad.tools import leaftools


def make_tied_note(pitch, duration, decrease_durations_monotonically=True, forbidden_written_duration=None):
    '''Returns a list of notes to fill the given duration.

    Notes returned are tie-spanned.
    '''
    from abjad.tools import notetools

    return leaftools.make_tied_leaf(
        notetools.Note, duration,
        decrease_durations_monotonically=decrease_durations_monotonically,
        forbidden_written_duration=forbidden_written_duration,
        pitches=pitch, tie_parts=True)
