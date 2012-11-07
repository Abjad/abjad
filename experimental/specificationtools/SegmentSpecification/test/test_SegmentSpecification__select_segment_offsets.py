from abjad import *
from experimental import *


def test_SegmentSpecification__select_segment_offsets_01():
    '''Explicit offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = segment.select_segment_offsets(start=(1, 8), stop=(4, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=middle_part_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_02():
    '''Implicit start-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = segment.select_segment_offsets(stop=(4, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=middle_part_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_03():
    '''Implicit stop-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_part_of_segment = segment.select_segment_offsets(start=(2, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=middle_part_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_04():
    '''Implicit start- and stop-offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = segment.select_segment_offsets()
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=whole_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_05():
    '''Negative start-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = segment.select_segment_offsets(start=(-4, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=whole_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_06():
    '''Negative stop-offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = segment.select_segment_offsets(stop=(-2, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=whole_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_segment_offsets_07():
    '''Negative start and stop-offsets.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    whole_segment = segment.select_segment_offsets(start=(-4, 8), stop=(-2, 8))
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=whole_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
