# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_divisions_time_relation_01():
    r'''Stop-based time relation.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_divisions([(4, 8)])
    time_relation = timespantools.timespan_2_stops_during_timespan_1()
    divisions_that_stop_during_red = red_segment.select_divisions('Voice 1', time_relation=time_relation)
    divisions_that_stop_during_blue = blue_segment.select_divisions('Voice 1', time_relation=time_relation)
    divisions_that_stop_during_red.timespan.set_rhythm(library.joined_sixteenths)
    divisions_that_stop_during_blue.timespan.set_rhythm(library.joined_eighths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
