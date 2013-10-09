# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_contents_of_container_01():

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))
    labeltools.color_contents_of_container(staff[1], 'blue')

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \override Accidental #'color = #blue
                \override Beam #'color = #blue
                \override Dots #'color = #blue
                \override NoteHead #'color = #blue
                \override Rest #'color = #blue
                \override Stem #'color = #blue
                \override TupletBracket #'color = #blue
                \override TupletNumber #'color = #blue
                e'8
                f'8
                \revert Accidental #'color
                \revert Beam #'color
                \revert Dots #'color
                \revert NoteHead #'color
                \revert Rest #'color
                \revert Stem #'color
                \revert TupletBracket #'color
                \revert TupletNumber #'color
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
