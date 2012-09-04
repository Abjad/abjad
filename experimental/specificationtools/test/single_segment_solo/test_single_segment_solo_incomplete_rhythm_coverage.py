from abjad import *
from experimental import *


def test_single_segment_solo_incomplete_rhythm_coverage_01():
    '''Rhythm covers only middle measure.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    selector = segment.select_background_measure(1)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_incomplete_rhythm_coverage_02():
    '''Rhythm covers only first and last measures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    selector = segment.select_background_measure(0)
    segment.set_rhythm(library.sixteenths, selector=selector)
    selector = segment.select_background_measure(-1)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_incomplete_rhythm_coverage_03():
    '''Contexts and selector work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    selector = segment.select_background_measure(1)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    segment.set_rhythm(library.sixteenths, contexts=['Voice 1'], selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_incomplete_rhythm_coverage_04():
    '''Contexts and selector work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    selector = segment.select_background_measure(0)
    segment.set_rhythm(library.sixteenths, selector=selector)
    selector = segment.select_background_measure(-1)
    segment.set_rhythm(library.thirty_seconds, contexts=['Voice 1'], selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
