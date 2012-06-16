from abjad import *


def test_tuplettools_make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots_01():

    duration = Fraction(3, 16)

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1])
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 1])
    assert t.lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 1, 1])
    assert t.lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 1, 1, 1])
    assert t.lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 1, 1, 1, 1])
    assert t.lilypond_format == "\\times 4/5 {\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"


def test_tuplettools_make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots_02():

    duration = Fraction(3, 16)

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1])
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 2])
    assert t.lilypond_format == "{\n\tc'16\n\tc'8\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 2, 2])
    assert t.lilypond_format == "\\times 4/5 {\n\tc'32.\n\tc'16.\n\tc'16.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 2, 2, 3])
    assert t.lilypond_format == "\\fraction \\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, 2, 2, 3, 3])
    assert t.lilypond_format == "\\fraction \\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"


def test_tuplettools_make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots_03():
    '''Reduce proportions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [1, -2, -2, 3, 3])
    t2 = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        duration, [2, -4, -4, 6, 6])
    assert t1.lilypond_format == t2.lilypond_format

    t = tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots(
        Fraction(1, 8), [27])
    assert t.lilypond_format == "{\n\tc'8\n}"
