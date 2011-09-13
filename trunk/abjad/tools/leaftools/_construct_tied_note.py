from abjad.tools.leaftools._construct_tied_leaf import _construct_tied_leaf


def _construct_tied_note(pitch, dur, direction='big-endian'):
    '''Returns a list of notes to fill the given duration.
        Notes returned are Tie spanned.
    '''
    from abjad.tools.notetools.Note import Note

    return _construct_tied_leaf(Note, dur, direction, pitch)
