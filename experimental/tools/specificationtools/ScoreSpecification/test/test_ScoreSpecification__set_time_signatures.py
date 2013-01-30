from experimental.tools import *


def test_ScoreSpecification__set_time_signatures_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    # TODO: allow interpretation to procede without dummy segment
    red_segment = score_specification.append_segment(name='red')
    score_specification.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
