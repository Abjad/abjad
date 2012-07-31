from abjad.tools import *
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification


def test_ScoreSpecification_interpret_01():
    '''Empty score specification interprets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)
    
    score = specification.interpret()

    r'''
    \context Score = "Grouped Rhythmic Staves Score" <<
        \context TimeSignatureContext = "TimeSignatureContext" {
        }
        \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
            \context RhythmicStaff = "Staff 1" {
                \context Voice = "Voice 1" {
                }
            }
        >>
    >>
    '''

    assert score.lilypond_format == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context TimeSignatureContext = "TimeSignatureContext" {\n\t}\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t}\n\t\t}\n\t>>\n>>'


def test_ScoreSpecification_interpret_02():
    '''Empty score specification with empty segment specification interprets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification_1 = ScoreSpecification(score_template)

    score_1 = specification_1.interpret()

    specification_2 = ScoreSpecification(score_template)
    segment = specification_2.append_segment()
    score_2 = specification_2.interpret()

    assert score_1.lilypond_format == score_2.lilypond_format


def test_ScoreSpecification_interpret_03():
    '''Time signatures only.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    segment.set_time_signatures([(4, 8), (3, 8)])

    score = specification.interpret()

    r'''
    \context Score = "Grouped Rhythmic Staves Score" <<
        \context TimeSignatureContext = "TimeSignatureContext" {
            {
                \time 4/8
                s1 * 1/2
            }
            {
                \time 3/8
                s1 * 3/8
            }
        }
        \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
            \context RhythmicStaff = "Staff 1" {
                \context Voice = "Voice 1" {
                    {
                        r2
                    }
                    {
                        r4.
                    }
                }
            }
        >>
    >>
    '''

    assert score.lilypond_format == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context TimeSignatureContext = "TimeSignatureContext" {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\ts1 * 1/2\n\t\t}\n\t\t{\n\t\t\t\\time 3/8\n\t\t\ts1 * 3/8\n\t\t}\n\t}\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t\t{\n\t\t\t\t\tr2\n\t\t\t\t}\n\t\t\t\t{\n\t\t\t\t\tr4.\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t>>\n>>'


#def test_ScoreSpecification_interpret_04():
#    py.test.skip('unskip after integrating pitch.')
#
#    specification = ScoreSpecification(scoretemplatetools.StringQuartetScoreTemplate)
#
#    segment = specification.append_segment(name='A')
#    segment.set_tempo(108)
#    segment.set_time_signatures([(2, 8), (2, 8), (3, 8), (2, 8), (3, 8)])
#    segment.set_aggregate([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])
#    segment.set_pitch_classes_timewise([0, 8, 9, 11, 1, 2, 4, 6, 3, 5, 7, 10])
#    segment.set_rhythm((repeated_quarter_divisions_right, thirty_seconds), contexts=segment.vn1)
#    segment.set_registration(cello_treble, contexts=segment.vn1)
#    segment.set_dynamics(terraced_fortissimo, contexts=segment.vn1)
#    segment.set_rhythm((repeated_quarter_divisions_right, thirty_seconds), contexts=segment.vn2)
#    segment.set_registration(cello_treble, contexts=segment.vn2)
#    segment.set_dynamics(terraced_fortissimo, contexts=segment.vn2)
