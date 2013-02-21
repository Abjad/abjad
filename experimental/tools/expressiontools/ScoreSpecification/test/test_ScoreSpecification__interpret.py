from abjad.tools import *
from experimental import *


def test_ScoreSpecification__interpret_01():
    '''Empty score specification interprets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    
    score = score_specification.interpret()

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


def test_ScoreSpecification__interpret_02():
    '''Empty score specification with empty segment specification interprets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification_1 = expressiontools.ScoreSpecification(score_template)

    score_1 = score_specification_1.interpret()

    score_specification_2 = expressiontools.ScoreSpecification(score_template)
    red_segment = score_specification_2.append_segment(name='red')
    score_2 = score_specification_2.interpret()

    assert score_1.lilypond_format == score_2.lilypond_format


def test_ScoreSpecification__interpret_03():
    '''Time signatures only.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    score = score_specification.interpret()

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
                        s1 * 1/2
                    }
                    {
                        s1 * 3/8
                    }
                }
            }
        >>
    >>
    '''

    assert score.lilypond_format == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context TimeSignatureContext = "TimeSignatureContext" {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\ts1 * 1/2\n\t\t}\n\t\t{\n\t\t\t\\time 3/8\n\t\t\ts1 * 3/8\n\t\t}\n\t}\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t\t{\n\t\t\t\t\ts1 * 1/2\n\t\t\t\t}\n\t\t\t\t{\n\t\t\t\t\ts1 * 3/8\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t>>\n>>'
