from abjad import *
from experimental.tools import *
import py


# NEXT TODO: make this work
def test_CounttimeComponentSelector__payload_callbacks_01():
    '''Slice leaves.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves[5:10]
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_02():
    '''Partition rhythm by ratio.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_left, red_right = leaves.partition_by_ratio((1, 1))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_left)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_03():
    '''Partition rhythm by ratio of durations.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_left, red_right = leaves.partition_by_ratio_of_durations((1, 1))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_left)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_04():
    '''Repeat to duration.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_duration(Duration(8, 16))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_05():
    '''Repeat to length.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_length(5)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_06():
    '''Reflect rhythm.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.reflect()
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelector__payload_callbacks_07():
    '''Rotate rhythm by count.
    '''
    py.test.skip('working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.rotate(-1)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
