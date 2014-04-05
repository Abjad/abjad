# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_offsets_01():
    r'''Explicit offsets.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment= red_segment.timespan.set_offsets((1, 8), (4, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_02():
    r'''Implicit start-offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = red_segment.timespan.set_offsets(stop_offset=(4, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_03():
    r'''Implicit stop-offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = red_segment.timespan.set_offsets(start_offset=(2, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_04():
    r'''Implicit start- and stop-offsets.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_05():
    r'''Negative start-offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(start_offset=(-4, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_06():
    r'''Negative stop-offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(stop_offset=(-2, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_07():
    r'''Negative start and stop-offsets.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(start_offset=(-4, 8), stop_offset=(-2, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)