# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_BeamSpecifier_beam_each_division_01():
    r'''Beam each cell with a multipart beam spanner.
    '''

    talea = rhythmmakertools.Talea(
        counts=(1, 1, 1, -1, 2, 2), 
        denominator=32, 
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(3, 4), 
        )

    divisions = [(2, 16), (5, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(music)
    score = Score([staff])
    set_(score).autoBeaming = False

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/16
                \times 4/7 {
                    c'32 [
                    c'32
                    c'32 ]
                    r32
                    c'16 [
                    c'32 ] ~
                }
            }
            {
                \time 5/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 5/7 {
                    c'32 [
                    c'32
                    c'32
                    c'32 ]
                    r32
                    c'16 [
                    c'16
                    c'32
                    c'32
                    c'32 ]
                    r32
                    c'32
                }
            }
        }
        '''
        )
