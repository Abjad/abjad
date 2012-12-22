from abjad import *
from experimental.tools import *


def test_single_segment_solo__fancy_rhythm_and_divisions_01():
    '''Rhythm and divisions carve out same partial time signature selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    selector = red_segment.set_offsets((10, 16), (13, 16))
    selector.set_divisions([(2, 32)])
    selector.set_rhythm(library.thirty_seconds)
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
    selector = red_segment.set_offsets((10, 16), (13, 16))
    selector.set_divisions([(2, 32)])
    selector = red_segment.divide_by_ratio((1, 2))[-1]
    selector.set_rhythm(library.thirty_seconds)
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
    left.set_divisions([(3, 16)])
    right.set_divisions([(2, 16)])
    selector = red_segment.select_divisions('Voice 1', stop=2)
    selector.set_rhythm(library.sixteenths)
    selector = red_segment.select_divisions('Voice 1', start=2)
    selector.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
