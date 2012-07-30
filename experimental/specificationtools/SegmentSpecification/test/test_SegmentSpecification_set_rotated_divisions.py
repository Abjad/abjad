from abjad.tools import *
from experimental import *
from experimental.specificationtools import library


def test_SegmentSpecification_set_rotated_divisions_01():
    '''Score with 4 one-voice staves.
    F1 divisions truncated in F1. F2, F3, F4 divisions rotated.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])

    segment.set_divisions(segment.v1, [(3, 16)])

    source = score_specification.select_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_rotated_divisions(segment.v2, source, -1)
    segment.set_rotated_divisions(segment.v3, source, -2)
    segment.set_rotated_divisions(segment.v4, source, -3)

    segment.set_rhythm(segment, library.thirty_seconds)

    segment = score_specification.append_segment('T2')

    score = score_specification.interpret()

    assert score_specification['T1'].time_signatures == [(4, 8), (3, 8)]

    assert score_specification['T1']['Voice 1']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
    assert score_specification['T1']['Voice 2']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (2, 16), (3, 16)]
    assert score_specification['T1']['Voice 3']['segment_pairs'] == \
        [(3, 16), (3, 16), (2, 16), (3, 16), (3, 16)]
    assert score_specification['T1']['Voice 4']['segment_pairs'] == \
        [(3, 16), (2, 16), (3, 16), (3, 16), (3, 16)]

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_rotated_divisions_02():
    '''As above with T2 equal to T1 and a hard break between.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    segment = score_specification.append_segment('T1')
    segment.set_time_signatures([(4, 8), (3, 8)])
    
    segment.set_divisions(segment.v1, [(3, 16)], truncate=True)
    
    source = score_specification.select_divisions('Voice 1', 'T1', segment_count=1)
    segment.set_rotated_divisions(segment.v2, source, -1)
    segment.set_rotated_divisions(segment.v3, source, -2)
    segment.set_rotated_divisions(segment.v4, source, -3)
    
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = score_specification.append_segment('T2')

    score = score_specification.interpret()

    assert score_specification['T1'].time_signatures == [(4, 8), (3, 8)]

    assert score_specification['T1']['Voice 1']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
    assert score_specification['T1']['Voice 2']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (2, 16), (3, 16)]
    assert score_specification['T1']['Voice 3']['segment_pairs'] == \
        [(3, 16), (3, 16), (2, 16), (3, 16), (3, 16)]
    assert score_specification['T1']['Voice 4']['segment_pairs'] == \
        [(3, 16), (2, 16), (3, 16), (3, 16), (3, 16)]

    assert score_specification['T2']['Voice 1']['segment_pairs'] == \
        score_specification['T1']['Voice 1']['segment_pairs']
    assert score_specification['T2']['Voice 2']['segment_pairs'] == \
        score_specification['T1']['Voice 2']['segment_pairs']
    assert score_specification['T2']['Voice 3']['segment_pairs'] == \
        score_specification['T1']['Voice 3']['segment_pairs']
    assert score_specification['T2']['Voice 4']['segment_pairs'] == \
        score_specification['T1']['Voice 4']['segment_pairs']

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
