from abjad import *
from experimental import *


def test_SegmentSpecification__set_rhythm_increasing_01():
    '''Remake of schematic example X3.
    Uses division material requests instead of rhythm material requests.
    Necessitates setting decreasing=False on rhythm maker.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    measures = red_segment.select_background_measure_timespan()
    left_measure, right_measure = measures.partition_by_ratio((1, 1))
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 2'], selector=left_measure)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 2'], selector=right_measure)

    left_half, right_half = red_segment.timespan.divide_by_ratio((1, 1))

    voice_1_left_division_command = red_segment.request_division_command('Voice 1', selector=left_measure)
    voice_1_right_division_command = red_segment.request_division_command('Voice 1', selector=right_measure)

    red_segment.set_divisions(voice_1_left_division_command, contexts=['Voice 3'], selector=left_half)
    red_segment.set_divisions(voice_1_right_division_command, contexts=['Voice 3'], selector=right_half)

    voice_2_left_division_command = red_segment.request_division_command('Voice 2', selector=left_measure)
    voice_2_right_division_command = red_segment.request_division_command('Voice 2', selector=right_measure)

    red_segment.set_divisions(voice_2_left_division_command, contexts=['Voice 4'], selector=left_half)
    red_segment.set_divisions(voice_2_right_division_command, contexts=['Voice 4'], selector=right_half)

    red_segment.set_rhythm(library.note_tokens)

    blue_segment = score_specification.append_segment(name='blue')

    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, reverse=True)

    red_voice_1_divisions = red_segment.request_divisions('Voice 1')
    red_voice_2_divisions = red_segment.request_divisions('Voice 2')
    red_voice_3_divisions = red_segment.request_divisions('Voice 3')
    red_voice_4_divisions = red_segment.request_divisions('Voice 4')
    blue_segment.set_divisions(red_voice_1_divisions, contexts=['Voice 1'], reverse=True)
    blue_segment.set_divisions(red_voice_2_divisions, contexts=['Voice 2'], reverse=True)
    blue_segment.set_divisions(red_voice_3_divisions, contexts=['Voice 3'], reverse=True)
    blue_segment.set_divisions(red_voice_4_divisions, contexts=['Voice 4'], reverse=True)

    red_rhythm_command = red_segment.request_rhythm_command('Voice 1')
    blue_segment.set_rhythm(red_rhythm_command, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
