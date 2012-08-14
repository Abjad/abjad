from abjad.tools.leaftools.make_tied_leaf import make_tied_leaf


def make_tied_chord(pitches, dur, direction='big-endian'):
    '''Returns a list of chords to fill the given duration.
        Chords returned are Tie spanned.
    '''

    from abjad.tools.chordtools.Chord import Chord
    return make_tied_leaf(Chord, dur, direction, pitches)
