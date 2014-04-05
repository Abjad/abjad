# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_divisions_between_voices_01():
    r'''Division select expression between voices.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_02():
    r'''Division select expression between voices with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_03():
    r'''Division select expression between voices with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_04():
    r'''Division select expression between voices with reverse callbacks.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)