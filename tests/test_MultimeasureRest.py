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

    assert abjad.wf.is_wellformed(multimeasure_rest)


def test_MultimeasureRest___init___02():
    """
    REGRESSION #1049. Parser reads multimeasure rest multipliers.
    """

    staff = abjad.Staff(r"\time 3/8 R1 * 3/8")
    score = abjad.Score([staff], name="Score")

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \context Score = "Score"
        <<
            \new Staff
            {
                \time 3/8
                R1 * 3/8
            }
        >>
        """
    )

    assert abjad.wf.is_wellformed(score)


def test_MultimeasureRest___init___03():
    """
    Multimeasure rests may be tagged.
    """

    rest = abjad.MultimeasureRest("R1", tag=abjad.Tag("GLOBAL_MULTIMEASURE_REST"))

    assert abjad.lilypond(rest, tags=True) == abjad.string.normalize(
        """
          %! GLOBAL_MULTIMEASURE_REST
        R1
        """
    )
