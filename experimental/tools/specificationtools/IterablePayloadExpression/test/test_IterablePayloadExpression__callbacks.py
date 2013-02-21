from experimental import *


def test_IterablePayloadExpression__callbacks_01():
    '''Slice payload expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions[1:3]
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_02():
    '''Partition payload expression elements by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    left_divisions, right_divisions = divisions.partition_by_ratio((1, 1))
    red_segment.set_divisions(left_divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_03():
    '''Partition payload expression elements by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    left_divisions, right_divisions = divisions.partition_by_ratio_of_durations((1, 1))
    red_segment.set_divisions(left_divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_04():
    '''Repeat divisions to truncating duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.repeat_to_duration(Duration(5, 16))
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_05():
    '''Repeat divisions to extended duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.repeat_to_duration(Duration(13, 16))
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_06():
    '''Repeat divisions to truncating length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.repeat_to_length(3)
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_07():
    '''Repeat divisions to extended length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.repeat_to_length(6)
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_08():
    '''Reflect divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.reflect()
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_09():
    '''Rotate divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions.rotate(-1)
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_IterablePayloadExpression__callbacks_10():
    '''Logical AND of divisions and timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    material_manager = specificationtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    timespan = timespantools.Timespan(Offset(2, 16), Offset(10, 16))
    divisions = divisions & timespan
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
