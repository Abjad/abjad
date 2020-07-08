import abjad


def test_MultimeasureRest___init___01():
    """
    Initializes multimeasure rest from empty input.
    """

    multimeasure_rest = abjad.MultimeasureRest()

    assert format(multimeasure_rest) == abjad.String.normalize(
        r"""
        R4
        """
    )

    assert abjad.wellformed(multimeasure_rest)
