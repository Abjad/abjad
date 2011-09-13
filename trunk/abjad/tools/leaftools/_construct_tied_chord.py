from abjad.tools.leaftools._construct_tied_leaf import _construct_tied_leaf


def _construct_tied_chord(pitches, dur, direction='big-endian'):
    '''Returns a list of chords to fill the given duration.
        Chords returned are Tie spanned.
    '''

    from abjad.tools.chordtools.Chord import Chord
    return _construct_tied_leaf(Chord, dur, direction, pitches)
