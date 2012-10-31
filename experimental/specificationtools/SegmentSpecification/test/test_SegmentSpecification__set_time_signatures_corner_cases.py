from abjad import *
from experimental import *


def test_SegmentSpecification__set_time_signatures_corner_cases_01():
    '''Multiple time signature settings are allowed for a single segment.

    Interpreter ignores all but the last.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(2, 8), (2, 8)])
    segment.set_time_signatures([(4, 8), (4, 8)])
    segment.set_time_signatures([(3, 8), (3, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
