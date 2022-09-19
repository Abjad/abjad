import abjad


def test_LilyPondParser__containers__Tuplet_01():

    notes = abjad.makers.make_notes([0, 2, 4], (1, 8))
    target = abjad.Tuplet(abjad.Multiplier(2, 3), notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \times 2/3
        {
            c'8
            d'8
            e'8
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
