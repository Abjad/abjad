from experimental import *


def test_CounttimeComponentSelectExpression__callbacks_01():
    '''Slice leaves.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves[5:9]
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_02():
    '''Partition rhythm by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    left_red_leaves, right_red_leaves = red_leaves.partition_by_ratio((1, 3))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(left_red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_03():
    '''Partition rhythm by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    left_red_leaves, right_red_leaves = red_leaves.partition_by_ratio_of_durations((1, 1))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(left_red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_04():
    '''Repeat to duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_duration(Duration(7, 16))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_05():
    '''Repeat to length.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_length(5)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_06():
    '''Reflect rhythm.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.reflect()
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_07():
    '''Rotate rhythm by count.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.rotate(-1)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_08():
    '''Rotate rhythm by duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.rotate(-Duration(1, 32))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_09():
    '''Logical AND of rhythm and timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    timespan = timespantools.Timespan(Offset(1, 32), Offset(18, 32))
    red_leaves = red_leaves & timespan
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
