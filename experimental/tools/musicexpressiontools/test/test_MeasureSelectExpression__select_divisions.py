# -*- encoding: utf-8 -*-
from experimental import *


def test_MeasureSelectExpression__select_divisions_01():
    r'''Select divisions from measure select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    measures = red_segment.select_measures('Voice 1')[1:3]
    time_relation = timespantools.timespan_2_stops_during_timespan_1()
    divisions = measures.select_divisions('Voice 1', time_relation=time_relation)
    divisions.timespan.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
