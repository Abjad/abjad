from abjad import *
from experimental import *


def test_single_segment_duo_division_command_request_01():
    '''Intervoice division command request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 1'], truncate=True)
    segment.set_rhythm(library.sixteenths)
    command = segment.request_division_command('Voice 1')
    segment.set_divisions(command, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_duo_division_command_request_02():
    '''Intervoice division command request. Reverse command at request-time.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 1'], truncate=True)
    segment.set_rhythm(library.sixteenths)
    command = segment.request_division_command('Voice 1', reverse=True)
    segment.set_divisions(command, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
