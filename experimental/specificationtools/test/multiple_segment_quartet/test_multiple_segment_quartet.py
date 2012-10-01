from abjad import *
from experimental import *


def test_multiple_segment_quartet_01():
    '''Create 4-staff score S with sections T1, T2.
    Set T1 time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set T1 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set T1 1 & 2 rhythm equal to running 32nd notes.
    Set T1 3 & 4 divisions equal to T1 time signatures.
    Set T1 3 & 4 rhythm equal to note-filled tokens.

    Set T2 time signatures equal to the last 2 time signatures of T1.
    Let all other T1 specifications continue to T2.

    Tests for spanning divisions in 1 & 2 over T1 / T2.
    Tests for truncated divisions in 1 & 2 at the end of T2.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(3, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.make_segment(name='blue')
    source = score_specification['red'].request_time_signatures()
    segment.set_time_signatures(source, index=-2, count=2)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_02():
    '''As above with different divisions.
    
    Tests for spanning divisions in 1 & 2 and also in 3 & 4.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(5, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_divisions([(4, 16), (3, 16)], contexts=lower)
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.make_segment(name='blue')
    source = score_specification['red'].request_time_signatures()
    segment.set_time_signatures(source, index=-2, count=2)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_03():
    '''Voices 1 & 2 set divisions according to ratio of background measures.
    Voices 3 & 4 set divisions according to ratio of segment duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    first_measure = segment.select_background_measures(stop=1)
    second_measure = segment.select_background_measures(start=-1)
    first_half = segment.select_segment_ratio_part((1, 1), 0)
    second_half = segment.select_segment_ratio_part((1, 1), 1)

    segment.set_divisions([(3, 16)], selector=first_measure, contexts=['Voice 1'], persist=False)
    segment.set_divisions([(5, 16)], selector=second_measure, contexts=['Voice 1'], persist=False)

    segment.set_divisions([(5, 16)], selector=first_measure, contexts=['Voice 2'], persist=False)
    segment.set_divisions([(3, 16)], selector=second_measure, contexts=['Voice 2'], persist=False)

    segment.set_divisions([(3, 16)], selector=first_half, contexts=['Voice 3'], persist=False)
    segment.set_divisions([(5, 16)], selector=second_half, contexts=['Voice 3'], persist=False)

    segment.set_divisions([(5, 16)], selector=first_half, contexts=['Voice 4'], persist=False)
    segment.set_divisions([(3, 16)], selector=second_half, contexts=['Voice 4'], persist=False)

    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.make_segment('blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_04():
    '''F1 divisions truncated in F1. F2, F3, F4 divisions with rotation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=['Voice 1'])
    source = segment.request_divisions('Voice 1') 
    segment.set_divisions(source, contexts=['Voice 2'], rotation=-1, truncate=True)
    segment.set_divisions(source, contexts=['Voice 3'], rotation=-2, truncate=True)
    segment.set_divisions(source, contexts=['Voice 4'], rotation=-3, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.make_segment('T2')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
