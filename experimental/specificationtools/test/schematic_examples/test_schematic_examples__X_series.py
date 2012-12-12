from abjad import *
from experimental import *


def test_schematic_examples__X_series_01():
    '''Schematic example X1.
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

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], truncate=True)
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


def test_schematic_examples__X_series_02():
    '''Schematic example X2.
    Quartet in two segments.
    Segment 1 time signatures [4/8, 3/8].
    Staff 1 [3/16] divisions and staff 2 [4/16] divisions.
    Staff 3 divisions equal to reversed staff 1 divisions.
    Staff 4 divisions equal to reverse staff 2 divisions.
    Segment 2 continues segment 1.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts='Voice 1', truncate=True)
    red_segment.set_divisions([(4, 16)], contexts='Voice 2', truncate=True)
    source_1 = red_segment.request_divisions('Voice 1')
    source_2 = red_segment.request_divisions('Voice 2')
    red_segment.set_divisions(source_1, contexts=['Voice 3'], reverse=True, truncate=True)
    red_segment.set_divisions(source_2, contexts=['Voice 4'], reverse=True, truncate=True)
    red_segment.set_rhythm(library.thirty_seconds)

    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples__X_series_03():
    '''Schematic example X3.
    Quartet in 2 segments. 
    First segment time signatures [6/8, 3/8]. 
    First staff 1:1 of measures then [3/16, 5/16] divisions.
    Second staff 1:1 of meaures then [5/16, 3/16] divisions.
    Third staff 1:1 of total time then [3/16, 5/16] divisions from staff 1.
    Fourth staff 1:1 of total time then [5/16, 3/16] divisions from staff 2.
    Note tokens scorewide.
    Second segment equal to first segment flipped about the y axis in all respects.
    ''' 

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    measures = red_segment.select_background_measures()
    left_measure, right_measure = measures.partition_by_ratio((1, 1))
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 2'], selector=left_measure)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 2'], selector=right_measure)

    segment = red_segment.select()
    left_half, right_half = segment.divide_by_ratio((1, 1))

    voice_1_left_division_command = red_segment.request_division_command('Voice 1', selector=left_measure)
    voice_1_right_division_command = red_segment.request_division_command('Voice 1', selector=right_measure)

    red_segment.set_divisions(voice_1_left_division_command, contexts=['Voice 3'], selector=left_half)
    red_segment.set_divisions(voice_1_right_division_command, contexts=['Voice 3'], selector=right_half)

    voice_2_left_division_command = red_segment.request_division_command('Voice 2', selector=left_measure)
    voice_2_right_division_command = red_segment.request_division_command('Voice 2', selector=right_measure)

    red_segment.set_divisions(voice_2_left_division_command, contexts=['Voice 4'], selector=left_half)
    red_segment.set_divisions(voice_2_right_division_command, contexts=['Voice 4'], selector=right_half)

    red_segment.set_rhythm(library.note_tokens)

    blue_segment = score_specification.append_segment(name='blue')
    
    red_time_signatures = red_segment.request_time_signatures('Voice 1')
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


