from abjad.tools import *
from experimental import *


def test_SegmentSpecification_set_retrograde_divisions_01():
    '''Four staves with V3, V4 divisions equal to V1, V2 divisions in retrograde.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    segment.set_divisions_new([(3, 16)], contexts='Voice 1', truncate=True)
    segment.set_divisions_new([(4, 16)], contexts='Voice 2', truncate=True)

    source_1 = score_specification.select_divisions('Voice 1', 'red', segment_count=1)
    source_2 = score_specification.select_divisions('Voice 2', 'red', segment_count=1)

    segment.set_retrograde_divisions(source_1, contexts=segment.v3)
    segment.set_retrograde_divisions(source_2, contexts=segment.v4)

    segment.set_rhythm(library.thirty_seconds)

    segment = score_specification.append_segment('blue')

    score = score_specification.interpret()

    assert score_specification['red']['Voice 1']['segment_pairs'] == \
        [(3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
    assert score_specification['red']['Voice 2']['segment_pairs'] == \
        [(4, 16), (4, 16), (4, 16), (2, 16)]
    assert score_specification['red']['Voice 3']['segment_pairs'] == \
        [(2, 16), (3, 16), (3, 16), (3, 16), (3, 16)]
    assert score_specification['red']['Voice 4']['segment_pairs'] == \
        [(2, 16), (4, 16), (4, 16), (4, 16)]

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
