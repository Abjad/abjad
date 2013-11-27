# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_tempo_01():
    r'''Set tempo on first and second half of leaves.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False,
        )
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    leaves = score_specification.select_leaves('Voice 1').partition_by_ratio((1, 1))
    leaves[0].set_tempo(library.quarter_equals_90)
    leaves[1].set_tempo(library.quarter_equals_108)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
