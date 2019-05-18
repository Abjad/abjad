import abjad
import pytest


def test_LilyPondParser__indicators__BarLine_01():

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)]))
    bar_line = abjad.BarLine("|.")
    abjad.attach(bar_line, target[-1])

    assert format(target) == abjad.String.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    items = abjad.inspect(result[2]).indicators()
    assert 1 == len(items) and isinstance(items[0], abjad.BarLine)
