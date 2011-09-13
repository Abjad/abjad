from abjad.tools.iotools.show import show


def show_leaves(leaves, template = None, suppress_pdf = False):
    r""".. versionadded:: 2.0

    Show `leaves` in temporary piano staff score::

        abjad> leaves = leaftools.make_leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
        abjad> score = leaftools.show_leaves(leaves) # doctest: +SKIP
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
    from abjad.tools.scoretools.make_piano_sketch_score_from_leaves import make_piano_sketch_score_from_leaves

    score, treble, bass = make_piano_sketch_score_from_leaves(leaves)
    show(score, template = template, suppress_pdf = suppress_pdf)

    return score
