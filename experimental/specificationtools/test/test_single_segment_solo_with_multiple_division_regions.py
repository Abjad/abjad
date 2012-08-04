from abjad.tools import *
from experimental import *


def test_single_segment_solo_with_multiple_division_regions_01():
    '''Three measures and three division regions.
    One division region per measure.
    Selection handle by measure index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])

    first_measure = segment.select_background_measure(0)
    second_measure = segment.select_background_measure(1)
    third_measure = segment.select_background_measure(2)

    # TODO: make it possible to eliminate contexts assignment in arbitrary ones of these settings
    #segment.set_divisions_new([(2, 32)], timespan=first_measure, contexts=['Voice 1'])
    segment.set_divisions_new([(2, 32)], timespan=first_measure)
    #segment.set_divisions_new([(3, 32)], timespan=second_measure, contexts=['Voice 1'])
    segment.set_divisions_new([(3, 32)], timespan=second_measure)
    #segment.set_divisions_new([(4, 32)], timespan=third_measure, contexts=['Voice 1'])
    segment.set_divisions_new([(4, 32)], timespan=third_measure)

    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
