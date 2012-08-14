from abjad.tools.leaftools.make_tied_leaf import make_tied_leaf


def make_tied_note(pitch, dur, direction='big-endian'):
    '''Returns a list of notes to fill the given duration.
        Notes returned are Tie spanned.
    '''
    from abjad.tools.notetools.Note import Note

    return make_tied_leaf(Note, dur, direction, pitch)
