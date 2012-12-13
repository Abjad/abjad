from abjad import *
from experimental import *


def test_miscellaneous_01():
    '''Voice 2 rhythms interpret incorrectly.
    Fix this and then rename test and house somewhere appropriate.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures(0, 1)
    second_measure = red_segment.select_background_measures(1, 2)
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'], timespan=first_measure)
    rhythm = red_segment.request_rhythm('Voice 1', anchor=first_measure)
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'], timespan=first_measure)
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'], timespan=second_measure)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
