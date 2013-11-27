# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_solo__incomplete_division_coverage_01():
    r'''Divisions cover only middle measure.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_02():
    r'''Divisions cover only first and last measures.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_03():
    r'''Contexts and select expression work together.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_divisions([(2, 16)])
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_04():
    r'''Contexts and select expression work together.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[:1]
    measures.timespan.set_divisions([(3, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_05():
    r'''One select expression partially covers the other.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_06():
    r'''One select expression partially covers the other. Works with contexts.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_07():
    r'''One select expression more important than the other.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')[-2:]
    measures.timespan.set_divisions([(2, 16)], contexts=['Voice 1'])
    measures = red_segment.select_measures('Voice 1')[-1:]
    measures.timespan.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__incomplete_division_coverage_08():
    r'''Division select expression cuts fractional chunks out of time signatures.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(4, 8)])
    select_expression = red_segment.timespan.set_offsets((10, 16), (13, 16))
    select_expression.set_divisions([(2, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
