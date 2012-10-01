import py
from abjad import *
from experimental import *


def test_schematic_examples_01():
    '''Schematic example [X1].
    Quartet in two segments.
    First segment [4/8, 3/8] time signatures.
    Staff 1 [3/16] divisions truncated at end of segment.
    Staff 2 divisions equal to staff 1 divisions rotated once left.
    Staff 3 divisions equal to staff 1 divisions rotated twice left.
    Staff 4 divisions equal to staff 1 divisions rotated three times left.
    Second segment exactly equal to first segment with hard break between.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], truncate=True)
    source = red_segment.request_divisions('Voice 1') 
    red_segment.set_divisions(source, contexts=['Voice 2'], rotation=-1, truncate=True)
    red_segment.set_divisions(source, contexts=['Voice 3'], rotation=-2, truncate=True)
    red_segment.set_divisions(source, contexts=['Voice 4'], rotation=-3, truncate=True)
    red_segment.set_rhythm(library.thirty_seconds)

    blue_segment = score_specification.make_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples_02():
    '''Schematic example [X2].
    Quartet in two segments.
    Segment 1 time signatures [4/8, 3/8].
    Staff 1 [3/16] divisions and staff 2 [4/16] divisions.
    Staff 3 divisions equal to reversed staff 1 divisions.
    Staff 4 divisions equal to reverse staff 2 divisions.
    Segment 2 continues segment 1.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts='Voice 1', truncate=True)
    red_segment.set_divisions([(4, 16)], contexts='Voice 2', truncate=True)
    source_1 = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    source_2 = score_specification.request_divisions('Voice 2', 'red', segment_count=1)
    red_segment.set_divisions(source_1, contexts=['Voice 3'], reverse=True, truncate=True)
    red_segment.set_divisions(source_2, contexts=['Voice 4'], reverse=True, truncate=True)
    red_segment.set_rhythm(library.thirty_seconds)

    blue_segment = score_specification.make_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples_03():
    '''Schematic example [X3].
    Quartet in 2 segments. 
    First segment time signatures [6/8, 3/8]. 
    First staff 1:1 of measures then [3/16, 5/16] divisions.
    Second staff 1:1 of meaures then [5/16, 3/16] divisions.
    Third staff 1:1 of total time then [3/16, 5/16] divisions from staff 1.
    Fourth staff 1:1 of total time then [5/16, 3/16] divisions from staff 2.
    Note-filled tokens scorewide.
    Second segment equal to first segment flipped about the y axis in all respects.
    ''' 

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

    voice_1_left_division_command = red_segment.request_division_command('Voice 1', selector=left_measure)
    voice_1_right_division_command = red_segment.request_division_command('Voice 1', selector=right_measure)

    red_segment.set_divisions(voice_1_left_division_command, contexts=['Voice 3'], selector=left_half)
    red_segment.set_divisions(voice_1_right_division_command, contexts=['Voice 3'], selector=right_half)

    voice_2_left_division_command = red_segment.request_division_command('Voice 2', selector=left_measure)
    voice_2_right_division_command = red_segment.request_division_command('Voice 2', selector=right_measure)

    red_segment.set_divisions(voice_2_left_division_command, contexts=['Voice 4'], selector=left_half)
    red_segment.set_divisions(voice_2_right_division_command, contexts=['Voice 4'], selector=right_half)

    red_segment.set_rhythm(library.note_filled_tokens)

    blue_segment = score_specification.make_segment(name='blue')
    
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, reverse=True)

    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    red_voice_2_rhythm = red_segment.request_rhythm('Voice 2')
    red_voice_3_rhythm = red_segment.request_rhythm('Voice 3')
    red_voice_4_rhythm = red_segment.request_rhythm('Voice 4')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], reverse=True)
    blue_segment.set_rhythm(red_voice_2_rhythm, contexts=['Voice 2'], reverse=True)
    blue_segment.set_rhythm(red_voice_3_rhythm, contexts=['Voice 3'], reverse=True)
    blue_segment.set_rhythm(red_voice_4_rhythm, contexts=['Voice 4'], reverse=True)

    score = score_specification.interpret() 

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples_04():
    '''Schematic example X4.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8]. 
    First staff 1:1:1 total time then thirty-seconds then sixteenths then eighths.
    Staff 2 rhythm equal to staff 1 rhythm regions rotated -1.
    Staff 3 rhythm equal to staff 1 rhythm regions rotate -2.
    Staff 4 divisions equal to naive time signature divisions.
    Staff 4 rhythm equal to note-filled tokens.
    Segment 2 time signatures preserve segment 1 time signatures.
    Segment 2 otherwise equal to segment 1 flipped about the y axis.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    #left = red_segment.select_segment_ratio_part((1, 1, 1), 0)
    #middle = red_segment.select_segment_ratio_part((1, 1, 1), 1)
    #right = red_segment.select_segment_ratio_part((1, 1, 1), 2)
    # TODO: implement SegmentSpecification method to return [(7, 24), (7, 24), (7, 24)] directly
    red_segment.set_divisions(3 * [(7, 24)])

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
