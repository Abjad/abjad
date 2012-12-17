from abjad import *
from experimental import *


def test_single_segment_solo__fancy_rhythm_and_divisions_01():
    '''Rhythm and divisions carve out same partial time signature selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    selector = red_segment.adjust_timespan_offsets(start=(10, 16), stop=(13, 16))
    red_segment.set_divisions([(2, 32)], timespan=selector)
    red_segment.set_rhythm(library.thirty_seconds, timespan=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__fancy_rhythm_and_divisions_02():
    '''Incomplete rhythm and division selectors overlap.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    selector = red_segment.adjust_timespan_offsets(start=(10, 16), stop=(13, 16))
    red_segment.set_divisions([(2, 32)], timespan=selector)
    selector = red_segment.divide_by_ratio((1, 2))[-1]
    red_segment.set_rhythm(library.thirty_seconds, timespan=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__fancy_rhythm_and_divisions_03():
    '''Several different types of selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    left, right = red_segment.divide_by_ratio((1, 1))
    red_segment.set_divisions([(3, 16)], timespan=left)
    red_segment.set_divisions([(2, 16)], timespan=right)
    selector = red_segment.select_divisions('Voice 1', stop=2)
    red_segment.set_rhythm(library.sixteenths, timespan=selector)
    selector = red_segment.select_divisions('Voice 1', start=2)
    red_segment.set_rhythm(library.thirty_seconds, timespan=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
