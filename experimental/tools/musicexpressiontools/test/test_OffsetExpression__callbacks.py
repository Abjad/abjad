# -*- encoding: utf-8 -*-
from experimental import *


def test_OffsetExpression__callbacks_01():
    r'''Translate offset expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_rhythm(library.thirty_seconds)
    offset = blue_segment.timespan.start_offset.translate(Duration(-1, 8))
    lookup = offset.look_up_rhythm_set_expression('Voice 1')
    green_segment.set_rhythm(lookup)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_OffsetExpression__callbacks_02():
    r'''Scale offset expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_rhythm(library.thirty_seconds)
    offset = blue_segment.timespan.start_offset.scale(Multiplier(1, 2))
    lookup = offset.look_up_rhythm_set_expression('Voice 1')
    green_segment.set_rhythm(lookup)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
