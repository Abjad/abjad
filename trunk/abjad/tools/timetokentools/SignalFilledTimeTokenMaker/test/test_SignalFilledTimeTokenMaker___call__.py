from abjad import *
from abjad.tools import sequencetools
from abjad.tools import timetokentools


def test_SignalFilledTimeTokenMaker___call___01():

    pattern, denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
    maker = timetokentools.SignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda)

    duration_tokens = [(2, 8), (5, 8)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/7 {
                r16
                c'4
                r8
            }
        }
        {
            \time 5/8
            \fraction \times 5/7 {
                c'8.
                r16
                c'4
                r8
                c'8.
                r16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\times 4/7 {\n\t\t\tr16\n\t\t\tc'4\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\time 5/8\n\t\t\\fraction \\times 5/7 {\n\t\t\tc'8.\n\t\t\tr16\n\t\t\tc'4\n\t\t\tr8\n\t\t\tc'8.\n\t\t\tr16\n\t\t}\n\t}\n}"


def test_SignalFilledTimeTokenMaker___call___02():

    pattern, denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
    secondary_divisions = [6]
    maker = timetokentools.SignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda, secondary_divisions)

    duration_tokens = [(2, 8), (5, 8)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/7 {
                r16
                c'4
                r8
            }
        }
        {
            \time 5/8
            {
                c'8
            }
            \times 2/3 {
                c'16
                r16
                c'4
                r8
                c'16
            }
            {
                c'8
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\times 4/7 {\n\t\t\tr16\n\t\t\tc'4\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\time 5/8\n\t\t{\n\t\t\tc'8\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\tr16\n\t\t\tc'4\n\t\t\tr8\n\t\t\tc'16\n\t\t}\n\t\t{\n\t\t\tc'8\n\t\t}\n\t}\n}"
