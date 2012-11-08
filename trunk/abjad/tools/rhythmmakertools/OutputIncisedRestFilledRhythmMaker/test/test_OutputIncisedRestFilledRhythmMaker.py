from abjad import *
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def test_OutputIncisedRestFilledRhythmMaker_01():

    prefix_talea, prefix_lengths = [8], [2]
    suffix_talea, suffix_lengths = [3], [4]
    talea_denominator = 32
    maker = rhythmmakertools.OutputIncisedRestFilledRhythmMaker(
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            c'4
            c'4
            r8
        }
        {
            \time 5/8
            r2
            r8
        }
        {
            \time 5/8
            r4
            c'16.
            c'16.
            c'16.
            c'16.
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tc'16.\n\t\tc'16.\n\t\tc'16.\n\t\tc'16.\n\t}\n}"


def test_OutputIncisedRestFilledRhythmMaker_02():

    prefix_talea, prefix_lengths = [1], [20]
    suffix_talea, suffix_lengths = [1], [2]
    talea_denominator = 4
    maker = rhythmmakertools.OutputIncisedRestFilledRhythmMaker(
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            c'4
            c'4
            c'8
        }
        {
            \time 5/8
            r2
            r8
        }
        {
            \time 5/8
            r8
            c'4
            c'4
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr8\n\t\tc'4\n\t\tc'4\n\t}\n}"


def test_OutputIncisedRestFilledRhythmMaker_03():

    prefix_talea, prefix_lengths = [], [0]
    suffix_talea, suffix_lengths = [], [0]
    talea_denominator = 4
    maker = rhythmmakertools.OutputIncisedRestFilledRhythmMaker(
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            r2
            r8
        }
        {
            \time 5/8
            r2
            r8
        }
        {
            \time 5/8
            r2
            r8
        }
    }
    '''

    assert staff.lilypond_format == '\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n}'


def test_OutputIncisedRestFilledRhythmMaker_04():

    prefix_talea, prefix_lengths = [1], [1]
    suffix_talea, suffix_lengths = [1], [1]
    talea_denominator = 8
    prolation_addenda = [1, 0, 3]
    maker = rhythmmakertools.OutputIncisedRestFilledRhythmMaker(
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator,
        prolation_addenda = prolation_addenda)

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 4/8
            \times 4/5 {
                c'8
                r2
            }
        }
        {
            \time 4/8
            {
                r2
            }
        }
        {
            \time 4/8
            \times 4/7 {
                r2.
                c'8
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/5 {\n\t\t\tc'8\n\t\t\tr2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/7 {\n\t\t\tr2.\n\t\t\tc'8\n\t\t}\n\t}\n}"


def test_OutputIncisedRestFilledRhythmMaker_05():

    prefix_talea, prefix_lengths = [1], [1]
    suffix_talea, suffix_lengths = [1], [1]
    talea_denominator = 8
    prolation_addenda =    [1, 0, 0, 0, 2]
    secondary_divisions = [3, 1, 4, 1, 3]
    maker = rhythmmakertools.OutputIncisedRestFilledRhythmMaker(
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator,
        prolation_addenda = prolation_addenda, secondary_divisions = secondary_divisions)

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 4/8
            \fraction \times 3/4 {
                c'8
                r4.
            }
            {
                r8
            }
        }
        {
            \time 4/8
            {
                r2
            }
        }
        {
            \time 4/8
            {
                r8
            }
            \fraction \times 3/5 {
                r2
                c'8
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tc'8\n\t\t\tr4.\n\t\t}\n\t\t{\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tr8\n\t\t}\n\t\t\\fraction \\times 3/5 {\n\t\t\tr2\n\t\t\tc'8\n\t\t}\n\t}\n}"
