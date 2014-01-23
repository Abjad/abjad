# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_mark_01():

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(2, 16)])
    beam_specifier = rhythmmakertools.BeamSpecifier(beam_cells_together=True)
    rhythm_maker = new(
        library.note_tokens,
        #beam_cells_together=True,
        beam_specifier=beam_specifier,
        )
    score_specification.set_rhythm(rhythm_maker)
    score_specification.select_leaves('Voice 1').set_mark(indicatortools.StemTremolo(32))
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
