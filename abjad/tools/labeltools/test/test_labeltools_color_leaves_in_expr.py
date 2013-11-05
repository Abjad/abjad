# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_leaves_in_expr_01():

    staff = Staff("cs'8. r8. s8. <c' cs' a'>8.")
    labeltools.color_leaves_in_expr(staff, 'red')

    r'''
    \new Staff {
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        cs'8.
        \once \override Dots #'color = #red
        \once \override Rest #'color = #red
        r8.
        s8.
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        <c' cs' a'>8.
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \once \override Accidental #'color = #red
            \once \override Beam #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            \once \override Stem #'color = #red
            cs'8.
            \once \override Dots #'color = #red
            \once \override Rest #'color = #red
            r8.
            s8.
            \once \override Accidental #'color = #red
            \once \override Beam #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            \once \override Stem #'color = #red
            <c' cs' a'>8.
        }
        '''
        )
