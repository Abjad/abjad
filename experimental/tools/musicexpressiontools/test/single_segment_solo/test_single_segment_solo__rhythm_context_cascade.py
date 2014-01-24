# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_solo__rhythm_context_cascade_01():
    r'''Settings made against lower-level contexts override
    set expressions made against higher-level contexts.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    red_segment.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_02():
    r'''Thirty-seconds override sixteenths.
    Then division-durated notes override thirty-seconds.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    red_segment.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_03():
    r'''Thirty-seconds override sixteenths.
    Then division-durated notes override thirty-seconds.
    Then division-durated rests override division-durated notes.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    red_segment.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    red_segment.set_rhythm(library.rest_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_04():
    r'''Lexically later set expressions don't matter if they
    are made against a higher-level context.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    red_segment.set_rhythm(library.rest_tokens, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_05():
    r'''SelectExpression and contexts work together.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    measures = red_segment.select_measures('Voice 1')[1:2]
    measures.timespan.set_rhythm(library.joined_thirty_seconds, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
