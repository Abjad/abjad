from abjad.tools import *
from experimental import *
from experimental.specificationtools import library


def test_multisegment_solo_01():
    '''Single division interprets cyclically over two segments.
    Division does not truncate at segment boundary.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_02():
    '''Single division interprets cyclically over two segments.
    Division truncates at segment boundary because of truncate keyword.
    Division starts over at beginning of second segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)
    
    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)], contexts=segment.v1, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_03():
    '''Single division exactly equal to duration of single segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(14, 16)], contexts=segment.v1)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_04():
    '''Single division exactly equal to duration of single segment.
    Division truncates because truncate keyword is set to true.
    Division starts over at beginning of second segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(14, 16)], contexts=segment.v1, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_05():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division does not truncate at segment boundary.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(20, 16)], contexts=segment.v1)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_06():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division truncates at segment boundary because truncate keyword is set to true.
    Division starts over from beginning of second segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)
    
    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(20, 16)], contexts=segment.v1, truncate=True)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multisegment_solo_07():
    '''Large division greater in duration than two segments.
    Division does not truncate at segment boundaries.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)
    
    segment = specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(15, 8)], contexts=segment.v1)
    segment.set_rhythm(library.thirty_seconds)

    segment = specification.append_segment('blue')
    segment = specification.append_segment('green')

    score = specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
