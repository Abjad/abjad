from experimental import *
import py


def test_SegmentSpecification__select_measures_01():
    '''Negative start.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    last_two_measures = red_segment.select_measures('Voice 1')[-2:]
    red_segment.set_divisions([(2, 32)])
    last_two_measures.timespan.set_divisions([(3, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_02():
    '''Negative stop.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    first_two_measures = red_segment.select_measures('Voice 1')[:-1]
    red_segment.set_divisions([(2, 32)])
    first_two_measures.timespan.set_divisions([(3, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_03():
    '''Negative start and stop.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    middle_measure = red_segment.select_measures('Voice 1')[1:-1]
    red_segment.set_divisions([(2, 32)])
    middle_measure.timespan.set_divisions([(3, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_04():
    '''Negative index.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    last_measure = red_segment.select_measures('Voice 1')[-1:]
    red_segment.set_divisions([(2, 32)])
    last_measure.timespan.set_divisions([(3, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_05():
    '''Positive index.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    last_measure = red_segment.select_measures('Voice 1')[1:2]
    red_segment.set_divisions([(2, 32)])
    last_measure.timespan.set_divisions([(3, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_06():
    '''Select measures that start during duration shard.
    '''
    py.test.skip('working on this one')
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half, right_half = red_segment.timespan.divide_by_ratio((1, 1))
    left_measures = left_half.select_measures('Voice 1')
    right_measures = right_half.select_measures('Voice 1')
    left_measures.timespan.set_rhythm(library.eighths)
    right_measures.timespan.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
