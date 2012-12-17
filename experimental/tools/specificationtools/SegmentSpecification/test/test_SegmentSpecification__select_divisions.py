from abjad import *
from experimental import *
import py


def test_SegmentSpecification__select_divisions_01():
    '''Divisions are interpreted for the entire score duration of a voice.
    Divisions are not interpreted segment by segment for a voice.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_divisions([(4, 8)])
    divisions_that_start_during_red = red_segment.select_divisions('Voice 1')
    divisions_that_start_during_blue = blue_segment.select_divisions('voice 1')
    red_segment.set_rhythm(library.sixteenths, timespan=divisions_that_start_during_red)
    blue_segment.set_rhythm(library.eighths, timespan=divisions_that_start_during_blue)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_02():
    '''Overlapping division selectors work across segment boundary.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_divisions([(4, 8)])
    divisions_that_start_during_red = red_segment.select_divisions('Voice 1')
    red_segment.set_rhythm(library.sixteenths, timespan=divisions_that_start_during_red)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_divisions_03():
    '''Negative index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    antepenultimate_division = red_segment.select_divisions('Voice 1', -3, -2)
    red_segment.set_rhythm(library.sixteenths, timespan=antepenultimate_division)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
