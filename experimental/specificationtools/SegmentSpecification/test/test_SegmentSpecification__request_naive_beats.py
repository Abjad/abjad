from abjad import *
from experimental import *


def test_SegmentSpecification__request_naive_beats_01():
    '''Two-segment score.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    divisions = red_segment.request_naive_beats()
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
