from experimental import *


def test_ScoreSpecification__set_pitch_class_transform_01():
    '''Transpose second half up a semitone.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('T1')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_02():
    '''Transpose second half by nothing (but drop into octave above middle C).
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('T0')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_03():
    '''Invert second half.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('I')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_04():
    '''Invert second half and then transpose up 1 semitone.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('T1I')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_05():
    '''Tranpose second half up 1 semitone and then invert.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('IT1')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_06():
    '''Multiply second half by 7.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('M7')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_07():
    '''Invert second half twice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('II')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_pitch_class_transform_08():
    '''Transpose second half up by 1 semitone and then up by 3 semitones.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    rhythm = library.sixteenths.new(beam_cells_together=False, beam_each_cell=True)
    score_specification.set_rhythm(rhythm)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch(library.example_pitches_1(position=(2,)))
    right.set_pitch_class_transform('T3T1')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
