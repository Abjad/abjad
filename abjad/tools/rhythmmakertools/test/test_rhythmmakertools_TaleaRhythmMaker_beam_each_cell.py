# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker_beam_each_cell_01():
    r'''Beam each cell with a multipart beam spanner.
    '''

    talea, talea_denominator, prolation_addenda = [1, 1, 1, -1, 2, 2], 32, [3, 4]
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea, 
        talea_denominator, 
        prolation_addenda, 
        beam_each_cell=True,
        )

    divisions = [(2, 16), (5, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = \
        scoretools.make_measures_with_full_measure_spacer_skips(divisions)
    staff = Staff(measures)
    scoretools.replace_contents_of_measures_in_expr(staff, music)
    score = Score([staff])
    contextualize(score).autoBeaming = False

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score \with {
            autoBeaming = ##f
        } <<
            \new Staff {
                {
                    \time 2/16
                    \times 4/7 {
                        c'32 [
                        c'32
                        c'32 ]
                        r32
                        c'16 [
                        c'32 ]
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
        >>
        '''
        )
