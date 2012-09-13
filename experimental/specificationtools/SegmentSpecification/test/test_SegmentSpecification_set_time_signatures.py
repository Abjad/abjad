from abjad import *
from experimental import *
import py


def test_SegmentSpecification_set_time_signatures_01():
    '''Set-time 'reverse' keyword.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)], reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_time_signatures_02():
    '''Request-time 'reverse' keyword.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    reversed_red_time_signatures = segment.request_time_signatures(reverse=True)
    segment = score_specification.append_segment(name='blue')
    segment.set_time_signatures(reversed_red_time_signatures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_time_signatures_03():
    '''Request- and set-time 'reverse' keywords undo each other.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    reversed_red_time_signatures = segment.request_time_signatures(reverse=True)
    segment = score_specification.append_segment(name='blue')
    segment.set_time_signatures(reversed_red_time_signatures, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
