from abjad import *
from experimental import *
import py


def test_multiple_segment_solo__persistent_overlapping_division_selectors_01():
    '''Persistent overlapping measure division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_selectors_02():
    '''Persistent overlapping measures ratio part division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    measures = red_segment.select_measures('Voice 1')
    middle_two_measures = measures.partition_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_selectors_03():
    '''Persistent overlapping segment offsets division selector.
    '''
    py.test.skip('FIXME')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.set_offsets((3, 16), (9, 16))
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_selectors_04():
    '''Persistent overlapping segment ratio part division selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_selectors_05():
    '''Persistent overlapping measure division selector can be overwritten.
    '''
    py.test.skip('working on this one now.')
    
    '''
    What's wrong here is that the not-overwritten parts of the blue segment
    fall back to default full-measure divisions rather than expressing the 1/16
    divisions set earlier in the red segment. That's what needs to be debugged.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)])
    middle_two_measures = red_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    # the following two lines trigger the bug
    middle_two_measures = blue_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
