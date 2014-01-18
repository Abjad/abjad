# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_measure_01():

    measure = Measure((2, 8), "c'8 d'8")
    labeltools.color_measure(measure, 'red')


    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \override Beam #'color = #red
            \override Dots #'color = #red
            \override NoteHead #'color = #red
            \override Staff.TimeSignature #'color = #red
            \override Stem #'color = #red
            \time 2/8
            c'8
            d'8
            \revert Beam #'color
            \revert Dots #'color
            \revert NoteHead #'color
            \revert Staff.TimeSignature #'color
            \revert Stem #'color
        }
        '''
        )

    assert inspect_(measure).is_well_formed()
