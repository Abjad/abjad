from abjad import *
from experimental import *


def test_multiple_segment_quartet_01():
    '''Create 4-staff score S with sections red, blue.
    Set red time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set red 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set red 1 & 2 rhythm equal to running 32nd notes.
    Set red 3 & 4 divisions equal to red time signatures.
    Set red 3 & 4 rhythm equal to division-durated notes.

    Set blue time signatures equal to the last 2 time signatures of red.
    Let all other red specifications continue to blue.

    Tests for spanning divisions in 1 & 2 over red / blue.
    Tests for truncated divisions in 1 & 2 at the end of blue.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])
    upper = [red_segment.v1, red_segment.v2]
    red_segment.set_divisions([(3, 16)], contexts=upper)
    red_segment.set_rhythm(library.thirty_seconds, contexts=upper)
    lower = [red_segment.v3, red_segment.v4]
    red_segment.set_rhythm(library.note_filled_tokens, contexts=lower)
    blue_segment = score_specification.append_segment(name='blue')
    source = score_specification['red'].request_time_signatures()
    blue_segment.set_time_signatures(source, index=-2, count=2)
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
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])
    upper = [red_segment.v1, red_segment.v2]
    red_segment.set_divisions([(5, 16)], contexts=upper)
    red_segment.set_rhythm(library.thirty_seconds, contexts=upper)
    lower = [red_segment.v3, red_segment.v4]
    red_segment.set_divisions([(4, 16), (3, 16)], contexts=lower)
    red_segment.set_rhythm(library.note_filled_tokens, contexts=lower)
    blue_segment = score_specification.append_segment(name='blue')
    source = score_specification['red'].request_time_signatures()
    blue_segment.set_time_signatures(source, index=-2, count=2)
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
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures(stop=1)
    second_measure = red_segment.select_background_measures(start=-1)
    first_half, second_half = red_segment.select_segment_ratio_part((1, 1))
    red_segment.set_divisions([(3, 16)], selector=first_measure, contexts=['Voice 1'], persist=False)
    red_segment.set_divisions([(5, 16)], selector=second_measure, contexts=['Voice 1'], persist=False)
    red_segment.set_divisions([(5, 16)], selector=first_measure, contexts=['Voice 2'], persist=False)
    red_segment.set_divisions([(3, 16)], selector=second_measure, contexts=['Voice 2'], persist=False)
    red_segment.set_divisions([(3, 16)], selector=first_half, contexts=['Voice 3'], persist=False)
    red_segment.set_divisions([(5, 16)], selector=second_half, contexts=['Voice 3'], persist=False)
    red_segment.set_divisions([(5, 16)], selector=first_half, contexts=['Voice 4'], persist=False)
    red_segment.set_divisions([(3, 16)], selector=second_half, contexts=['Voice 4'], persist=False)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_04():
    '''F1 divisions truncated in F1. F2, F3, F4 divisions with rotation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'])
    source = red_segment.request_divisions('Voice 1') 
    red_segment.set_divisions(source, contexts=['Voice 2'], rotation=-1, truncate=True)
    red_segment.set_divisions(source, contexts=['Voice 3'], rotation=-2, truncate=True)
    red_segment.set_divisions(source, contexts=['Voice 4'], rotation=-3, truncate=True)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
