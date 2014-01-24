# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_dynamic_handler_01():
    r'''Set handler on all leaves in voice.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    handler = new(
        library.hairpins,
        ('pp', '<', 'p'),
        )
    score_specification.select_leaves('Voice 1').set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_dynamic_handler_02():
    r'''Set handler on leaf slice.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    handler = new(
        library.hairpins,
        ('pp', '<', 'p'),
        )
    score_specification.select_leaves('Voice 1')[2:5].set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_dynamic_handler_03():
    r'''Set handler on division slice.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_rhythm(library.joined_sixteenths, contexts=['Voice 1'])
    handler = new(
        library.hairpins,
        ('p', '<', 'f'),
        )
    divisions = score_specification.select_divisions('Voice 1')[2:5]
    divisions.timespan.select_leaves('Voice 1').set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
