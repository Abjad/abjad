from experimental import *


def test_SegmentSpecification__select_divisions_from_past_01():
    '''From-past division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_02():
    '''From-past division selector with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_03():
    '''From-past division selector with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_04():
    '''From-past division selector with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_05():
    '''From-past division selector with region break preservation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    left = red_segment.select_measures('Voice 1')[:1]
    right = red_segment.select_measures('Voice 1')[-1:]
    left.timespan.set_divisions([(2, 16)])
    right.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(5, 8), (6, 8)])
    red_voice_1_divisions = red_segment.select_divisions('Voice 1')
    blue_segment.set_divisions(red_voice_1_divisions, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
