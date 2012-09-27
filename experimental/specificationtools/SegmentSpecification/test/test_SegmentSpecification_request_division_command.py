from abjad import *
from experimental import *
import py


def test_SegmentSpecification_request_division_command_01():
    '''Request division command active at 1/8 into measure 2 in earlier segment.
    Request only first element of command.
    '''
    py.test.skip('refactoring')
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8), (4, 8)])
    segment.set_divisions([(4, 16)])
    selector = segment.select_background_measures(1, 3)
    segment.set_divisions([(2, 16), (3, 16)], selector=selector)
    segment.set_rhythm(library.sixteenths)

    selector = segment.select_background_measure(2)
    offset = durationtools.Offset(1, 8)
    source = segment.request_division_command(selector=selector, offset=offset, count=1)

    segment = score_specification.make_segment(name='blue')
    segment.set_divisions(source)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_division_command_02():
    '''Request division command from future segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(5, 16)])

    green_segment = score_specification.make_segment(name='green', index=1)
    green_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_division_command = blue_segment.request_division_command('Voice 1')
    green_segment.set_divisions(blue_division_command)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
