from abjad import *
from experimental.tools import *
import py


def test_DivisionSelector__request_modifiers_01():
    '''Division get item.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    divisions = divisions[2:5]
    divisions.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_DivisionSelector__request_modifiers_02():
    '''Partition divisions by ratio.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    left, right = divisions.partition_objects_by_ratio((1, 2))
    left.set_rhythm(library.sixteenths)
    right.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_DivisionSelector__request_modifiers_03():
    '''Partition divisions by ratio of durations.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    divisions = red_segment.select_divisions('Voice 1')
    left, right = divisions.partition_objects_by_ratio_of_durations((1, 2))
    left.set_rhythm(library.sixteenths)
    right.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_DivisionSelector__request_modifiers_04():
    '''Repeat divisions to length.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_divisions([(2, 16), (3, 16), (4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    red_divisions = red_segment.select_divisions('Voice 1')
    red_divisions = red_divisions.repeat_to_length(2)
    blue_segment.set_divisions(red_divisions)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
