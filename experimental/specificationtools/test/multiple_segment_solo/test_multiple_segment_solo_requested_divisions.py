from abjad import *
from experimental import *
import py


def test_multiple_segment_solo_requested_divisions_01():
    '''Intersegment division material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(3, 8), (2, 8)])
    segment.set_divisions([(4, 16)])
    segment.set_rhythm(library.sixteenths)
    red_divisions = segment.request_divisions('Voice 1')

    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures([(5, 8), (2, 8)])
    segment.set_divisions(red_divisions)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_requested_divisions_02():
    '''Intersegment division material request.
    With start- and stop-offsets.
    '''
    py.test.skip('skpping until ScoreSpecification.request_divisions() is refactored.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(4, 16)])
    segment.set_rhythm(library.sixteenths)
    #some_divisions = segment.request_divisions('Voice 1', start_offset=(1, 16), stop_offset=(10, 16))
    # TODO: refactor ScoreSpecification.request_divisions() to make the following two lines work
    #selector = score_specification.select_offsets(start_offset=(1, 16), stop_offset=(10, 16))
    #some_divisions = segment.request_divisions('Voice 1', selector=selector)

    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures([(7, 16), (6, 16)])
    segment.set_divisions(some_divisions)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
