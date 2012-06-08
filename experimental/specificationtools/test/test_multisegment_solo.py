from abjad.tools import *
from helpers import *
from specificationtools import ScoreSpecification
import specificationtools.library as library
import py


def test_multisegment_solo_01():
    '''Single division interprets cyclically over two segments.
    Division does not truncate at segment boundary.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_02():
    '''Single division interprets cyclically over two segments.
    Division truncates at segment boundary because of truncate keyword.
    Division starts over at beginning of second segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_03():
    '''Single division exactly equal to duration of single segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_04():
    '''Single division exactly equal to duration of single segment.
    Division truncates because truncate keyword is set to true.
    Division starts over at beginning of second segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_05():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division does not truncate at segment boundary.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_06():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division truncates at segment boundary because truncate keyword is set to true.
    Division starts over from beginning of second segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_multisegment_solo_07():
    '''Single division greater in duration than two segments but lesser in duration than three segments.
    Division does not truncate at segment boundaries.
    '''
    py.test.skip('this one fails and means that some division calculation stuff needs work.')

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(15, 8)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()
    segment = specification.append_segment()

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name, go=True)

    assert score.format == read_test_output(__file__, current_function_name)
