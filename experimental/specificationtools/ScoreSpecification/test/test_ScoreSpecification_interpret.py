from abjad.tools import *
from baca.specificationtools.ScoreSpecification import ScoreSpecification
from library import *
import baca
import py


def test_ScoreSpecification_interpret_01():
    py.test.skip('still working on this one ...')

    specification = ScoreSpecification(scoretemplatetools.StringQuartetScoreTemplate)

    segment = specification.append_segment(name='A')
    segment.set_tempo(segment, 108)
    segment.set_time_signatures(segment, [(2, 8), (2, 8), (3, 8), (2, 8), (3, 8)])
    segment.set_aggregate(segment, baca.pitch.CC[0][0])
    segment.set_pitch_classes_timewise(segment, [0, 8, 9, 11, 1, 2, 4, 6, 3, 5, 7, 10])
    segment.set_rhythm(segment.vn1, (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_register(segment.vn1, cello_treble)
    segment.set_dynamics(segment.vn1, terraced_fortissimo)
    segment.set_rhythm(segment.vn2, (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_register(segment.vn2, cello_treble)
    segment.set_dynamics(segment.vn2, terraced_fortissimo)
