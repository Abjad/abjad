from experimental import *


def test_CounttimeComponentSelectExpression__time_relation_01():
    '''Red starts during blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_starts_during_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_02():
    '''Red stops during blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_stops_during_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_03():
    '''Red intersects blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_intersects_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_04():
    '''Red overlaps start of blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_overlaps_start_of_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_05():
    '''Red overlaps stop of blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_overlaps_stop_of_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__time_relation_06():
    '''Red trisects blue.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    score_specification.set_divisions([(5, 16)], contexts=['Voice 2'])
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm, contexts=['Voice 2'])
    division = score_specification.select_divisions('Voice 2')[1:2]
    division.timespan.select_leaves('Voice 2').set_note_head_color('blue')
    time_relation = timerelationtools.timespan_2_trisects_timespan_1()
    leaves = division.timespan.select_leaves('Voice 1', time_relation=time_relation)
    leaves.set_note_head_color('red')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
