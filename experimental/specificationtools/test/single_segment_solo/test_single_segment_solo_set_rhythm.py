from abjad import *
from experimental import *


def test_single_segment_solo_set_rhythm_01():
    '''Two nonoverlapping rhythm selectors in one segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(2, 8)])
    first_two_measures = segment.select_background_measures(stop=2)
    segment.set_rhythm(library.thirty_seconds, selector=first_two_measures)
    last_two_measures = segment.select_background_measures(start=-2)
    segment.set_rhythm(library.sixteenths, selector=last_two_measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo_set_rhythm_02():
    '''Two overlapping rhythm selectors in one segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.thirty_seconds)
    first_two_measures = segment.select_background_measures(stop=2)
    segment.set_rhythm(library.sixteenths, selector=first_two_measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
