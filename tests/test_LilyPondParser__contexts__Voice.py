import abjad


def test_LilyPondParser__contexts__Voice_01():

    target = abjad.Voice([])

    assert format(target) == abjad.String.normalize(
        r"""
        \new Voice
        {
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
