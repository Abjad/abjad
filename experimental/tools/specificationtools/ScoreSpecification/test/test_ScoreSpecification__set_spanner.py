from experimental import *


def test_ScoreSpecification__set_spanner_01():
    '''Set spanner on divisions' leaves.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1())
    divisions = score_specification.select_divisions('Voice 1')[2:4]
    leaves = divisions.timespan.select_leaves('Voice 1')
    leaves.set_spanner(spannertools.SlurSpanner())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