def test_schematic_examples__X_series_04():
    '''Schematic example X4.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8, 2/8]. 
    First staff 1:1:1 total time then thirty-seconds then sixteenths then eighths.
    Staff 2 rhythm equal to staff 1 rhythm regions rotated -1.
    Staff 3 rhythm equal to staff 1 rhythm regions rotated -2.
    Staff 4 divisions equal to naive time signature divisions.
    Staff 4 rhythm equal to division-durated notes.
    Segment 2 time signatures preserve segment 1 time signatures.
    Segment 2 otherwise equal to segment 1 flipped about the y axis.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment = red_segment.select()
    divisions = segment.divide_by_ratio([1, 1, 1])
    red_segment.set_divisions(divisions)
    left = red_segment.select_divisions('Voice 1', 0, 1)
    middle = red_segment.select_divisions('Voice 1', 1, 2)
    right = red_segment.select_divisions('Voice 1', 2, 3)
    red_segment.set_rhythm(library.equal_divisions(16), selector=left, contexts=['Voice 1'])
    red_segment.set_rhythm(library.equal_divisions(8), selector=middle, contexts=['Voice 1'])
    red_segment.set_rhythm(library.equal_divisions(4), selector=right, contexts=['Voice 1'])
    voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    indicator = settingtools.RotationIndicator(-1, 1)
    red_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 2'], rotation=indicator)
    indicator = settingtools.RotationIndicator(-2, 1)
    red_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 3'], rotation=indicator)
    naive_beats = red_segment.request_naive_beats('Voice 1')
    red_segment.set_divisions(naive_beats, contexts=['Voice 4'])
    red_segment.set_rhythm(library.note_tokens)
    blue_segment = score_specification.append_segment(name='blue')
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


def test_schematic_examples__X_series_05():
    '''Schematic example X5.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    F1 rhythm 1, 2, 3 thirty-seconds.
    F2 rhythm F1 surface rhythm rotated by 1 thirty-second.
    F3 rhythm F1 surface rhythm rotated by 2 thirty-seconds.
    F4 rhythm F1 surface rhythm rotated by 3 thirty-seconds.
    Second segment time signatures [1/8, 1/8]. 
    Staves repeat rhythm exactly until cut off at end of score.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. ] }", contexts=['Voice 1'])
    first_division = red_segment.select_divisions('Voice 1', 0, 1)
    voice_1_rhythmic_cell = red_segment.request_rhythm('Voice 1', anchor=first_division)
    indicator = settingtools.RotationIndicator(Duration(-1, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell, contexts=['Voice 2'], rotation=indicator)
    indicator = settingtools.RotationIndicator(Duration(-2, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell, contexts=['Voice 3'], rotation=indicator)
    indicator = settingtools.RotationIndicator(Duration(-3, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell, contexts=['Voice 4'], rotation=indicator)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(1, 8)])
    
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples__X_series_06():
    '''Schematic example X6.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    F1 rhythm 1, 2, 3, 4 thirty-seconds.
    F2 rhythm F1 surface rhythm rotated by 1 leaf.
    F3 rhythm F1 surface rhythm rotated by 2 leaves.
    F4 rhythm F1 surface rhythm rotated by 3 leaves.
    Second segment time signatures [1/8, 1/8]. 
    Second segment staves repeat reversed first segment rhythms until cut off at end of score.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(10, 32)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    first_division = red_segment.select_divisions('Voice 1', 0, 1)
    rhythmic_cell = red_segment.request_rhythm('Voice 1', anchor=first_division)
    indicator = settingtools.RotationIndicator(-1, fracture_spanners=False)
    red_segment.set_rhythm(rhythmic_cell, contexts=['Voice 2'], rotation=indicator)
    indicator = settingtools.RotationIndicator(-2, fracture_spanners=False)
    red_segment.set_rhythm(rhythmic_cell, contexts=['Voice 3'], rotation=indicator)
    indicator = settingtools.RotationIndicator(-3, fracture_spanners=False)
    red_segment.set_rhythm(rhythmic_cell, contexts=['Voice 4'], rotation=indicator)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(1, 8)])
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], reverse=True)
    red_voice_2_rhythm = red_segment.request_rhythm('Voice 2')
    blue_segment.set_rhythm(red_voice_2_rhythm, contexts=['Voice 2'], reverse=True)
    red_voice_3_rhythm = red_segment.request_rhythm('Voice 3')
    blue_segment.set_rhythm(red_voice_3_rhythm, contexts=['Voice 3'], reverse=True)
    red_voice_4_rhythm = red_segment.request_rhythm('Voice 4')
    blue_segment.set_rhythm(red_voice_4_rhythm, contexts=['Voice 4'], reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples__X_series_07():
    '''Schematic example X7.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    Rhythm of each staff specified separately for first and second measures.
    F1 m1 rhythm 1, 2, 3, 4 thirty-seconds; F1 m2 rhythm rotates F1 m1 rhythm by 1 thirty-second.
    F2 m1 rhythm rotates F1 m1 rhythm 2 thirty-seconds; F2 m2 rotates F1 m1 rhythm 3 thirty-seconds.
    F3 m1 rhythm rotates F1 m1 rhythm 4 thirty-seconds; F3 m2 rotates F1 m1 rhythm 5 thirty-seconds.
    F4 m1 rhythm rotates F1 m1 rhythm 6 thirty-seconds; F4 m2 rotates F1 m1 rhythm 7 thirty-seconds.
    Second segment time signatures [2/8]. 
    Second segment equal to slice of first segment from start offset of F1 leaf 5.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures(0, 1)
    second_measure = red_segment.select_background_measures(1, 2)
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'], selector=first_measure)
    cell = red_segment.request_rhythm('Voice 1', anchor=first_measure)
    red_segment.set_rhythm(cell, contexts=['Voice 1'], selector=second_measure, rotation=Duration(-1, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 2'], selector=first_measure, rotation=Duration(-2, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 2'], selector=second_measure, rotation=Duration(-3, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 3'], selector=first_measure, rotation=Duration(-4, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 3'], selector=second_measure, rotation=Duration(-5, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 4'], selector=first_measure, rotation=Duration(-6, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 4'], selector=second_measure, rotation=Duration(-7, 32))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves('Voice 1', start=4)
    voice_1_rhythm = red_segment.request_rhythm('Voice 1', anchor=timespan)
    voice_2_rhythm = red_segment.request_rhythm('Voice 2', anchor=timespan)
    voice_3_rhythm = red_segment.request_rhythm('Voice 3', anchor=timespan)
    voice_4_rhythm = red_segment.request_rhythm('Voice 4', anchor=timespan)
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    blue_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 2'])
    blue_segment.set_rhythm(voice_3_rhythm, contexts=['Voice 3'])
    blue_segment.set_rhythm(voice_4_rhythm, contexts=['Voice 4'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples__X_series_08():
    '''Schematic example X8.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8, 2/8].
    Rhythm of each staff specified separately for each measure.
    F1 measures 1:1:1 by count.
    F1 measures part 1 with denominator / 1;
    F1 measures part 2 with denominator / 2;
    F1 measures part 3 with denominator / 4;
    F2 R-1 F1 tokens to give [d/2, d/4, d/1].
    F3 R-2 F1 tokens to give [d/4, d/1, d/2].
    F4 thirty-second-valued rest-incised notes.
    T2 [3/16, 3/16].
    F1, F2, F3 select last 10 notes of T1 F1 then cycle.
    F4 continues as before.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_background_measures()
    first_measure, middle_measure, last_measure = measures.partition_by_ratio((1, 1, 1))
    red_segment.set_rhythm(library.even_runs(0), contexts=['Voice 1'], selector=first_measure)
    red_segment.set_rhythm(library.even_runs(1), contexts=['Voice 1'], selector=middle_measure)
    red_segment.set_rhythm(library.even_runs(2), contexts=['Voice 1'], selector=last_measure)
    red_segment.set_rhythm(library.even_runs(1), contexts=['Voice 2'], selector=first_measure)
    red_segment.set_rhythm(library.even_runs(2), contexts=['Voice 2'], selector=middle_measure)
    red_segment.set_rhythm(library.even_runs(0), contexts=['Voice 2'], selector=last_measure)
    red_segment.set_rhythm(library.even_runs(2), contexts=['Voice 3'], selector=first_measure)
    red_segment.set_rhythm(library.even_runs(0), contexts=['Voice 3'], selector=middle_measure)
    red_segment.set_rhythm(library.even_runs(1), contexts=['Voice 3'], selector=last_measure)
    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker([-1], [1], [-1], [1], 32)
    red_segment.set_rhythm(maker, contexts=['Voice 4'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(3, 16)])
    timespan = red_segment.select_leaves('Voice 1', start=-10)
    last_leaves = red_segment.request_rhythm('Voice 1', anchor=timespan)
    blue_segment.set_rhythm(last_leaves, contexts=['Voice 1', 'Voice 2', 'Voice 3'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_schematic_examples__X_series_09():
    '''Schematic example X9.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    F1 with [1, 2, 3, 4] thirty-seconds.
    F2 rotation of F1 R left by exactly 1/4 of duration.
    F3 rotation of F1 R left by exactly 2/4 quarter of duration.
    F4 rotation of F1 R left by exactly 3/4 quarter of duration.
    More description goes here.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    # TODO: extend RotationIndicator to allow for symoblic rotation by portion of total duration
    # This will remove hard-coded duration values in the three lines below.
    # Might look like rotation=settingtools.RotationIndicator((-1, 3)).
    # Or like rotation=(-1, 3), rotation=(-2, 2), rotation(-3, 1).
    # This also suggests a companion procedure that rotates based on ratio of total count of elements.
    red_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 2'], rotation=Duration(-7, 32))
    red_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 3'], rotation=Duration(-14, 32))
    red_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 4'], rotation=Duration(-21, 32))
    # TODO: implement a composer "cake slice" management interface on SegmentSpecification.
    # See the TODO file for an example of what the interface might look like.
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(3, 16)])
    segment = red_segment.select() 
    timespan = segment.adjust_offsets(Offset(3, 16), Offset(6, 16))
    rhythm = red_segment.request_rhythm('Voice 1', anchor=timespan)
    blue_segment.set_rhythm(rhythm, contexts=['Voice 1'])
    rhythm = red_segment.request_rhythm('Voice 2', anchor=timespan)
    blue_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    rhythm = red_segment.request_rhythm('Voice 3', anchor=timespan)
    blue_segment.set_rhythm(rhythm, contexts=['Voice 3'])
    rhythm = red_segment.request_rhythm('Voice 4', anchor=timespan)
    blue_segment.set_rhythm(rhythm, contexts=['Voice 4'])
    green_segment = score_specification.append_segment(name='green')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
