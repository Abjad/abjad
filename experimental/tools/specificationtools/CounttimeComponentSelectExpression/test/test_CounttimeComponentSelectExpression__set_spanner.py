from experimental import *


def test_CounttimeComponentSelectExpression__set_spanner_01():
    '''Set crescendo spanner.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_rhythm(library.note_tokens)
    score_specification.select_leaves('Voice 1').set_spanner(spannertools.CrescendoSpanner())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
