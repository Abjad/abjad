import abjad


def test_LilyPondParser__indicators__BarLine_01():
    target = abjad.Staff(
        abjad.makers.make_notes(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)])
    )
    abjad.Score([target], name="Score")
    bar_line = abjad.BarLine("|.")
    abjad.attach(bar_line, target[-1])

    assert abjad.lilypond(target) == abjad.string.normalize(
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
