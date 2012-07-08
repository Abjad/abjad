from abjad.tools import *
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification


def test_ScoreSpecification_interpret_01():
    '''Empty score specification interprets.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
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

    specification_1 = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    score_1 = specification_1.interpret()

    specification_2 = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification_2.append_segment()
    score_2 = specification_2.interpret()

    assert score_1.lilypond_format == score_2.lilypond_format


def test_ScoreSpecification_interpret_03():
    '''Time signatures only.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

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
#    segment.set_tempo(segment, 108)
#    segment.set_time_signatures(segment, [(2, 8), (2, 8), (3, 8), (2, 8), (3, 8)])
#    segment.set_aggregate(segment, [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])
#    segment.set_pitch_classes_timewise(segment, [0, 8, 9, 11, 1, 2, 4, 6, 3, 5, 7, 10])
#    segment.set_rhythm(segment.vn1, (repeated_quarter_divisions_right, thirty_seconds))
#    segment.set_register(segment.vn1, cello_treble)
#    segment.set_dynamics(segment.vn1, terraced_fortissimo)
#    segment.set_rhythm(segment.vn2, (repeated_quarter_divisions_right, thirty_seconds))
#    segment.set_register(segment.vn2, cello_treble)
#    segment.set_dynamics(segment.vn2, terraced_fortissimo)
