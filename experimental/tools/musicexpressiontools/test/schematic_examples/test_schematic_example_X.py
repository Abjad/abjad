# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_schematic_example_X_01():
    r'''Schematic example X1.
    Quartet in two segments.
    First segment [4/8, 3/8] time signatures.
    Staff 1 [3/16] divisions truncated at end of segment.
    Staff 2 divisions equal to staff 1 divisions rotated once left.
    Staff 3 divisions equal to staff 1 divisions rotated twice left.
    Staff 4 divisions equal to staff 1 divisions rotated three times left.
    Second segment exactly equal to first segment with hard break between.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], truncate=True)
    source_expression = red_segment.select_divisions('Voice 1')
    red_segment.set_divisions(source_expression.rotate(-1), contexts=['Voice 2'], truncate=True)
    red_segment.set_divisions(source_expression.rotate(-2), contexts=['Voice 3'], truncate=True)
    red_segment.set_divisions(source_expression.rotate(-3), contexts=['Voice 4'], truncate=True)
    red_segment.set_rhythm(library.joined_thirty_seconds)

    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_schematic_example_X_05():
    r'''Schematic example X5.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    F1 rhythm 1, 2, 3 thirty-seconds.
    F2 rhythm F1 surface rhythm rotated by 1 thirty-second.
    F3 rhythm F1 surface rhythm rotated by 2 thirty-seconds.
    F4 rhythm F1 surface rhythm rotated by 3 thirty-seconds.
    Second segment time signatures [1/8, 1/8].
    Staves repeat rhythm exactly until cut off at end of score.
    '''
    pytest.skip('fix at some point.')

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. ] }", contexts=['Voice 1'])
    first_division = red_segment.select_divisions('Voice 1')[:1]
    voice_1_rhythmic_cell = first_division.start_offset.look_up_rhythm_set_expression('Voice 1')
    rotation = musicexpressiontools.RotationExpression(Duration(-1, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell.rotate(rotation), contexts=['Voice 2'])
    rotation = musicexpressiontools.RotationExpression(Duration(-2, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell.rotate(rotation), contexts=['Voice 3'])
    rotation = musicexpressiontools.RotationExpression(Duration(-3, 32), fracture_spanners=False)
    red_segment.set_rhythm(voice_1_rhythmic_cell.rotate(rotation), contexts=['Voice 4'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(1, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_schematic_example_X_07():
    r'''Schematic example X7.
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

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    first_measure.timespan.set_rhythm(cell.rotate(Duration(-2, 32)), contexts=['Voice 2'])
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-3, 32)), contexts=['Voice 2'])
    first_measure.timespan.set_rhythm(cell.rotate(Duration(-4, 32)), contexts=['Voice 3'])
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-5, 32)), contexts=['Voice 3'])
    first_measure.timespan.set_rhythm(cell.rotate(Duration(-6, 32)), contexts=['Voice 4'])
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-7, 32)), contexts=['Voice 4'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves('Voice 1')[4:]
    voice_1_rhythm = timespan.timespan.select_leaves('Voice 1')
    voice_2_rhythm = timespan.timespan.select_leaves('Voice 2')
    voice_3_rhythm = timespan.timespan.select_leaves('Voice 3')
    voice_4_rhythm = timespan.timespan.select_leaves('Voice 4')
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    blue_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 2'])
    blue_segment.set_rhythm(voice_3_rhythm, contexts=['Voice 3'])
    blue_segment.set_rhythm(voice_4_rhythm, contexts=['Voice 4'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_schematic_example_X_08():
    r'''Schematic example X8.
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
    pytest.skip('fix at some point.')

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    measures = red_segment.select_measures('Voice 1')
    first_measure, middle_measure, last_measure = measures.partition_by_ratio((1, 1, 1))
    first_measure.timespan.set_rhythm(library.even_runs(0), contexts=['Voice 1'])
    middle_measure.timespan.set_rhythm(library.even_runs(1), contexts=['Voice 1'])
    last_measure.timespan.set_rhythm(library.even_runs(2), contexts=['Voice 1'])
    first_measure.timespan.set_rhythm(library.even_runs(1), contexts=['Voice 2'])
    middle_measure.timespan.set_rhythm(library.even_runs(2), contexts=['Voice 2'])
    last_measure.timespan.set_rhythm(library.even_runs(0), contexts=['Voice 2'])
    first_measure.timespan.set_rhythm(library.even_runs(2), contexts=['Voice 3'])
    middle_measure.timespan.set_rhythm(library.even_runs(0), contexts=['Voice 3'])
    last_measure.timespan.set_rhythm(library.even_runs(1), contexts=['Voice 3'])
    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=32,
        )
    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_divisions=True,
        )
    red_segment.set_rhythm(maker, contexts=['Voice 4'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(3, 16)])
    timespan = red_segment.select_leaves('Voice 1')[-10:]
    last_leaves = timespan.timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(last_leaves, contexts=['Voice 1', 'Voice 2', 'Voice 3'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_schematic_example_X_09():
    r'''Schematic example X9.
    Quartet in two segments.
    First segment time signatures [4/8, 3/8].
    F1 with [1, 2, 3, 4] thirty-seconds.
    F2 rotation of F1 R left by exactly 1/4 of duration.
    F3 rotation of F1 R left by exactly 2/4 quarter of duration.
    F4 rotation of F1 R left by exactly 3/4 quarter of duration.
    More description goes here.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    voice_1_rhythm = red_segment.select_leaves('Voice 1')
    # Extend RotationExpression to allow for symoblic rotation by portion of total duration
    # This will remove hard-coded duration values in the three lines below.
    # Might look like rotation=musicexpressiontools.RotationExpression((-1, 3)).
    # Or like rotation=(-1, 3), rotation=(-2, 2), rotation(-3, 1).
    # This also suggests a companion procedure that rotates based on ratio of total count of elements.
    red_segment.set_rhythm(voice_1_rhythm.rotate(Duration(-7, 32)), contexts=['Voice 2'])
    red_segment.set_rhythm(voice_1_rhythm.rotate(Duration(-14, 32)), contexts=['Voice 3'])
    red_segment.set_rhythm(voice_1_rhythm.rotate(Duration(-21, 32)), contexts=['Voice 4'])
    # Implement a composer "cake slice" management interface on SegmentSpecification.
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(3, 16)])
    timespan = red_segment.timespan.set_offsets(Offset(3, 16), Offset(6, 16))
    rhythm = timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(rhythm, contexts=['Voice 1'])
    rhythm = timespan.select_leaves('Voice 2')
    blue_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    rhythm = timespan.select_leaves('Voice 3')
    blue_segment.set_rhythm(rhythm, contexts=['Voice 3'])
    rhythm = timespan.select_leaves('Voice 4')
    blue_segment.set_rhythm(rhythm, contexts=['Voice 4'])
    green_segment = score_specification.append_segment(name='green')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)