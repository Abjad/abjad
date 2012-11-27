from abjad import *
from experimental import *


def test_SegmentSpecification__select_segment_01():
    '''Trivial test to ensure selection of entire segment works.

    This is default behavior for the case where selector is left unspecified.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    selector = segment.select_segment()
    segment.set_divisions([(3, 16)], selector=selector)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
