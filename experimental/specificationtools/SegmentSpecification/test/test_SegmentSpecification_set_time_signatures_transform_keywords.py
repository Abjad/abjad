from abjad import *
from experimental import *


def test_SegmentSpecification_set_time_signatures_transform_keywords_01():
    '''Time signature 'index' transform.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)], index=-2)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_time_signatures_transform_keywords_02():
    '''Time signature 'count' transform.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)], count=6)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_time_signatures_transform_keywords_03():
    '''Time signature 'reverse' transform.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)], reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_time_signatures_transform_keywords_04():
    '''Time signature 'rotation' transform.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)], rotation=-2)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
