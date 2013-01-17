from abjad import *
from experimental import *


def test_AbsoluteExpression__payload_callbacks_01():
    '''Slice absolute expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    material_manager = settingtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    divisions = divisions[1:3]
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_AbsoluteExpression__payload_callbacks_02():
    '''Partition absolute expression elements by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    material_manager = settingtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    left_divisions, right_divisions = divisions.partition_by_ratio((1, 1))
    red_segment.set_divisions(left_divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_AbsoluteExpression__payload_callbacks_03():
    '''Partition absolute expression elements by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    material_manager = settingtools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(3 * [(3, 8)])
    divisions = material_manager.register_material([(1, 16), (2, 16), (3, 16), (4, 16)])
    left_divisions, right_divisions = divisions.partition_by_ratio_of_durations((1, 1))
    red_segment.set_divisions(left_divisions)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
