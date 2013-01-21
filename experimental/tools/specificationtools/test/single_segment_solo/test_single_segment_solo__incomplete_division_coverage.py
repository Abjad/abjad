from experimental import *


def test_single_segment_solo__incomplete_division_coverage_01():
    '''Divisions cover only middle measure.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_02():
    '''Divisions cover only first and last measures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_03():
    '''Contexts and selector work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_divisions([(2, 16)])
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_04():
    '''Contexts and selector work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_05():
    '''One selector partially covers the other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_06():
    '''One selector partially covers the other. Works with contexts.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_07():
    '''One selector more important than the other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_08():
    '''Division selector cuts fractional chunks out of time signatures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    selector = red_segment.timespan.set_offsets((10, 16), (13, 16))
    selector.set_divisions([(2, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
