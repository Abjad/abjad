from experimental import *


def test_single_segment_solo__incomplete_rhythm_coverage_01():
    '''Rhythm covers only middle measure.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_02():
    '''Rhythm covers only first and last measures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_03():
    '''Contexts and select expression work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_rhythm(library.thirty_seconds)
    measures.timespan.set_rhythm(library.sixteenths, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_04():
    '''Contexts and select expression work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_rhythm(library.thirty_seconds, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_05():
    '''One select expression partially covers the other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_06():
    '''One select expression partially covers the other. Works with contexts.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_rhythm(library.thirty_seconds, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_rhythm_coverage_07():
    '''One select expression more important than the other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_rhythm(library.sixteenths, contexts=['Voice 1'])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
