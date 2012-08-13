from abjad import *
from experimental import *


def test_multiple_segment_solo_selector_boundary_cases_01():
    '''Overlapping division commands both persist.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    first_third_of_segment = segment.select_segment_ratio_part((1, 1, 1), 0)
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=first_third_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_selector_boundary_cases_02():
    '''Overlapping division commands both persist.
    Selector here picks out a single measure.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (2, 8), (2, 8), (3, 8)])
    segment.set_divisions([(2, 16)])
    penultimate_measure = segment.select_background_measure(-2)
    segment.set_divisions([(3, 16)], selector=penultimate_measure)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_selector_boundary_cases_03():
    '''Same as above but second segment changes time signatures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (2, 8), (2, 8), (3, 8)])
    segment.set_divisions([(2, 16)])
    penultimate_measure = segment.select_background_measure(-2)
    segment.set_divisions([(3, 16)], selector=penultimate_measure)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures([(3, 16), (3, 16), (3, 16), (3, 16)])
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_selector_boundary_cases_04():
    '''Division region overlapped by segment offset selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (2, 8), (2, 8), (2, 8)])
    segment.set_divisions([(2, 16)])
    middle_chunk = segment.select_segment_offsets((2, 8), (5, 8))
    segment.set_divisions([(3, 16)], selector=middle_chunk)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures([(3, 16), (3, 16), (3, 16), (3, 16)])
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_selector_boundary_cases_05():
    '''Division region overlapped by segment ratio part selector.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (2, 8), (2, 8), (2, 8)])
    segment.set_divisions([(1, 16)])
    middle_part = segment.select_segment_ratio_part((1, 2, 1), 1)
    segment.set_divisions([(3, 16)], selector=middle_part)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures([(3, 16), (3, 16), (3, 16), (3, 16)])
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
