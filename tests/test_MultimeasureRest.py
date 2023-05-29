import copy

import abjad


def test_MultimeasureRest___copy___01():
    multi_measure_rest_1 = abjad.MultimeasureRest((1, 4))
    multi_measure_rest_2 = copy.copy(multi_measure_rest_1)

    assert isinstance(multi_measure_rest_1, abjad.MultimeasureRest)
    assert isinstance(multi_measure_rest_2, abjad.MultimeasureRest)
    assert abjad.lilypond(multi_measure_rest_1) == abjad.lilypond(multi_measure_rest_2)
    assert multi_measure_rest_1 is not multi_measure_rest_2


def test_MultimeasureRest___init___01():
    """
    Initializes multimeasure rest from empty input.
    """

    multimeasure_rest = abjad.MultimeasureRest()

    assert abjad.lilypond(multimeasure_rest) == abjad.string.normalize(
        r"""
        R4
        """
    )

    assert abjad.wf.wellformed(multimeasure_rest)
