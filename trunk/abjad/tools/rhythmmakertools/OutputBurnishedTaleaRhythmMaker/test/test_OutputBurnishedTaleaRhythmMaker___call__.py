from abjad import *
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def test_OutputBurnishedTaleaRhythmMaker___call___01():

    talea, talea_denominator, prolation_addenda = [1], 16, [2]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [1], [1]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)

    divisions = [(3, 16), (3, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 3/16
            \fraction \times 3/5 {
                c'16
                r16
                r16
                r16
                r16
            }
        }
        {
            \time 3/8
            \fraction \times 3/4 {
                r16
                r16
                r16
                r16
                r16
                r16
                r16
                c'16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\t\\fraction \\times 3/5 {\n\t\t\tc'16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tc'16\n\t\t}\n\t}\n}"


def test_OutputBurnishedTaleaRhythmMaker___call___02():

    talea, talea_denominator, prolation_addenda = [1], 4, [2]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)

    divisions = [(3, 16), (3, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 3/16
            \fraction \times 3/5 {
                r4
                c'16
            }
        }
        {
            \time 3/8
            \fraction \times 3/4 {
                c'8.
                c'4
                r16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\t\\fraction \\times 3/5 {\n\t\t\tr4\n\t\t\tc'16\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tc'8.\n\t\t\tc'4\n\t\t\tr16\n\t\t}\n\t}\n}"


def test_OutputBurnishedTaleaRhythmMaker___call___03():

    talea, talea_denominator, prolation_addenda = [1, 2, 3], 16, [0, 2]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    secondary_divisions = [9]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths, secondary_divisions)

    divisions = [(3, 8), (4, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 3/8
            {
                r16
                c'8
                c'8.
            }
        }
        {
            \time 4/8
            \fraction \times 3/5 {
                c'16
                c'8
                c'8
            }
            {
                c'16
                c'16
                c'8
                r16
            }
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/8\n\t\t{\n\t\t\tr16\n\t\t\tc'8\n\t\t\tc'8.\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t\\fraction \\times 3/5 {\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tc'8\n\t\t}\n\t\t{\n\t\t\tc'16\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tr16\n\t\t}\n\t}\n}"


def test_OutputBurnishedTaleaRhythmMaker___call___04():

    talea, talea_denominator, prolation_addenda  = [1], 8, []
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [2]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda,
        lefts, middles, rights,
        left_lengths, right_lengths)

    divisions = [(8, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 8/8
            r8
            c'8
            c'8
            c'8
            c'8
            c'8
            r8
            r8
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 8/8\n\t\tr8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tr8\n\t\tr8\n\t}\n}"
