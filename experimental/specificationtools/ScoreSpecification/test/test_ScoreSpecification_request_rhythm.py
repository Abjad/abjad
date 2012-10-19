from abjad import *
from experimental import *


def test_ScoreSpecification_request_rhythm_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(6, 32)], contexts=['Voice 1'])

    maker = timetokentools.SignalFilledTimeTokenMaker([1, 2, 3], 32)
    maker.beam = True
    red_segment.set_rhythm(maker, contexts=['Voice 1'])
    first_division = red_segment.select_division(0)
    red_rhythm_cell = score_specification.request_rhythm('Voice 1', selector=first_division)
    red_segment.set_rhythm(red_rhythm_cell, contexts=['Voice 2'], reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
