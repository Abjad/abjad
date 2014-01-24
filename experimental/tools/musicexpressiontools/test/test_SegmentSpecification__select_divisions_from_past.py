# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_divisions_from_past_01():
    r'''From-past division select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_02():
    r'''From-past division select expression with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_03():
    r'''From-past division select expression with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_04():
    r'''From-past division select expression with reverse callbacks.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_from_past_05():
    r'''From-past division select expression with region break preservation.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[-1:]
    left_measure.timespan.set_divisions([(2, 16)])
    right_measure.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(5, 8), (6, 8)])
    red_voice_1_divisions = red_segment.select_divisions('Voice 1')
    blue_segment.set_divisions(red_voice_1_divisions, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
