from abjad import *
from experimental import *


def test_SegmentSpecification__select_leaves_01():
    '''Select leaves composited on leaf selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    rhythm = red_segment.select_leaves('Voice 1')[2:4]
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_02():
    '''Rotate leaf selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    leaves = red_segment.select_leaves('Voice 1')[4:7]
    voice_1_rhythm = leaves.timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_03():
    '''Leaves select correctly across rhythm region product boundaries.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    first_measure.timespan.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.timespan.select_leaves('Voice 1')
    second_measure.timespan.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    voice_1_rhythm = red_segment.select_leaves('Voice 1')[4:8]
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_04():
    '''Select one division's leaves.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(6, 32)], contexts=['Voice 1'])
    maker = rhythmmakertools.TaleaRhythmMaker([1, 2, 3], 32)
    maker.beam_cells_together = True
    red_segment.set_rhythm(maker, contexts=['Voice 1'])
    first_division = red_segment.select_divisions('Voice 1')[:1]
    red_rhythm_cell = first_division.timespan.select_leaves('Voice 1')
    red_rhythm_cell = red_rhythm_cell.reflect()
    red_segment.set_rhythm(red_rhythm_cell, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
