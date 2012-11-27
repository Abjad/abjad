from abjad.tools import *
from experimental import *


def test_SegmentSpecification__select_background_measures_01():
    '''Negative start.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    last_two_measures = segment.select_background_measures(start=-2)
    segment.set_divisions([(2, 32)])
    segment.set_divisions([(3, 32)], selector=last_two_measures)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_background_measures_02():
    '''Negative stop.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    first_two_measures = segment.select_background_measures(stop=-1)
    segment.set_divisions([(2, 32)])
    segment.set_divisions([(3, 32)], selector=first_two_measures)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_background_measures_03():
    '''Negative start and stop.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    middle_measure = segment.select_background_measures(start=1, stop=-1)
    segment.set_divisions([(2, 32)])
    segment.set_divisions([(3, 32)], selector=middle_measure)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
