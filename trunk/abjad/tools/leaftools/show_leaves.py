from abjad.tools import iotools


def show_leaves(leaves, suppress_pdf=False):
    r""".. versionadded:: 2.0

    Show `leaves` in temporary piano staff score::

        >>> leaves = leaftools.make_leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
        >>> score = leaftools.show_leaves(leaves) # doctest: +SKIP
        \new Score <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    r4
                    cs'4
                    <g' a''>4
                    r4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    r4
                    r4
                    <c, d,>4
                    r4
                }
            >>
        >>

    Useful when working with notes, rests, chords not yet added to score.

    Return temporary piano staff score.
    """
    from abjad.tools import scoretools

    score, treble, bass = scoretools.make_piano_sketch_score_from_leaves(leaves)
    iotools.show(score, suppress_pdf=suppress_pdf)

    return score
