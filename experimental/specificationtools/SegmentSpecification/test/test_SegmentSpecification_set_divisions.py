from abjad import *
from experimental import *


def test_SegmentSpecification_set_divisions_01():
    '''Voices 1 & 2 set divisions according to ratio of background measures.
    Voices 3 & 4 set divisions according to ratio of segment duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('red')
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
    segment = score_specification.make_segment('blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_divisions_02():
    '''V3, V4 divisions equal V1, V2 divisions reversed.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts='Voice 1', truncate=True)
    segment.set_divisions([(4, 16)], contexts='Voice 2', truncate=True)
    source_1 = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    source_2 = score_specification.request_divisions('Voice 2', 'red', segment_count=1)

    segment.set_divisions(source_1, contexts=['Voice 3'], reverse=True, truncate=True)
    segment.set_divisions(source_2, contexts=['Voice 4'], reverse=True, truncate=True)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.make_segment('blue')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_divisions_03():
    '''F1 divisions truncated in F1. F2, F3, F4 divisions with rotation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1)
    source = score_specification.request_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_divisions(source, contexts=segment.v2, rotation=-1, truncate=True)
    segment.set_divisions(source, contexts=segment.v3, rotation=-2, truncate=True)
    segment.set_divisions(source, contexts=segment.v4, rotation=-3, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.make_segment('T2')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_divisions_04():
    '''As above with T2 equal to T1 and a hard break between.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1, truncate=True)
    source = score_specification.request_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_divisions(source, contexts=segment.v2, rotation=-1, truncate=True)
    segment.set_divisions(source, contexts=segment.v3, rotation=-2, truncate=True)
    segment.set_divisions(source, contexts=segment.v4, rotation=-3, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.make_segment('T2')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
