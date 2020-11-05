import abjad


def test_LilyPondParser__indicators__KeySignature_01():

    target = abjad.Staff([abjad.Note("fs'", 1)])
    key_signature = abjad.KeySignature("g", "major")
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \key g \major
            fs'1
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    key_signatures = abjad.get.indicators(result[0], abjad.KeySignature)
    assert len(key_signatures) == 1
