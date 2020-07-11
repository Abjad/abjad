import abjad


def test_LilyPondParser__contexts__StaffGroup_01():

    target = abjad.StaffGroup([])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new StaffGroup
        <<
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
