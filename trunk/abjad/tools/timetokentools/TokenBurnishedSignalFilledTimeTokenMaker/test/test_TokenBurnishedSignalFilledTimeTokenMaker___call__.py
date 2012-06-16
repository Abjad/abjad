from abjad import *
from abjad.tools import sequencetools
from abjad.tools import timetokentools


def test_TokenBurnishedSignalFilledTimeTokenMaker___call___01():

    pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [0]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [2], [1]
    maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)

    duration_tokens = [(5, 16), (6, 16)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                r32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            {
                r16
                r8
                c'32
                c'32
                c'16
                r16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\t{\n\t\t\tr32\n\t\t\tr32\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tc'32\n\t\t\tr32\n\t\t}\n\t}\n\t{\n\t\t\\time 6/16\n\t\t{\n\t\t\tr16\n\t\t\tr8\n\t\t\tc'32\n\t\t\tc'32\n\t\t\tc'16\n\t\t\tr16\n\t\t}\n\t}\n}"


def test_TokenBurnishedSignalFilledTimeTokenMaker___call___02():

    pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [0]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [2], [1]
    maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    duration_tokens = [(5, 16), (6, 16)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                c'32
                c'32
                r16
                r8
                r32
                c'32
            }
        }
        {
            \time 6/16
            {
                c'16
                c'8
                r32
                r32
                r16
                c'16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\t{\n\t\t\tc'32\n\t\t\tc'32\n\t\t\tr16\n\t\t\tr8\n\t\t\tr32\n\t\t\tc'32\n\t\t}\n\t}\n\t{\n\t\t\\time 6/16\n\t\t{\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tr32\n\t\t\tr32\n\t\t\tr16\n\t\t\tc'16\n\t\t}\n\t}\n}"


def test_TokenBurnishedSignalFilledTimeTokenMaker___call___03():

    pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [3]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [2], [1]
    maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    duration_tokens = [(5, 16), (6, 16)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            \fraction \times 10/13 {
                c'32
                c'32
                r16
                r8
                r32
                r32
                r16
                c'32
            }
        }
        {
            \time 6/16
            \times 4/5 {
                c'16.
                c'32
                r32
                r16
                r8
                r32
                r32
                c'16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\t\\fraction \\times 10/13 {\n\t\t\tc'32\n\t\t\tc'32\n\t\t\tr16\n\t\t\tr8\n\t\t\tr32\n\t\t\tr32\n\t\t\tr16\n\t\t\tc'32\n\t\t}\n\t}\n\t{\n\t\t\\time 6/16\n\t\t\\times 4/5 {\n\t\t\tc'16.\n\t\t\tc'32\n\t\t\tr32\n\t\t\tr16\n\t\t\tr8\n\t\t\tr32\n\t\t\tr32\n\t\t\tc'16\n\t\t}\n\t}\n}"


def test_TokenBurnishedSignalFilledTimeTokenMaker___call___04():

    pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    duration_tokens = [(5, 16), (6, 16)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                c'32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            \times 4/5 {
                r16
                c'8
                c'32
                c'32
                c'16
                c'8
                r32
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\t{\n\t\t\tr32\n\t\t\tc'32\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tc'32\n\t\t\tr32\n\t\t}\n\t}\n\t{\n\t\t\\time 6/16\n\t\t\\times 4/5 {\n\t\t\tr16\n\t\t\tc'8\n\t\t\tc'32\n\t\t\tc'32\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tr32\n\t\t}\n\t}\n}"


def test_TokenBurnishedSignalFilledTimeTokenMaker___call___05():

    pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    secondary_divisions = [14]
    maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths, secondary_divisions)

    duration_tokens = [(5, 16), (6, 16)]
    music = maker(duration_tokens)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                c'32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            \times 4/7 {
                r16
                c'8
                r32
            }
            {
                r32
                c'16
                c'8
                r32
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\t{\n\t\t\tr32\n\t\t\tc'32\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tc'32\n\t\t\tr32\n\t\t}\n\t}\n\t{\n\t\t\\time 6/16\n\t\t\\times 4/7 {\n\t\t\tr16\n\t\t\tc'8\n\t\t\tr32\n\t\t}\n\t\t{\n\t\t\tr32\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tr32\n\t\t}\n\t}\n}"
