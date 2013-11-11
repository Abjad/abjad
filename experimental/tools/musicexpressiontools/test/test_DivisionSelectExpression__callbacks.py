# -*- encoding: utf-8 -*-
from experimental import *


def test_DivisionSelectExpression__callbacks_01():
    r'''Division get item.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    divisions = divisions[2:5]
    divisions.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_02():
    r'''Partition divisions by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    left, right = divisions.partition_by_ratio((1, 2))
    left.timespan.set_rhythm(library.sixteenths)
    right.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_03():
    r'''Partition divisions by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    left, right = divisions.partition_by_ratio_of_durations((1, 2))
    left.timespan.set_rhythm(library.sixteenths)
    right.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_04():
    r'''Repeat divisions to length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.repeat_to_length(2)
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_05():
    r'''Repeat divisions to duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.repeat_to_duration(Duration(6, 16))
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_06():
    r'''Reflect divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.reflect()
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_07():
    r'''Rotate divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.rotate(-1)
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_DivisionSelectExpression__callbacks_08():
    r'''Logical AND of divisions and timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    timespan = timespantools.Timespan(Offset(1, 16), Offset(9, 16))
    red_divisions = red_divisions & timespan
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
