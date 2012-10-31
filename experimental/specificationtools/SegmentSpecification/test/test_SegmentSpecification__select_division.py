from abjad import *
from experimental import *


def test_SegmentSpecification__select_division_01():
    '''Negative index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures(4 * [(2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.thirty_seconds)
    antepenultimate_division = segment.select_division(-3)
    segment.set_rhythm(library.sixteenths, selector=antepenultimate_division)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
