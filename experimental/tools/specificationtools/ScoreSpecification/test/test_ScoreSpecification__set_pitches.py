from experimental import *
import copy
import py


def test_ScoreSpecification__set_pitches_01():
    '''Read from server over entire score.
    '''
    py.test.skip('working on this one')

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    score_specification.set_pitches(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitches_02():
    '''Read from server contiguous leaves.
    '''
    py.test.skip('working on this one')

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    leaves = score_specification.select_leaves('Voice 1')[10:20]
    leaves.set_pitches(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitches_03():
    '''Read from server over discontiguous leaves in same voice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    first_leaves = score_specification.select_leaves('Voice 1')[:10]
    last_leaves = score_specification.select_leaves('Voice 1')[-10:]
    leaves = first_leaves + last_leaves
    leaves.set_pitches(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitches_04():
    '''Read from server over discontiguous leaves in different voices.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    first_leaves = score_specification.select_leaves('Voice 1')[:10]
    last_leaves = score_specification.select_leaves('Voice 2')[-10:]
    leaves = first_leaves + last_leaves
    leaves.set_pitches(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitches_05():
    '''Read from server over overlaid pitches in discontiguous select expression.
    Earlier pitch assignments are simply overwritten by later pitch assignments.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    first_leaves = score_specification.select_leaves('Voice 1')[:9]
    last_leaves = score_specification.select_leaves('Voice 1')[3:12]
    leaves = first_leaves + last_leaves
    leaves.set_pitches(library.example_pitches_1())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
