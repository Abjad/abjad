from abjad import *
from experimental import *


def test_SegmentSpecification_set_divisions_01():
    '''Voices 1 & 2 set divisions according to ratio of background measures.
    Voices 3 & 4 set divisions according to ratio of segment duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    first_measure = segment.select_background_measures(stop=1)
    second_measure = segment.select_background_measures(start=-1)
    first_half = segment.select_segment_ratio_part((1, 1), 0)
    second_half = segment.select_segment_ratio_part((1, 1), 1)

    segment.set_divisions([(3, 16)], selector=first_measure, contexts=['Voice 1'], persist=False)
    segment.set_divisions([(5, 16)], selector=second_measure, contexts=['Voice 1'], persist=False)

    segment.set_divisions([(5, 16)], selector=first_measure, contexts=['Voice 2'], persist=False)
    segment.set_divisions([(3, 16)], selector=second_measure, contexts=['Voice 2'], persist=False)

    segment.set_divisions([(3, 16)], selector=first_half, contexts=['Voice 3'], persist=False)
    segment.set_divisions([(5, 16)], selector=second_half, contexts=['Voice 3'], persist=False)

    segment.set_divisions([(5, 16)], selector=first_half, contexts=['Voice 4'], persist=False)
    segment.set_divisions([(3, 16)], selector=second_half, contexts=['Voice 4'], persist=False)

    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_divisions_02():
    '''Reverse keyword works on list input.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(5, 16), (3, 16)], reverse=True)
    segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_divisions_03():
    '''Request- and set-time 'reverse' keywords undo each other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(5, 16), (3, 16)], contexts=['Voice 1'])
    voice_1_division_command = segment.request_division_command('Voice 1', reverse=True)
    segment.set_divisions(voice_1_division_command, contexts=['Voice 2'], reverse=True)
    segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
