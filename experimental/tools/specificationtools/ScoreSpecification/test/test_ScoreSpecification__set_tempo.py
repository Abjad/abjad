from experimental import *


def test_ScoreSpecification__set_tempo_01():
    '''Set tempo on first and second half of leaves.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False)
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    leaves = score_specification.select_leaves('Voice 1').partition_by_ratio((1, 1))
    leaves[0].set_tempo(library.quarter_equals_90)
    leaves[1].set_tempo(library.quarter_equals_108)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
