from abjad.tools import leaftools


def make_tied_chord(pitches, duration,
    decrease_durations_monotonically=True, forbidden_written_duration=None):
    '''Returns a list of chords to fill the given duration.

    Chords returned are tie spanned.
    '''
    from abjad.tools import chordtools

    return leaftools.make_tied_leaf(
        chordtools.Chord, duration,
        decrease_durations_monotonically=decrease_durations_monotonically,
        forbidden_written_duration=forbidden_written_duration,
        pitches=pitches)
