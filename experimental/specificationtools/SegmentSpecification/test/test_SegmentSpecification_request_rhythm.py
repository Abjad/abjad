from abjad import *
from experimental import *

# TODO: Add rhythm request tests for requests between voices.
# TODO: Add rhythm request tests for requests for material from an earlier segment.
# TODO: Add rhythm request tests for requests for material from a later segment.
# TODO: Add rhythm request tests for requests for reversed material.

def test_SegmentSpecification_request_rhythm_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.append_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm(context='Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
