from abjad.tools import leaftools


def make_tied_chord(pitches, duration, big_endian=True):
    '''Returns a list of chords to fill the given duration.

    Chords returned are tie spanned.
    '''
    from abjad.tools import chordtools

    return leaftools.make_tied_leaf(chordtools.Chord, duration, big_endian=big_endian, pitches=pitches)
