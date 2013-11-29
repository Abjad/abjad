# -*- encoding: utf-8 -*-
from experimental import *


def test_CounttimeComponentSelectExpression__time_relation_01():
    r'''Red starts during blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_starts_during_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_02():
    r'''Red stops during blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_stops_during_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_03():
    r'''Red intersects blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_intersects_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_04():
    r'''Red overlaps start of blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_overlaps_start_of_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_05():
    r'''Red overlaps stop of blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_overlaps_stop_of_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_06():
    r'''Red trisects blue.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_leaf_color('blue')
    time_relation = timespantools.timespan_2_trisects_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
