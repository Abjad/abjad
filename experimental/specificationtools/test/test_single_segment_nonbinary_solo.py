from abjad.tools import *
from experimental import *
from experimental.specificationtools import library


def test_single_segment_nonbinary_solo_01():
    '''Nonbinary division.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment()
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(1, 5)], contexts=segment.v1)
    segment.set_rhythm(library.tuplet_monads)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
