from abjad import *
from experimental import *


def test_SegmentSpecification_request_rhythm_between_voices_01():
    '''Rhythm material request between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.request_rhythm('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
