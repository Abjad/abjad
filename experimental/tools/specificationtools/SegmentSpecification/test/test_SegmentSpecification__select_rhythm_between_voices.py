from experimental import *


def test_SegmentSpecification__select_rhythm_between_voices_01():
    '''Rhythm select expression between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.select_leaves('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_between_voices_02():
    '''Rhythm select expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.select_leaves('Voice 2')
    voice_2_rhythm = voice_2_rhythm.reflect()
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_between_voices_03():
    '''Rhythm select expression between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.select_leaves('Voice 2')
    voice_2_rhythm = voice_2_rhythm.reflect()
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_between_voices_04():
    '''Rhythm select expression between voices with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.select_leaves('Voice 2')
    voice_2_rhythm = voice_2_rhythm.reflect()
    voice_2_rhythm = voice_2_rhythm.reflect()
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_between_voices_05():
    '''Rhythm select expression between voices with multiple in-voice application.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    first_measure.timespan.set_rhythm(cell.rotate(Duration(-2, 32)), contexts=['Voice 2'])
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-3, 32)), contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_rhythm_between_voices_06():
    '''Voice 2 rhythms interpret incorrectly.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    rhythm = first_measure.timespan.select_leaves('Voice 1')
    first_measure.timespan.set_rhythm(rhythm, contexts=['Voice 2'])
    second_measure.timespan.set_rhythm(rhythm, contexts=['Voice 2'])
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
