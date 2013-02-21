from experimental import *
import py


def test_SegmentSpecification__select_measures_01():
    '''Negative start.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
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
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
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
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
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
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
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
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
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
    '''Measure select expression dependent on divided timespan.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half = red_segment.timespan.divide_by_ratio((1, 1))[0]
    left_measures = left_half.select_measures('Voice 1')
    left_measures.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_07():
    '''Measure select expression dependent on divided timespan.
    Order of set expressions matters.
    First measure of right set expression covers last measure of left set expression.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half, right_half = red_segment.timespan.divide_by_ratio((1, 1))
    left_measures = left_half.select_measures('Voice 1')
    right_measures = right_half.select_measures('Voice 1')
    left_measures.timespan.set_rhythm(library.eighths)
    right_measures.timespan.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_08():
    '''Measure select expression dependent on divided timespan.
    Order of set expressions matters.
    Last measure of left set expression covers first measure of right set expression.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half, right_half = red_segment.timespan.divide_by_ratio((1, 1))
    left_measures = left_half.select_measures('Voice 1')
    right_measures = right_half.select_measures('Voice 1')
    right_measures.timespan.set_rhythm(library.sixteenths)
    left_measures.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_09():
    '''Measure select expression dependent on divided timespan.
    With explicit time-relation.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half = red_segment.timespan.divide_by_ratio((1, 1))[0]
    time_relation = timerelationtools.timespan_2_stops_during_timespan_1()
    left_measures = left_half.select_measures('Voice 1', time_relation=time_relation)
    left_measures.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_10():
    '''Measure select expression dependent on divided timespan.
    With explicit time-relation.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    left_half = red_segment.timespan.divide_by_ratio((1, 1))[0]
    time_relation = timerelationtools.timespan_2_overlaps_stop_of_timespan_1()
    left_measures = left_half.select_measures('Voice 1', time_relation=time_relation)
    left_measures.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_11():
    '''Measure select expression with composed getitem callbacks.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(2, 8), (3, 8), (4, 8), (5, 8)])
    red_segment.set_rhythm(library.eighths)
    measures = red_segment.select_measures('Voice 1')[2:6][1:3]
    measures.timespan.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_12():
    '''Measure select expression with composed getitem and partition callbacks.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8)])
    red_segment.set_rhythm(library.eighths)
    measures = red_segment.select_measures('Voice 1')
    measures = measures.partition_by_ratio((1, 1, 1))[1]
    measures = measures[:2]
    measures.timespan.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_measures_13():
    '''Measure select expression with composed partition and getitem callbacks.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8)])
    red_segment.set_rhythm(library.eighths)
    measures = red_segment.select_measures('Voice 1')
    measures = measures[2:8]
    measures = measures.partition_by_ratio((1, 1, 1))[1]
    measures.timespan.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
