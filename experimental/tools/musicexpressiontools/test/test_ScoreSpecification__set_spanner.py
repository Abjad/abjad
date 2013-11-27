# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_spanner_01():
    r'''Set spanner on divisions' leaves.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1())
    divisions = score_specification.select_divisions('Voice 1')[2:4]
    leaves = divisions.timespan.select_leaves('Voice 1')
    leaves.set_spanner(spannertools.Slur())
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_spanner_02():
    r'''Use spanner to set grob overrides and subsequent reverts.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = new(
        library.sixteenths,
        beam_cells_together=False, 
        beam_each_cell=True,
        )
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1())
    divisions = score_specification.select_divisions('Voice 1')[2:4]
    leaves = divisions.timespan.select_leaves('Voice 1')
    spanner = spannertools.Slur()
    override(spanner).note_head.color = 'red'
    override(spanner).stem.color = 'red'
    override(spanner).beam.color = 'red'
    override(spanner).accidental.color = 'red'
    leaves.set_spanner(spanner)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
