from experimental import *


def test_single_segment_solo__overlapping_division_selectors_01():
    '''Second division setting overwrites first division setting.
    Settings stop and start at same time.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_02():
    '''Second division setting overrides first division setting.
    First setting smaller than second setting.
    Settings start at same time.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    first_measure.timespan.set_divisions([(3, 16)])
    red_segment.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_03():
    '''Second division setting overrides first division setting.
    First setting smaller than second setting.
    First setting starts after second setting.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_divisions([(3, 16)])
    red_segment.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_04():
    '''Second division overlaps and shortens the first.
    Result is two separate division regions that both express in score.
    Both the (compositional) order of specification
    and the (temporal) order of performance matter in this example.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    last_measure = red_segment.select_measures('Voice 1')[1:2]
    red_segment.set_divisions([(3, 16)])
    last_measure.timespan.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_05():
    '''Second division sits in the middle of the first.
    Three division regions result.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    middle_measure = red_segment.select_measures('Voice 1')[1:2]
    red_segment.set_divisions([(3, 16)])
    middle_measure.timespan.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_06():
    '''Second division sits in the middle of the first.
    Three division regions result.
    Same as above but with a different select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    middle_measure = red_segment.timespan.divide_by_ratio((4, 3, 2))[1]
    red_segment.set_divisions([(3, 16)])
    middle_measure.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_07():
    '''Three division select expressions sitting exactly on top of each other.
    Only the topmost (ie, lexically last) is expressed.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(2, 16)])
    red_segment.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_08():
    '''Two fractional division select expressions sitting exactly on top of each other.
    Only the topmost is expressed.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    middle_measure = red_segment.select_measures('Voice 1')[1:2]
    middle_measure.timespan.set_divisions([(2, 16)])
    middle_measure.timespan.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_division_selectors_09():
    '''Two fractional division select expressions partially overlapping.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    red_segment = score_specification.append_segment(name='red') 
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    middle_measure = red_segment.select_measures('Voice 1')[1:2]
    middle_measure.timespan.set_divisions([(2, 16)])
    arbitrary_chunk = red_segment.timespan.set_offsets((5, 8), (6, 8))
    arbitrary_chunk.set_divisions([(1, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
