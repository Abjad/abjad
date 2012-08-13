from abjad import *
from experimental import *


def test_multiple_segment_solo_nonpersistent_overlapping_division_selectors_01():
    '''Nonpersistent overlapping background measure division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = segment.select_background_measures(1, 3)
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=False)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_nonpersistent_overlapping_division_selectors_02():
    '''Nonpersistent overlapping background measures ratio part division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = segment.select_background_measures_ratio_part((1, 2, 1), 1)
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=False)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_nonpersistent_overlapping_division_selectors_03():
    '''Nonpersistent overlapping segment offsets division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = segment.select_segment_offsets((3, 16), (9, 16))
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=False)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_nonpersistent_overlapping_division_selectors_04():
    '''Nonpersistent overlapping segment ratio part division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = segment.select_segment_ratio_part((1, 2, 1), 1)
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=False)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
