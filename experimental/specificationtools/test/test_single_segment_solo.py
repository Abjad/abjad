from abjad.tools import *
from helpers import *
from specificationtools import ScoreSpecification
import specificationtools.library as library


def test_single_segment_solo_01():
    '''Single division with duration less than segment.
    Division interprets cyclically.
    Division truncates at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_single_segment_solo_02():
    '''Single division with duration equal to segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_single_segment_solo_03():
    '''Single division with duration greater than segment.
    Division truncates at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)
