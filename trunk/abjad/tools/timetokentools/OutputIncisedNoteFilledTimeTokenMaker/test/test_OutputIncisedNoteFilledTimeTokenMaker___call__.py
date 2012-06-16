from abjad import *
from abjad.tools import sequencetools
from abjad.tools import timetokentools


def test_OutputIncisedNoteFilledTimeTokenMaker___call___01():

    prefix_signal, prefix_lengths = [-8], [2]
    suffix_signal, suffix_lengths = [-3], [4]
    denominator = 32
    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker(
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    duration_tokens = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            r4
            r4
            c'8
        }
        {
            \time 5/8
            c'2
            c'8
        }
        {
            \time 5/8
            c'4
            r16.
            r16.
            r16.
            r16.
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tr4\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tr16.\n\t\tr16.\n\t\tr16.\n\t\tr16.\n\t}\n}"


def test_OutputIncisedNoteFilledTimeTokenMaker___call___02():

    prefix_signal, prefix_lengths = [-1], [20]
    suffix_signal, suffix_lengths = [-1], [2]
    denominator = 4
    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker(
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    duration_tokens = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            r4
            r4
            r8
        }
        {
            \time 5/8
            c'2
            c'8
        }
        {
            \time 5/8
            c'8
            r4
            r4
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tr4\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'8\n\t\tr4\n\t\tr4\n\t}\n}"


def test_OutputIncisedNoteFilledTimeTokenMaker___call___03():

    prefix_signal, prefix_lengths = [], [0]
    suffix_signal, suffix_lengths = [], [0]
    denominator = 4
    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker(
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    duration_tokens = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 5/8
            c'2
            c'8
        }
        {
            \time 5/8
            c'2
            c'8
        }
        {
            \time 5/8
            c'2
            c'8
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n}"


def test_OutputIncisedNoteFilledTimeTokenMaker___call___04():

    prefix_signal, prefix_lengths = [-1], [1]
    suffix_signal, suffix_lengths = [-1], [1]
    denominator = 8
    prolation_addenda = [1, 0, 3]
    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker(
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator,
        prolation_addenda = prolation_addenda)

    duration_tokens = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 4/8
            \times 4/5 {
                r8
                c'2
            }
        }
        {
            \time 4/8
            {
                c'2
            }
        }
        {
            \time 4/8
            \times 4/7 {
                c'2.
                r8
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/5 {\n\t\t\tr8\n\t\t\tc'2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tc'2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/7 {\n\t\t\tc'2.\n\t\t\tr8\n\t\t}\n\t}\n}"


def test_OutputIncisedNoteFilledTimeTokenMaker___call___05():

    prefix_signal, prefix_lengths = [-1], [1]
    suffix_signal, suffix_lengths = [-1], [1]
    denominator = 8
    prolation_addenda =    [1, 0, 0, 0, 2]
    secondary_divisions = [3, 1, 4, 1, 3]
    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker(
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator,
        prolation_addenda = prolation_addenda, secondary_divisions = secondary_divisions)

    duration_tokens = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 4/8
            \fraction \times 3/4 {
                r8
                c'4.
            }
            {
                c'8
            }
        }
        {
            \time 4/8
            {
                c'2
            }
        }
        {
            \time 4/8
            {
                c'8
            }
            \fraction \times 3/5 {
                c'2
                r8
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tr8\n\t\t\tc'4.\n\t\t}\n\t\t{\n\t\t\tc'8\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tc'2\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tc'8\n\t\t}\n\t\t\\fraction \\times 3/5 {\n\t\t\tc'2\n\t\t\tr8\n\t\t}\n\t}\n}"
