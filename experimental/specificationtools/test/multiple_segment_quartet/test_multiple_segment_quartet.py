from abjad import *
from experimental import *
import py


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

    segment = score_specification.make_segment(name='T1')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(3, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.make_segment(name='T2')
    source = score_specification['T1'].request_time_signatures()
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

    segment = score_specification.make_segment(name='T1')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(5, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_divisions([(4, 16), (3, 16)], contexts=lower)
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.make_segment(name='T2')
    source = score_specification['T1'].request_time_signatures()
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
    '''V3, V4 divisions equal V1, V2 divisions reversed.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts='Voice 1', truncate=True)
    segment.set_divisions([(4, 16)], contexts='Voice 2', truncate=True)
    source_1 = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    source_2 = score_specification.request_divisions('Voice 2', 'red', segment_count=1)

    segment.set_divisions(source_1, contexts=['Voice 3'], reverse=True, truncate=True)
    segment.set_divisions(source_2, contexts=['Voice 4'], reverse=True, truncate=True)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.make_segment('blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_05():
    '''F1 divisions truncated in F1. F2, F3, F4 divisions with rotation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1)
    source = score_specification.request_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_divisions(source, contexts=segment.v2, rotation=-1, truncate=True)
    segment.set_divisions(source, contexts=segment.v3, rotation=-2, truncate=True)
    segment.set_divisions(source, contexts=segment.v4, rotation=-3, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.make_segment('T2')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_06():
    '''As above with T2 equal to T1 and a hard break between.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1, truncate=True)
    source = score_specification.request_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_divisions(source, contexts=segment.v2, rotation=-1, truncate=True)
    segment.set_divisions(source, contexts=segment.v3, rotation=-2, truncate=True)
    segment.set_divisions(source, contexts=segment.v4, rotation=-3, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.make_segment('T2')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_07():
    '''Render example [3]:
    Quartet in 2 segments. T1 time signatures 6/8 3/8. 
    F1 1:1 of measures then left part 3/16 and right part 5/16 divisions.
    F2 1:1 of meaures then [5/16, 3/16]
    F3 1:1 of total time then [3/16, 5/16] from F1.
    F4 1:1 of total time then [5/16, 3/16] from F2.
    Filled note tokens scorewide.
    T2 equal to T1 flipped about the y axis in all respects.
    ''' 
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measures_ratio_part((1, 1), 0, is_count=True)
    right_measure = red_segment.select_background_measures_ratio_part((1, 1), -1, is_count=True)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 2'], selector=left_measure)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 2'], selector=right_measure)

    left_half = red_segment.select_segment_ratio_part((1, 1), 0)
    right_half = red_segment.select_segment_ratio_part((1, 1), -1)

    voice_1_left_division_command = red_segment.request_division_command(context='Voice 1', selector=left_measure)
    voice_1_right_division_command = red_segment.request_division_command(context='Voice 1', selector=right_measure)

    red_segment.set_divisions(voice_1_left_division_command, contexts=['Voice 3'], selector=left_half)
    red_segment.set_divisions(voice_1_right_division_command, contexts=['Voice 3'], selector=right_half)

    voice_2_left_division_command = red_segment.request_division_command(context='Voice 2', selector=left_measure)
    voice_2_right_division_command = red_segment.request_division_command(context='Voice 2', selector=right_measure)

    red_segment.set_divisions(voice_2_left_division_command, contexts=['Voice 4'], selector=left_half)
    red_segment.set_divisions(voice_2_right_division_command, contexts=['Voice 4'], selector=right_half)

    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, reverse=True)

    # TODO: make these lines work
    red_voice_1_rhythm = red_segment.request_rhythm(context='Voice 1')
    red_voice_2_rhythm = red_segment.request_rhythm(context='Voice 2')
    red_voice_3_rhythm = red_segment.request_rhythm(context='Voice 3')
    red_voice_4_rhythm = red_segment.request_rhythm(context='Voice 4')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], reverse=True)
    blue_segment.set_rhythm(red_voice_2_rhythm, contexts=['Voice 2'], reverse=True)
    blue_segment.set_rhythm(red_voice_3_rhythm, contexts=['Voice 3'], reverse=True)
    blue_segment.set_rhythm(red_voice_4_rhythm, contexts=['Voice 4'], reverse=True)

    score = score_specification.interpret() 

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
