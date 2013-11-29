# -*- encoding: utf-8 -*-
from experimental import *
import pytest


def test_SegmentSpecification__select_beats_01():
    r'''Set red segment divisions to red segment beats.
    Set blue segment divisions to blue segment beats.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_02():
    r'''Set both segments' divisions to red segment beats.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_segment.set_divisions(red_beats)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_03():
    r'''Set both segments' divisions to blue segment beats.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    score_specification.set_rhythm(library.sixteenths)
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    blue_beats = blue_segment.select_beats('Voice 1')
    red_segment.set_divisions(blue_beats)
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_segment.set_divisions(blue_beats)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_04():
    r'''Single-integer positive beat getitem index.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    beat = blue_segment.select_beats('Voice 1')[2]
    beat.timespan.select_leaves('Voice 1').set_spanner(spannertools.Slur())
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_05():
    r'''Single-integer negative beat getitem index.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    beat = blue_segment.select_beats('Voice 1')[-2]
    beat.timespan.select_leaves('Voice 1').set_spanner(spannertools.Slur())
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_06():
    r'''Select beats that start during explicit timespan.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    timespan = red_segment.timespan
    timespan = timespan.set_offsets(Offset(1, 16), Offset(5, 16))
    beats = timespan.select_beats('Voice 1')
    beats.select_leaves('Voice 1').set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_07():
    r'''Select beats that stop during explicit timespan.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    timespan = red_segment.timespan
    timespan = timespan.set_offsets(Offset(1, 16), Offset(5, 16))
    time_relation = timespantools.timespan_2_stops_during_timespan_1()
    beats = timespan.select_beats('Voice 1', time_relation=time_relation)
    beats.select_leaves('Voice 1').set_leaf_color('red')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
