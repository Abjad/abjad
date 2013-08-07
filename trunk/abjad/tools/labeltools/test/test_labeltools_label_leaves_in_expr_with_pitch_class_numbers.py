# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_pitch_class_numbers_01():
    r'''With number = True.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_pitch_class_numbers(staff, number=True)

    r'''
    \new Staff {
        c'8
            _ \markup {
                \small
                    0
                }
        d'8
            _ \markup {
                \small
                    2
                }
        e'8
            _ \markup {
                \small
                    4
                }
        f'8
            _ \markup {
                \small
                    5
                }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
                _ \markup {
                    \small
                        0
                    }
            d'8
                _ \markup {
                    \small
                        2
                    }
            e'8
                _ \markup {
                    \small
                        4
                    }
            f'8
                _ \markup {
                    \small
                        5
                    }
        }
        '''
        )


def test_labeltools_label_leaves_in_expr_with_pitch_class_numbers_02():
    r'''With color = True.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_pitch_class_numbers(t, number=False, color=True)

    r'''
    \new Staff {
      \once \override NoteHead #'color = #(x11-color 'red)
      c'8
      \once \override NoteHead #'color = #(x11-color 'orange)
      d'8
      \once \override NoteHead #'color = #(x11-color 'ForestGreen)
      e'8
      \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
      f'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            \once \override NoteHead #'color = #(x11-color 'red)
            c'8
            \once \override NoteHead #'color = #(x11-color 'orange)
            d'8
            \once \override NoteHead #'color = #(x11-color 'ForestGreen)
            e'8
            \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
            f'8
        }
        '''
        )
