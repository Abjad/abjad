import abjad


def test_LilyPondParser__indicators__TimeSignature_01():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    time_signature = abjad.TimeSignature((8, 8))
    abjad.attach(time_signature, target[0][0])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 8/8
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select(result).leaves()
    leaf = leaves[0]
    time_signatures = abjad.get.indicators(leaf, abjad.TimeSignature)
    assert len(time_signatures) == 1
