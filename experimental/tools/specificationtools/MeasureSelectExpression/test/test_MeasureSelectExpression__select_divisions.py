from experimental import *


def test_MeasureSelectExpression__select_divisions_01():
    '''Select divisions from measure select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[1:3]
    time_relation = timerelationtools.timespan_2_stops_during_timespan_1()
    divisions = measures.select_divisions('Voice 1', time_relation=time_relation)
    divisions.timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
