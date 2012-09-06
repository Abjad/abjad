from abjad.tools import leaftools


def make_tied_note(pitch, duration, big_endian=True):
    '''Returns a list of notes to fill the given duration.

    Notes returned are tie-spanned.
    '''
    from abjad.tools import notetools

    return leaftools.make_tied_leaf(
        notetools.Note, duration, big_endian=big_endian, pitches=pitch, tied=True)
