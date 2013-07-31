# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_rhythm_from_future_01():
    r'''From-future rhythm select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
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
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_02():
    r'''From-future rhythm select expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reflect()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_03():
    r'''From-future rhythm select expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reflect()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_from_future_04():
    r'''From-future rhythm select expression with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    blue_rhythm = blue_rhythm.reflect()
    blue_rhythm = blue_rhythm.reflect()
    red_segment.set_rhythm(blue_rhythm)
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_rhythm(library.dotted_sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
