import abjad


def test_LilyPondParser__contexts__context_ids_01():

    maker = abjad.NoteMaker()
    notes = maker([0, 2, 4, 5, 7], (1, 8))
    target = abjad.Staff(notes)
    target.name = "foo"

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \context Staff = "foo"
        {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
