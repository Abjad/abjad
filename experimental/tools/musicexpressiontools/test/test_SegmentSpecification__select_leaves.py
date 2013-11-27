# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_leaves_01():
    r'''Select leaves composited on leaf select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    rhythm = red_segment.select_leaves('Voice 1')[2:4]
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_02():
    r'''Rotate leaf select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    leaves = red_segment.select_leaves('Voice 1')[4:7]
    voice_1_rhythm = leaves.timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_03():
    r'''Leaves select correctly across rhythm payload expression boundaries.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    voice_1_rhythm = red_segment.select_leaves('Voice 1')[4:8]
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_04():
    r'''Select one division's leaves.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(6, 32)], contexts=['Voice 1'])
    maker = rhythmmakertools.TaleaRhythmMaker([1, 2, 3], 32)
    maker.beam_cells_together = True
    red_segment.set_rhythm(maker, contexts=['Voice 1'])
    first_division = red_segment.select_divisions('Voice 1')[:1]
    red_rhythm_cell = first_division.timespan.select_leaves('Voice 1')
    red_rhythm_cell = red_rhythm_cell.reflect()
    red_segment.set_rhythm(red_rhythm_cell, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_05():
    r'''Select leaves that start during measure 1 + 1.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.note_tokens)
    measure = red_segment.select_measures('Voice 1')[1]
    measure.select_leaves('Voice 1').set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_06():
    r'''Select leaves that stop during measure 1 + 1.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.note_tokens)
    measure = red_segment.select_measures('Voice 1')[1]
    time_relation = timerelationtools.timespan_2_stops_during_timespan_1()
    measure.select_leaves('Voice 1', time_relation=time_relation).set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_07():
    r'''Select leaves that intersect measure 1 + 1.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.note_tokens)
    measure = red_segment.select_measures('Voice 1')[1]
    time_relation = timerelationtools.timespan_2_intersects_timespan_1()
    measure.select_leaves('Voice 1', time_relation=time_relation).set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
