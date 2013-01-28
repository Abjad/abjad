from experimental import *


def test_SegmentSpecification__select_divisions_between_voices_01():
    '''Division select expression between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_02():
    '''Division select expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_03():
    '''Division select expression between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_between_voices_04():
    '''Division select expression between voices with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 2'])
    voice_2_divisions = red_segment.select_divisions('Voice 2')
    voice_2_divisions = voice_2_divisions.reflect()
    voice_2_divisions = voice_2_divisions.reflect()
    red_segment.set_divisions(voice_2_divisions, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
