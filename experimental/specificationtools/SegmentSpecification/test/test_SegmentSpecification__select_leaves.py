from abjad import *
from experimental import *


def test_SegmentSpecification__select_leaves_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    timespan = red_segment.select_leaves(start=2, stop=4)
    rhythm = red_segment.request_rhythm('Voice 1', timespan=timespan)
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures(0, 1)
    second_measure = red_segment.select_background_measures(1, 2)
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'], selector=first_measure)
    cell = red_segment.request_rhythm('Voice 1', timespan=first_measure)
    red_segment.set_rhythm(cell, contexts=['Voice 1'], selector=second_measure, rotation=Duration(-1, 32))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves(start=4, stop=7)
    voice_1_rhythm = red_segment.request_rhythm('Voice 1', timespan=timespan)
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_03():
    '''Leaves select correctly across offset-positioned rhythm expression boundaries.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures(0, 1)
    second_measure = red_segment.select_background_measures(1, 2)
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'], selector=first_measure)
    cell = red_segment.request_rhythm('Voice 1', timespan=first_measure)
    red_segment.set_rhythm(cell, contexts=['Voice 1'], selector=second_measure, rotation=Duration(-1, 32))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves(start=4, stop=8)
    voice_1_rhythm = red_segment.request_rhythm('Voice 1', timespan=timespan)
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
