from experimental import *


def test_CounttimeComponentSelectExpression__evaluate_against_score_01():
    '''Score-evaluate counttime component select expression anchored to division select expression.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(reverse=True))
    right.set_pitch(library.example_pitches_1(reverse=True))
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
