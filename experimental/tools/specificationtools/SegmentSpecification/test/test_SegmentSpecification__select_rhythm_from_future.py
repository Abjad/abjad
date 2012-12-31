from abjad import *
from experimental.tools import *


def test_SegmentSpecification__select_rhythm_from_future_01():
    '''From-future rhythm material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_02():
    '''From-future rhythm material request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reverse()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_03():
    '''From-future rhythm material request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reverse()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_04():
    '''From-future rhythm material request with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reverse()
    blue_rhythm = blue_rhythm.reverse()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
