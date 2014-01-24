# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_solo__fancy_rhythm_and_divisions_01():
    r'''Rhythm and divisions carve out same partial time signature 
    select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    select_expression = red_segment.timespan.set_offsets((10, 16), (13, 16))
    select_expression.set_divisions([(2, 32)])
    select_expression.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__fancy_rhythm_and_divisions_02():
    r'''Incomplete rhythm and division select expressions overlap.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    select_expression = red_segment.timespan.set_offsets((10, 16), (13, 16))
    select_expression.set_divisions([(2, 32)])
    select_expression = red_segment.timespan.divide_by_ratio((1, 2))[-1]
    select_expression.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__fancy_rhythm_and_divisions_03():
    r'''Several different types of select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    left, right = red_segment.timespan.divide_by_ratio((1, 1))
    left.set_divisions([(3, 16)])
    right.set_divisions([(2, 16)])
    select_expression = red_segment.select_divisions('Voice 1')[:2]
    select_expression.timespan.set_rhythm(library.joined_sixteenths)
    select_expression = red_segment.select_divisions('Voice 1')[2:]
    select_expression.timespan.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
