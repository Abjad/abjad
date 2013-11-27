# -*- encoding: utf-8 -*-
from experimental import *


def test_TimespanExpression__callbacks_01():
    r'''Scale timespan.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.scale(Multiplier(4))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_02():
    r'''Set timespan duration.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.set_duration(Duration(2, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_03():
    r'''Set timespan start offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.set_offsets(start_offset=Offset(1, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_04():
    r'''Set timespan stop offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.set_offsets(stop_offset=Offset(2, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_05():
    r'''Translate timespan.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.translate_offsets(Duration(1, 8), Duration(1, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_06():
    r'''Translate timespan start offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(start_offset_translation=Duration(1, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_07():
    r'''Translate timespan stop offset.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(stop_offset_translation=Duration(-1, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_08():
    r'''Stacked timespan callbacks applied in composition.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(start_offset_translation=Duration(1, 8))
    timespan = timespan.scale(Multiplier(2))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
