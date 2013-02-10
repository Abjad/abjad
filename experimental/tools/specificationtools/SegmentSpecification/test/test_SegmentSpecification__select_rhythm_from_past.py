from experimental import *


def test_SegmentSpecification__select_rhythm_from_past_01():
    '''From-past rhythm select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_02():
    '''From-past rhythm select expression.

    Fit larger source_expression into smaller target.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(8, 8)])
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_03():
    '''From-past rhythm select expression with reverse callback.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    red_voice_1_rhythm = red_voice_1_rhythm.reflect()
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_04():
    '''From-past rhythm select expression with reverse callback.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    red_voice_1_rhythm = red_voice_1_rhythm.reflect()
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_05():
    '''From-past rhythm select expression with reverse callbacks.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    red_voice_1_rhythm = red_voice_1_rhythm.reflect()
    red_voice_1_rhythm = red_voice_1_rhythm.reflect()
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_06():
    '''From-past rhythm select expression with rotation.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    red_voice_1_rhythm = red_voice_1_rhythm.rotate(8)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_07():
    '''From-past rhythm select expression with rotation callback.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm.rotate(8), contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_08():
    '''From-past rhythm select expression with paired rotation.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.select_leaves('Voice 1')
    red_voice_1_rhythm = red_voice_1_rhythm.rotate(8)
    red_voice_1_rhythm = red_voice_1_rhythm.rotate(-8)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_past_09():
    '''From-past rhythm select expression.

    Repeat smaller source_expression to filler larger target.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(6, 8), (9, 8)])
    red_rhythm = red_segment.select_leaves('Voice 1')
    blue_segment.set_rhythm(red_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
