from abjad import *
from experimental import *


def test_single_segment_solo_context_cascade_01():
    '''Settings made against lower-level contexts override 
    settings made against higher-level contexts.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)
    segment.set_rhythm(library.note_filled_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
