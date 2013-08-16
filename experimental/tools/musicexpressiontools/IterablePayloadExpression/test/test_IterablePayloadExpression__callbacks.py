# -*- encoding: utf-8 -*-
import py.test
from experimental import *


def test_IterablePayloadExpression__callbacks_01():
    r'''Slice payload expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Partition payload expression elements by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Partition payload expression elements by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Repeat divisions to truncating duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Repeat divisions to extended duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Repeat divisions to truncating length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Repeat divisions to extended length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Reflect divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Rotate divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
    r'''Logical AND of divisions and timespan.
    '''
    py.test.skip('FIXME: Broke after TypedList stopped inheriting from list.')
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
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
