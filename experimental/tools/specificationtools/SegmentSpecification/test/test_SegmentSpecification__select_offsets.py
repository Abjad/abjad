from experimental import *


def test_SegmentSpecification__select_offsets_01():
    '''Explicit offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment= red_segment.timespan.set_offsets((1, 8), (4, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_02():
    '''Implicit start-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = red_segment.timespan.set_offsets(stop_offset=(4, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_03():
    '''Implicit stop-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = red_segment.timespan.set_offsets(start_offset=(2, 8))
    red_segment.set_divisions([(2, 16)])
    middle_part_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_04():
    '''Implicit start- and stop-offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_05():
    '''Negative start-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(start_offset=(-4, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_06():
    '''Negative stop-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(stop_offset=(-2, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_offsets_07():
    '''Negative start and stop-offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = red_segment.timespan.set_offsets(start_offset=(-4, 8), stop_offset=(-2, 8))
    red_segment.set_divisions([(2, 16)])
    whole_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
