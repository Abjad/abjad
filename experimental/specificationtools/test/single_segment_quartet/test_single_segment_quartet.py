from abjad import *
from experimental import *


def test_single_segment_quartet_01():
    '''Single-segment test in preparation for exemplum [X3].
    Quartet in 2 segments red, blue. Red time signatures 6/8 3/8. 
    F1 1:1 of measures then left part 3/16 and right part 5/16 divisions.
    F2 1:1 of meaures then [5/16, 3/16]
    F3 1:1 of total time then [3/16, 5/16] from F1.
    F4 1:1 of total time then [5/16, 3/16] from F2.
    Filled note tokens scorewide.
    Blue segment equal to red flipped about the y axis exactly.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    measures = red_segment.select_background_measures()
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

    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
