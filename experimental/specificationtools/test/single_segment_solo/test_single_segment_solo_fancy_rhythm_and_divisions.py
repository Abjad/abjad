from abjad import *
from experimental import *


def test_single_segment_solo_fancy_rhythm_and_divisions_01():
    '''Rhythm and divisions carve out same partial time signature selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures(3 * [(4, 8)])
    selector = segment.select_segment_offsets(start=(10, 16), stop=(13, 16))
    segment.set_divisions([(2, 32)], selector=selector)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_fancy_rhythm_and_divisions_02():
    '''Incomplete rhythm and division selectors overlap.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures(3 * [(4, 8)])
    selector = segment.select_segment_offsets(start=(10, 16), stop=(13, 16))
    segment.set_divisions([(2, 32)], selector=selector)
    selector = segment.select_segment_ratio_part((1, 2), -1)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_fancy_rhythm_and_divisions_03():
    '''Several different types of selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    selector = segment.select_segment_ratio_part((1, 1), 0)
    segment.set_divisions([(3, 16)], selector=selector)
    selector = segment.select_segment_ratio_part((1, 1), -1)
    segment.set_divisions([(2, 16)], selector=selector)
    selector = segment.select_divisions(stop=2)
    segment.set_rhythm(library.sixteenths, selector=selector)
    selector = segment.select_divisions(start=2)
    segment.set_rhythm(library.thirty_seconds, selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
