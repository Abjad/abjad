# -*- encoding: utf-8 -*-
from experimental import *
import copy


def test_ScoreSpecification__set_pitch_01():
    r'''Read from server over all leaves in voice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_02():
    r'''Read from server over contiguous leaves in one voice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')[9:18]
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_03():
    r'''Read from server over discontiguous leaves in same voice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    first_leaves = score_specification.select_leaves('Voice 1')[:10]
    last_leaves = score_specification.select_leaves('Voice 1')[-10:]
    leaves = first_leaves + last_leaves
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_04():
    r'''Read from server over discontiguous leaves in different voices.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    first_leaves = score_specification.select_leaves('Voice 1')[:10]
    last_leaves = score_specification.select_leaves('Voice 2')[-10:]
    leaves = first_leaves + last_leaves
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_05():
    r'''Read from server over overlaid pitches in discontiguous select expression.
    Earlier pitch assignments are simply overwritten by later pitch assignments.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    first_leaves = score_specification.select_leaves('Voice 1')[:9]
    last_leaves = score_specification.select_leaves('Voice 1')[3:12]
    leaves = first_leaves + last_leaves
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_06():
    r'''Read from server over synchronous discontiguous selection.
    Voice 1 before voice 2.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')[:9]
    leaves += score_specification.select_leaves('Voice 2')[:9]
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_07():
    r'''Read from server over synchronous discontiguous selection.
    Voice 2 before voice 1.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 2')[:9]
    leaves += score_specification.select_leaves('Voice 1')[:9]
    leaves.set_pitch(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_08():
    r'''Two cursors open against the same server.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    cursor_1 = library.example_pitches_1()
    cursor_2 = library.example_pitches_1()
    score_specification.select_leaves('Voice 1')[:9].set_pitch(cursor_1)
    score_specification.select_leaves('Voice 2')[:9].set_pitch(cursor_2)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_09():
    r'''One cursor read three times.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    cursor = library.example_pitches_1()
    score_specification.select_leaves('Voice 1')[:3].set_pitch(cursor)
    score_specification.select_leaves('Voice 1')[6:9].set_pitch(cursor)
    score_specification.select_leaves('Voice 1')[12:15].set_pitch(cursor)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_10():
    r'''One cursor initialized from the position of another.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    cursor_1 = library.example_pitches_1()
    score_specification.select_leaves('Voice 1')[:9].set_pitch(cursor_1)
    cursor_2 = library.example_pitches_1(position=cursor_1.position)
    score_specification.select_leaves('Voice 2')[-9:].set_pitch(cursor_2)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_11():
    r'''Copied cursor preserves state.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    cursor_1 = library.example_pitches_1()
    score_specification.select_leaves('Voice 1')[:9].set_pitch(cursor_1)
    cursor_2 = copy.deepcopy(cursor_1)
    score_specification.select_leaves('Voice 2')[-9:].set_pitch(cursor_2)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_12():
    r'''Reverse cursor.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')[:9]
    leaves.set_pitch(library.example_pitches_1(reverse=True))
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_13():
    r'''Limit to first 4 nodes at level -1.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1(), node_count=4, level=-1)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_14():
    r'''Limit to first 4 nodes after position (2, 0) at level -1.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1(position=(2, 0)), node_count=4, level=-1)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_15():
    r'''Limit to first 2 nodes at level -2.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1(), node_count=2, level=-2)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_16():
    r'''Limit to first 2 nodes after (2, ) at level -2.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    leaves = score_specification.select_leaves('Voice 1')
    leaves.set_pitch(library.example_pitches_1(position=(2, )), node_count=2, level=-2)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)
