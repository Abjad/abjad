from abjad.tools import *
from experimental import selectortools
from experimental.specificationtools import helpers
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification


def test_SegmentSpecification_set_rotated_divisions_01():
    '''Score with 4 one-voice staves.
    F1 divisions truncated in F1. F2, F3, F4 divisions rotated.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))

    segment = specification.append_segment('T1')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    segment.set_divisions(segment.v1, [(3, 16)])

    source = selectortools.request_divisions('T1', 'Voice 1', segment_count=1)
    segment.set_rotated_divisions(segment.v2, source, -1)
    segment.set_rotated_divisions(segment.v3, source, -2)
    segment.set_rotated_divisions(segment.v4, source, -3)

    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment('T2')

    score = specification.interpret()

    assert specification.segments['T1'].time_signatures == [(4, 8), (3, 8)]

    assert specification.segments['T1']['Voice 1']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
    assert specification.segments['T1']['Voice 2']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (2, 16), (3, 16)]
    assert specification.segments['T1']['Voice 3']['segment_pairs'] == \
        [(3, 16), (3, 16), (2, 16), (3, 16), (3, 16)]
    assert specification.segments['T1']['Voice 4']['segment_pairs'] == \
        [(3, 16), (2, 16), (3, 16), (3, 16), (3, 16)]

    current_function_name = introspectiontools.get_current_function_name()
    helpers.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpers.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_set_rotated_divisions_02():
    '''As above with T2 equal to T1 and a hard break between.
    '''
    
    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))
    
    segment = specification.append_segment('T1')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    
    segment.set_divisions(segment.v1, [(3, 16)], truncate=True)
    
    source = selectortools.request_divisions('T1', 'Voice 1', segment_count=1)
    segment.set_rotated_divisions(segment.v2, source, -1)
    segment.set_rotated_divisions(segment.v3, source, -2)
    segment.set_rotated_divisions(segment.v4, source, -3)
    
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment('T2')

    score = specification.interpret()

    assert specification.segments['T1'].time_signatures == [(4, 8), (3, 8)]

    assert specification.segments['T1']['Voice 1']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
    assert specification.segments['T1']['Voice 2']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (2, 16), (3, 16)]
    assert specification.segments['T1']['Voice 3']['segment_pairs'] == \
        [(3, 16), (3, 16), (2, 16), (3, 16), (3, 16)]
    assert specification.segments['T1']['Voice 4']['segment_pairs'] == \
        [(3, 16), (2, 16), (3, 16), (3, 16), (3, 16)]

    assert specification.segments['T2']['Voice 1']['segment_pairs'] == \
        specification.segments['T1']['Voice 1']['segment_pairs']
    assert specification.segments['T2']['Voice 2']['segment_pairs'] == \
        specification.segments['T1']['Voice 2']['segment_pairs']
    assert specification.segments['T2']['Voice 3']['segment_pairs'] == \
        specification.segments['T1']['Voice 3']['segment_pairs']
    assert specification.segments['T2']['Voice 4']['segment_pairs'] == \
        specification.segments['T1']['Voice 4']['segment_pairs']

    current_function_name = introspectiontools.get_current_function_name()
    helpers.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpers.read_test_output(__file__, current_function_name)
