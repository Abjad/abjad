import abjad


def apply_final_bar_lines(score):
    """
    Applies final bar lines to score.
    """

    for voice in abjad.iterate(score).components(abjad.Voice):
        bar_line = abjad.BarLine('|.')
        leaf = abjad.inspect(voice).get_leaf(-1)
        abjad.attach(bar_line, leaf)
