# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_register_01():
    r'''Transpose pitches from aggregate 0.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(1, 16)])
    score_specification.set_rhythm(library.note_tokens)
    score_specification.select_leaves('Voice 1').set_pitch(library.example_pitches_1())
    score_specification.select_leaves('Voice 1').set_aggregate(library.example_aggregates[0])
    score_specification.select_leaves('Voice 1').set_register(library.example_octave_transposition)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_register_02():
    r'''Transpose pitches from aggregate 1.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(1, 16)])
    score_specification.set_rhythm(library.note_tokens)
    score_specification.select_leaves('Voice 1').set_pitch(library.example_pitches_1())
    score_specification.select_leaves('Voice 1').set_aggregate(library.example_aggregates[1])
    score_specification.select_leaves('Voice 1').set_register(library.example_octave_transposition)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
