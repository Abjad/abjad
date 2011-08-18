from abjad import *


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots_01():

    duration = Fraction(3, 16)

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'8\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 1])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'16\n\tc'16\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 1, 1])
    assert t.format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 1, 1, 1])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 1, 1, 1, 1])
    assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots_02():

    duration = Fraction(3, 16)

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'8\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 2])
    assert t.format == "{\n\tc'16\n\tc'8\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 2, 2])
    assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 2, 2, 3])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, 2, 2, 3, 3])
    assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots_03():
    '''Interpret negative proportions as rests.
    '''

    duration = Fraction(3, 16)

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, -2, -2, 3, 3])
    assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tr32\n\tr32\n\tc'32.\n\tc'32.\n}"


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots_04():
    '''Reduce proportions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [1, -2, -2, 3, 3])
    t2 = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        duration, [2, -4, -4, 6, 6])
    assert t1.format == t2.format

    t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
        Fraction(1, 8), [27])
    assert t.format == "{\n\tc'8\n}"
