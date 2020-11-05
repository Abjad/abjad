import abjad


def test_MultimeasureRest___init___01():
    """
    Initializes multimeasure rest from empty input.
    """

    multimeasure_rest = abjad.MultimeasureRest()

    assert abjad.lilypond(multimeasure_rest) == abjad.String.normalize(
        r"""
        R4
        """
    )

    assert abjad.wf.wellformed(multimeasure_rest)
