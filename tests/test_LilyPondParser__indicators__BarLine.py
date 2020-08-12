import abjad


def test_LilyPondParser__indicators__BarLine_01():

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)]))
    bar_line = abjad.BarLine("|.")
    abjad.attach(bar_line, target[-1])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'4
            d'4
            c'2
            \bar "|."
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    items = abjad.get.indicators(result[2])
    assert 1 == len(items) and isinstance(items[0], abjad.BarLine)
