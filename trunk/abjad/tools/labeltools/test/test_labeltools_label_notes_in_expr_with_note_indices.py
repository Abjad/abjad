# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_notes_in_expr_with_note_indices_01():

    staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")
    labeltools.label_notes_in_expr_with_note_indices(staff)

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
                    1
                }
        r8
        r8
        g'8
            _ \markup {
                \small
                    2
                }
        a'8
            _ \markup {
                \small
                    3
                }
        r8
        c''8
            _ \markup {
                \small
                    4
                }
    }
    '''

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
                        1
                    }
            r8
            r8
            g'8
                _ \markup {
                    \small
                        2
                    }
            a'8
                _ \markup {
                    \small
                        3
                    }
            r8
            c''8
                _ \markup {
                    \small
                        4
                    }
        }
        '''
        )
